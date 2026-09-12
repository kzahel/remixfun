import { useEffect, useState } from "react";

type File = { file_id: string; name: string; sha256: string; size_estimate: number | null };
type Download = { id: string; status: string; downloaded_bytes: number; total_bytes: number | null; message: string; consumers?: string[] };
type Dependency = { id: string; name: string; version_name?: string; status: string; message?: string;
  file: File | null; candidates: File[]; download?: Download };
export type Plan = { revision: string; dependencies: Dependency[]; total_download_bytes: number; unknown_sizes: number;
  generation_blockers: string[]; operation?: { status: string; message?: string };
  reproduction?: { revision: string; ready: boolean; assumptions: { field: string; reason: string }[]; mappings: unknown[] } };

export async function modelApi<T>(path: string, method = "GET", body?: unknown): Promise<T> {
  const res = await fetch(`/api${path}`, { method, ...(body === undefined ? {} : {
    headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  }) });
  const data = await res.json();
  if (!res.ok) throw new Error(typeof data.detail === "string" ? data.detail : "The model request could not be completed.");
  return data;
}

export function bytes(value: number | null) {
  if (value === null) return "size unknown";
  if (value >= 1e9) return `${(value / 1e9).toFixed(2)} GB`;
  return `${(value / 1e6).toFixed(1)} MB`;
}

const labels: Record<string, string> = { available: "Available", download_needed: "Download needed", choose_file: "Choose file",
  blocked: "Needs attention", queued: "Queued", downloading: "Downloading", verifying: "Verifying SHA-256",
  retry_wait: "Retrying", paused: "Paused", canceled: "Canceled", failed: "Download failed" };

