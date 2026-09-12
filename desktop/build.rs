fn main() {
    println!("cargo:rerun-if-env-changed=REMIXFUN_SOURCE_SHA");
    tauri_build::build()
}
