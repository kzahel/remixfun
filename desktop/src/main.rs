#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::{
    process::{Child, Command, Stdio},
    sync::Mutex,
    time::{Duration, Instant},
};
use tauri::Manager;

const URL: &str = "http://127.0.0.1:8788";
const VERSION: &str = env!("CARGO_PKG_VERSION");
const SOURCE_SHA: &str = match option_env!("REMIXFUN_SOURCE_SHA") {
    Some(value) => value,
    None => "development",
};

struct ServiceProcess(Mutex<Option<Child>>);

fn owner_token() -> &'static str {
    static TOKEN: std::sync::OnceLock<String> = std::sync::OnceLock::new();
    TOKEN.get_or_init(|| uuid::Uuid::new_v4().to_string())
}

static SHUTDOWN_REQUESTED: std::sync::atomic::AtomicBool =
    std::sync::atomic::AtomicBool::new(false);

fn request_owned_shutdown() -> bool {
    if SHUTDOWN_REQUESTED.load(std::sync::atomic::Ordering::SeqCst) {
        return true;
    }
    let accepted = reqwest::blocking::Client::builder()
        .timeout(Duration::from_secs(5))
        .no_proxy()
        .build()
        .ok()
        .and_then(|client| {
            client
                .post(format!("{URL}/api/shutdown"))
                .header("X-Remixfun-Owner", owner_token())
                .send()
                .ok()
        })
        .map(|response| response.status().is_success())
        .unwrap_or(false);
    if accepted {
        SHUTDOWN_REQUESTED.store(true, std::sync::atomic::Ordering::SeqCst);
    }
    accepted
}

fn stop_owned(child: &mut Child) {
    if request_owned_shutdown() {
        let deadline = Instant::now() + Duration::from_secs(30);
        while Instant::now() < deadline {
            if child.try_wait().ok().flatten().is_some() {
                return;
            }
            std::thread::sleep(Duration::from_millis(100));
        }
    }
    let _ = child.kill();
    let _ = child.wait();
}

impl Drop for ServiceProcess {
    fn drop(&mut self) {
        if let Ok(child) = self.0.get_mut() {
            if let Some(mut child) = child.take() {
                stop_owned(&mut child);
            }
        }
    }
}

fn health(client: &reqwest::blocking::Client) -> Option<serde_json::Value> {
    client
        .get(format!("{URL}/api/health"))
        .send()
        .ok()?
        .error_for_status()
        .ok()?
        .json()
        .ok()
}

fn compatible(value: &serde_json::Value) -> bool {
    value["app"] == "remixfun"
        && value["version"] == VERSION
        && value["api_version"] == 1
        && value["source_sha"] == SOURCE_SHA
}

fn start_service(
    client: &reqwest::blocking::Client,
) -> Result<Option<Child>, Box<dyn std::error::Error>> {
    if let Some(current) = health(client) {
        if !compatible(&current) {
            return Err(
                "Port 8788 belongs to an incompatible service. Stop it before opening Remixfun."
                    .into(),
            );
        }
        return Ok(None); // An independently started service is never owned by this window.
    }
    let instance = format!("desktop-{}", std::process::id());
    let mut command;
    if cfg!(debug_assertions) {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .parent()
            .unwrap();
        let python = if cfg!(windows) {
            root.join(".venv/Scripts/python.exe")
        } else {
            root.join(".venv/bin/python")
        };
        command = Command::new(python);
        command.args(["-m", "remixfun.cli"]);
        command.current_dir(root);
    } else {
        let sibling = std::env::current_exe()?
            .parent()
            .unwrap()
            .join(if cfg!(windows) {
                "remixfun-service.exe"
            } else {
                "remixfun-service"
            });
        command = Command::new(sibling);
    }
    command
        .args(["serve", "--instance", &instance])
        .env("REMIXFUN_OWNER_TOKEN", owner_token())
        .env("REMIXFUN_SOURCE_SHA", SOURCE_SHA);
    command
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null());
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        command.creation_flags(0x08000000); // CREATE_NO_WINDOW
    }
    let mut child = command.spawn()?;
    let deadline = Instant::now() + Duration::from_secs(30);
    while Instant::now() < deadline {
        if child.try_wait()?.is_some() {
            return Err("The application service could not start. Check that port 8788 and the library are available.".into());
        }
        if let Some(current) = health(client) {
            if compatible(&current) && current["instance"] == instance {
                return Ok(Some(child));
            }
            let _ = child.kill();
            let _ = child.wait();
            return Err("Another service took port 8788 during startup.".into());
        }
        std::thread::sleep(Duration::from_millis(100));
    }
    let _ = child.kill();
    let _ = child.wait();
    Err("Timed out waiting for the application service.".into())
}