export function ModelDownloads({ importId, onPlan }: { importId: string; onPlan?: (plan: Plan | null) => void }) {
  const [plan, setPlan] = useState<Plan | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [choices, setChoices] = useState<Record<string, string>>({});
  useEffect(() => {
    let active = true;
    let timer: ReturnType<typeof setTimeout>;
    setPlan(null); setError(""); setChoices({});
    async function poll() {
      try {
        const next = await modelApi<Plan>(`/imports/${importId}/dependencies`);
        if (active) { setPlan(next); onPlan?.(next); setError(""); }
      } catch (e) { if (active) { setError((e as Error).message); onPlan?.(null); } }
      if (active) timer = setTimeout(poll, 1000);
    }
    poll();
    return () => { active = false; clearTimeout(timer); };
  }, [importId, onPlan]);

  async function command(path: string, body?: unknown) {
    setBusy(true); setError("");
    try {
      await modelApi(path, "POST", body);
      setPlan(await modelApi(`/imports/${importId}/dependencies`));
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  const resolving = plan?.operation && ["queued", "running"].includes(plan.operation.status);
  const needed = plan?.dependencies.filter(d => d.status === "download_needed" || (d.status === "choose_file" && choices[d.id]));
  const selectedFiles = Array.from(new Map(needed?.map(d => d.file ?? d.candidates.find(f => f.file_id === choices[d.id]))
    .filter((f): f is File => !!f).map(f => [f.sha256, f])).values());
  return <section className="model-downloads" aria-label="Model downloads">
    <div className="section-heading"><h3>Model dependencies</h3><span>{plan?.dependencies.length ?? "…"}</span></div>
    {!plan && <p>Checking model availability…</p>}
    {resolving && <p role="status">Checking model files and local libraries…</p>}
    {plan?.operation?.status === "failed" && <p className="notice">{plan.operation.message}</p>}
    {plan?.dependencies.map(d => <div className="model-download" key={d.id}>
      <strong>{d.name}</strong>{d.version_name && <small>{d.version_name}</small>}
      <span className="tag">{labels[d.status] ?? d.status}</span>
      {d.file && <small>{d.file.name} · {bytes(d.file.size_estimate)}</small>}
      {d.message && <p>{d.message}</p>}
      {d.status === "choose_file" && <label>Source model file
        <select value={choices[d.id] ?? ""} onChange={e => setChoices({ ...choices, [d.id]: e.target.value })}>
          <option value="">Select the source file variant</option>
          {d.candidates.map(f => <option key={f.file_id} value={f.file_id}>{f.name} · {bytes(f.size_estimate)}</option>)}
        </select>
      </label>}
      {d.download && d.status !== "available" && <>
        {(d.download.consumers?.length ?? 0) > 1 && <p>This model download is shared by multiple imports. These controls affect the shared transfer.</p>}
        <p aria-live="polite">{bytes(d.download.downloaded_bytes)} / {bytes(d.download.total_bytes)}</p>
        <progress aria-label={`${d.name} download progress`} value={d.download.total_bytes ? d.download.downloaded_bytes : undefined}
          max={d.download.total_bytes ?? undefined} />
        {["queued", "downloading", "retry_wait"].includes(d.download.status) && <button className="secondary" disabled={busy}
          onClick={() => command(`/downloads/${d.download!.id}/pause`)}>Pause download</button>}
        {["paused", "failed", "canceled"].includes(d.download.status) && <button className="secondary" disabled={busy}
          onClick={() => command(`/downloads/${d.download!.id}/${d.download!.status === "paused" ? "resume" : "retry"}`)}>
          {d.download.status === "paused" ? "Resume download" : "Retry download"}</button>}
        {d.download.status === "paused" && <button className="secondary" disabled={busy}
          onClick={() => command(`/downloads/${d.download!.id}/cancel`)}>Discard partial download</button>}
      </>}
      <details className="advanced"><summary>File identity</summary><pre>{JSON.stringify({ selected: d.file, candidates: d.candidates }, null, 2)}</pre></details>
    </div>)}
    {plan && !plan.dependencies.length && <p className="notice">No exact model version was recovered from this source.</p>}
    {!!needed?.length && <button className="primary" disabled={busy || !!resolving}
      onClick={() => command(`/imports/${importId}/downloads`, { revision: plan!.revision, choices })}>
      Download missing models · {selectedFiles.some(f => f.size_estimate === null) ? "check file sizes" : bytes(selectedFiles.reduce((sum, f) => sum + (f.size_estimate ?? 0), 0))}</button>}
    <button className="secondary" disabled={busy || !!resolving}
      onClick={() => command(`/imports/${importId}/dependencies/resolve`)}>Refresh model details</button>
    {error && <p role="alert" className="notice">{error}</p>}
    {plan && <div className="notice"><strong>{plan.reproduction?.ready && !plan.generation_blockers.length
      ? "Ready to try this recipe." : plan.dependencies.length > 0 && plan.dependencies.every(d => d.status === "available")
        ? "Models available. Generation needs setup." : "Recipe saved. Reproduction needs setup."}</strong>
      {plan.generation_blockers.map(reason => <p key={reason}>{reason}</p>)}</div>}
    {plan?.reproduction?.ready && <div className="notice"><strong>Settings for this attempt</strong>
      {plan.reproduction.assumptions.map(a => <p key={a.field}>{a.reason}</p>)}
      <p>Try reproduction uses these assumptions and saves them with the result. Your source recipe stays unchanged.</p>
      <details className="advanced"><summary>Sampler and CLIP mapping</summary><pre>{JSON.stringify(plan.reproduction.mappings, null, 2)}</pre></details>
    </div>}
  </section>;
}

export function ModelSettings() {
  const [root, setRoot] = useState("");
  const [paths, setPaths] = useState("");
  const [key, setKey] = useState("");
  const [configured, setConfigured] = useState(false);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    modelApi<{ model_root: string; model_paths: string[]; civitai_key_configured: boolean }>("/models/settings")
      .then(s => { setRoot(s.model_root); setPaths(s.model_paths.join("\n")); setConfigured(s.civitai_key_configured); })
      .catch(e => setMessage(e.message));
  }, []);
  async function save(action: "folders" | "key" | "scan") {
    setBusy(true);
    try {
      if (action === "folders") {
        const result = await modelApi<{ restart_required: boolean }>("/models/settings", "PUT", {
          model_root: root, model_paths: paths.split("\n").map(p => p.trim()).filter(Boolean),
        });
        setMessage(result.restart_required ? "Folders saved. Restart the app to use the new model cache. Existing files and partial downloads remain in the old folder." : "Model folders saved.");
      } else if (action === "key") {
        await modelApi("/models/credential", "PUT", { key });
        setConfigured(!!key); setKey(""); setMessage(key ? "Civitai key saved in the operating-system credential store." : "Civitai key removed.");
      } else {
        await modelApi("/models/scan", "POST");
        setMessage("Local model verification started. Reopen a source to see its model availability.");
      }
    } catch (e) { setMessage((e as Error).message); }
    finally { setBusy(false); }
  }
  return <div className="model-settings">
    <label>Model cache folder<input value={root} onChange={e => setRoot(e.target.value)} /></label>
    <label>Existing model folders · one per line<textarea value={paths} onChange={e => setPaths(e.target.value)} /></label>
    <button className="secondary" disabled={busy} onClick={() => save("folders")}>Save model folders</button>
    <button className="secondary" disabled={busy} onClick={() => save("scan")}>Check existing models</button>
    <label>Civitai API key {configured ? "· saved" : "· optional"}<input type="password" autoComplete="off" value={key} onChange={e => setKey(e.target.value)} /></label>
    <button className="secondary" disabled={busy} onClick={() => save("key")}>{key ? "Save Civitai key" : "Remove saved key"}</button>
    {message && <p role="status" className="notice">{message}</p>}
  </div>;
}