fn main() {
    let application = tauri::Builder::default()
        .plugin(tauri_plugin_single_instance::init(|app, _, _| {
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.unminimize();
                let _ = window.set_focus();
            }
        }))
        .setup(|app| {
            let client = reqwest::blocking::Client::builder().timeout(Duration::from_secs(2)).no_proxy().build()?;
            let child = start_service(&client)?;
            app.manage(ServiceProcess(Mutex::new(child)));
            tauri::WebviewWindowBuilder::new(app, "main", tauri::WebviewUrl::External(URL.parse()?))
                .title("Remixfun").inner_size(1320.0, 930.0).min_inner_size(720.0, 640.0)
                .on_navigation(|url| url.scheme() == "http" && url.host_str() == Some("127.0.0.1") && url.port() == Some(8788))
                .build()?;
            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { api, .. } = event {
                let state = window.state::<ServiceProcess>();
                let owned = state.0.lock().map(|child| child.is_some()).unwrap_or(false);
                if owned {
                    // Admission closes atomically at the service before this window
                    // exits; downloads are flushed and remain resumable on relaunch.
                    if !request_owned_shutdown() {
                        api.prevent_close();
                        if let Some(webview) = window.get_webview_window("main") {
                            let _ = webview.eval("alert('Generation is active or the service cannot prepare to close. Finish or inspect generation before closing Remixfun.');");
                        }
                    }
                }
            }
        })
        .build(tauri::generate_context!());
    let application = match application {
        Ok(application) => application,
        Err(error) => {
            eprintln!("Remixfun could not start: {error}");
            #[cfg(windows)]
            {
                let title: Vec<u16> = "Remixfun could not start\0".encode_utf16().collect();
                let message: Vec<u16> = format!("{error}\0").encode_utf16().collect();
                // Both UTF-16 buffers remain alive for the synchronous native dialog.
                unsafe {
                    windows_sys::Win32::UI::WindowsAndMessaging::MessageBoxW(
                        std::ptr::null_mut(),
                        message.as_ptr(),
                        title.as_ptr(),
                        windows_sys::Win32::UI::WindowsAndMessaging::MB_OK
                            | windows_sys::Win32::UI::WindowsAndMessaging::MB_ICONERROR,
                    );
                }
            }
            std::process::exit(1);
        }
    };
    application.run(|app, event| {
        if let tauri::RunEvent::Exit = event {
            if let Some(state) = app.try_state::<ServiceProcess>() {
                if let Ok(mut child) = state.0.lock() {
                    if let Some(mut child) = child.take() {
                        stop_owned(&mut child);
                    }
                }
            }
        }
    });
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn attachment_requires_app_version_protocol_and_source() {
        let mut v = serde_json::json!({"app":"remixfun", "version":VERSION, "api_version":1, "source_sha":SOURCE_SHA});
        assert!(compatible(&v));
        for field in ["app", "version", "api_version", "source_sha"] {
            let old = v[field].take();
            assert!(!compatible(&v), "must reject missing {field}");
            v[field] = old;
        }
    }
}
