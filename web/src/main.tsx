import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowDownToLine,
  ArrowLeft,
  ArrowRight,
  Check,
  ChevronDown,
  CircleHelp,
  FlaskConical,
  ImagePlus,
  Layers3,
  Link2,
  LoaderCircle,
  Plus,
  Settings2,
  Sparkles,
  WandSparkles,
  X,
} from "lucide-react";
import "./style.css";
import { ModelDownloads, ModelSettings } from "./ModelDownloads";

type Media = { url: string; sha256: string; bytes: number };
type Recipe = {
  fields: Record<string, string | number | null>;
  unknown: string[];
  provenance: Record<string, string>;
  resources: {
    name: string;
    type: string;
    version_id: string | number | null;
    hash: string | null;
    status: string;
    version_name?: string | null;
    files?: { id?: number; name?: string; sizeKB?: number; hashes?: Record<string, string> }[];
  }[];
};
type ImportRecord = {
  id: string;
  title: string;
  demo: boolean;
  created_at: string;
  media: Media | null;
  image: { width: number; height: number } | null;
  source: { kind: string; url?: string };
  raw: unknown;
  raw_json?: string;
  recipe: Recipe;
  warning: string | null;
  reproduction?: { status: string; blockers: string[] };
};
type Job = {
  id: string;
  import_id: string;
  status: string;
  message: string;
  output: Media | null;
  engine: string;
  image?: { width: number; height: number };
};

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api${path}`, init);
  const data = await res.json();
  if (!res.ok)
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "This request could not be completed.",
    );
  return data;
}

function App() {
  const [items, setItems] = useState<ImportRecord[]>([]);
  const [selected, setSelected] = useState<ImportRecord | null>(null);
  const [url, setUrl] = useState("");
  const [gpu, setGpu] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [seed, setSeed] = useState("42");
  const [modelHash, setModelHash] = useState("");
  const [availableModels, setAvailableModels] = useState<{ sha256: string; name: string; role: string; base_model: string }[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [health, setHealth] = useState<"connecting" | "online" | "offline">(
    "connecting",
  );
  const [job, setJob] = useState<Job | null>(null);
  const [panel, setPanel] = useState<"settings" | "help" | null>(null);
  const [tab, setTab] = useState<"recipe" | "result">("recipe");
  const [drag, setDrag] = useState(false);
  const file = useRef<HTMLInputElement>(null);
  const loadEpoch = useRef(0);
  const modal = useRef<HTMLElement>(null);

  useEffect(() => {
    if (!panel) return;
    const previous = document.activeElement as HTMLElement | null;
    const buttons = modal.current?.querySelectorAll<HTMLElement>(
      "button, a[href], input",
    );
    buttons?.[0]?.focus();
    function keydown(event: KeyboardEvent) {
      if (event.key === "Escape") setPanel(null);
      if (event.key === "Tab" && buttons?.length) {
        const first = buttons[0],
          last = buttons[buttons.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        }
        if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    }
    document.addEventListener("keydown", keydown);
    return () => {
      document.removeEventListener("keydown", keydown);
      previous?.focus();
    };
  }, [panel]);

  async function refresh() {
    setItems(await api<ImportRecord[]>("/imports"));
    setAvailableModels(await api("/models"));
  }
  useEffect(() => {
    api<{ engine: string }>("/health")
      .then((status) => { setHealth("online"); setGpu(status.engine === "comfy"); })
      .catch(() => setHealth("offline"));
    refresh().catch(() =>
      setError(
        "The local service is unavailable. Start Remixfun and reload this page.",
      ),
    );
  }, []);
  useEffect(() => {
    if (!job || !["queued", "running"].includes(job.status)) return;
    let disposed = false;
    const timer = setInterval(() => {
      api<Job>(`/jobs/${job.id}`)
        .then((next) => {
          if (!disposed) {
            setJob(next);
            if (next.status === "completed") setTab("result");
          }
        })
        .catch(() => {
          if (!disposed)
            setError(
              "Connection lost. This job is saved; reopen the image to check its status.",
            );
        });
    }, 500);
    return () => {
      disposed = true;
      clearInterval(timer);
    };
  }, [job?.id, job?.status]);

  async function open(item: ImportRecord) {
    const epoch = ++loadEpoch.current;
    setSelected(item);
    setJob(null);
    setError("");
    setTab("recipe");
    try {
      const jobs = await api<Job[]>("/jobs");
      if (epoch === loadEpoch.current)
        setJob(jobs.find((j) => j.import_id === item.id) || null);
    } catch {
      if (epoch === loadEpoch.current)
        setError(
          "Saved results could not be loaded. Reopen this image to retry.",
        );
    }
  }
  async function importSource(demo = false, upload?: File) {
    setBusy(true);
    setError("");
    try {
      let record: ImportRecord;
      if (upload) {
        const body = new FormData();
        body.append("file", upload);
        record = await api("/imports/file", { method: "POST", body });
      } else
        record = await api(demo ? "/demo" : "/imports", {
          method: "POST",
          ...(demo
            ? {}
            : {
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
              }),
        });
      await refresh();
      await open(record);
      setUrl("");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
      if (file.current) file.current.value = "";
    }
  }
  async function reproduce() {
    if (!selected) return;
    setBusy(true);
    setError("");
    try {
      setJob(
        await api(`/imports/${selected.id}/reproduce`, { method: "POST" }),
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function createRecipe() {
    setBusy(true);
    setError("");
    try {
      const record = await api<ImportRecord>("/recipes", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, seed, model_sha256: modelHash || null }),
      });
      await refresh();
      await open(record);
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }
  const running = job && ["queued", "running"].includes(job.status);
  const fields = selected?.recipe.fields;
  const authored = selected?.source.kind === "authored";
  const displayedMedia = tab === "result" && job?.output ? job.output : selected?.media;

  return (
    <div className="app">
      <aside className="sidebar">
        <button
          className="brand"
          onClick={() => {
            ++loadEpoch.current;
            setSelected(null);
            setError("");
          }}
          aria-label="Remixfun home"
        >
          <span className="brand-mark">
            <Layers3 size={23} />
          </span>
          remixfun<span className="brand-dot">.</span>
        </button>
        <div className="workspace-label">YOUR WORKSPACE</div>
        <button
          className={`nav-item ${!selected ? "active" : ""}`}
          onClick={() => {
            ++loadEpoch.current;
            setSelected(null);
            setError("");
          }}
        >
          <ImagePlus size={18} />
          Import & create
          <Plus size={16} className="push" />
        </button>
        <div className="sidebar-section">
          <span>LIBRARY</span>
          <span>{items.length.toString().padStart(2, "0")}</span>
        </div>
        {items.length === 0 ? (
          <p className="empty-library">
            A home for your images.
            <br />
            Your imports will appear here.
          </p>
        ) : (
          <div className="library">
            {items.map((item) => (
              <button
                className={`library-item ${selected?.id === item.id ? "chosen" : ""}`}
                key={item.id}
                onClick={() => open(item)}
              >
                {item.media ? (
                  <img src={item.media.url} alt="" />
                ) : (
                  <span className="library-placeholder">
                    <ImagePlus size={18} />
                  </span>
                )}
                <span>
                  <strong>{item.title}</strong>
                  <small>
                    {item.demo ? "Demo collection" : item.source.kind === "authored" ? "Generation recipe" : "Imported recipe"}
                  </small>
                </span>
              </button>
            ))}
          </div>
        )}
        <div className="sidebar-bottom">
          <div className="local-card">
            <span className={`status-dot ${health}`} />
            <div>
              <strong>
                {health === "online"
                  ? "Local workspace"
                  : health === "connecting"
                    ? "Connecting…"
                    : "Service offline"}
              </strong>
              <small>Your library stays on this device</small>
            </div>
          </div>
          <button
            className="nav-item subtle"
            onClick={() => setPanel("settings")}
          >
            <Settings2 size={18} />
            Settings
          </button>
          <button className="nav-item subtle" onClick={() => setPanel("help")}>
            <CircleHelp size={18} />A little guidance
            <span className="push">↗</span>
          </button>
          <div className="version">
            LOCAL PREVIEW <span>v0.1.0</span>
          </div>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace</span>
            <span className="slash">/</span>
            {selected ? "Image recipe" : "Import & create"}
          </div>
          <span className="preview-badge">
            <FlaskConical size={13} />
            Early preview
          </span>
        </header>
        {error && (
          <div className="error" role="alert">
            <span>{error}</span>
            <button aria-label="Dismiss error" onClick={() => setError("")}>
              <X size={18} />
            </button>
          </div>
        )}
        {!selected ? (
          <div className="home">
            <div className="eyebrow">
              <span />
              FROM A LITTLE INSPIRATION
            </div>
            <h1>
              Your next idea
              <br />
              starts with an image<span>.</span>
            </h1>
            <p className="lead">
              Bring an image you love. Discover its recipe.
              <br />
              Make room for what comes next.
            </p>
            <section
              className={`import-box ${drag ? "dragging" : ""}`}
              onDragOver={(e) => {
                e.preventDefault();
                setDrag(true);
              }}
              onDragLeave={() => setDrag(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDrag(false);
                if (!busy && e.dataTransfer.files[0])
                  importSource(false, e.dataTransfer.files[0]);
              }}
            >
              <div className="import-heading">
                <span className="square-icon">
                  <Link2 size={20} />
                </span>
                <div>
                  <h2>Start with a Civitai image</h2>
                  <p>We’ll keep its original recipe and source together.</p>
                </div>
              </div>
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  importSource();
                }}
              >
                <label className="sr-only" htmlFor="source-url">
                  Civitai image URL
                </label>
                <input
                  id="source-url"
                  placeholder="https://civitai.com/images/…"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  disabled={busy}
                />
                <button className="primary" disabled={busy || !url.trim()}>
                  {busy ? (
                    <LoaderCircle className="spin" size={17} />
                  ) : (
                    <>
                      Import image
                      <ArrowRight size={17} />
                    </>
                  )}
                </button>
              </form>
              <div className="upload-line">
                <span>or drop an original image here</span>
                <span className="dot-separator">·</span>
                <button onClick={() => file.current?.click()} disabled={busy}>
                  Choose a file <ArrowDownToLine size={13} />
                </button>
                <small>PNG, JPG, WebP · up to 25 MB</small>
              </div>
            </section>
            {gpu && <section className="import-box create-box">
              <h2>Create an image on your GPU</h2>
              <p>SDXL Base 1.0 · a new recipe with a verified model file.</p>
              <form onSubmit={(e) => { e.preventDefault(); createRecipe(); }}>
                <label htmlFor="create-prompt">Describe your image</label>
                <textarea id="create-prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)}
                  maxLength={10000} placeholder="A quiet alpine lake at sunrise…" disabled={busy} required />
                <details className="advanced">
                  <summary>Generation settings <ChevronDown size={16} /></summary>
                  <p>1024 × 1024 · 25 steps · guidance 7 · Euler / normal · empty negative prompt</p>
                  <label htmlFor="create-seed">Seed</label>
                  <input id="create-seed" value={seed} onChange={(e) => setSeed(e.target.value)} inputMode="numeric" pattern="[0-9]{1,20}" />
                  <label htmlFor="create-model">Checkpoint for this new recipe</label>
                  <select id="create-model" value={modelHash} onFocus={() => api<typeof availableModels>("/models").then(setAvailableModels).catch(() => {})}
                    onChange={e => setModelHash(e.target.value)}>
                    <option value="">SDXL Base 1.0 · preset checkpoint</option>
                    {availableModels.filter(m => m.role === "checkpoint" && m.base_model === "SDXL 1.0").map(m =>
                      <option key={m.sha256} value={m.sha256}>{m.name} · verified</option>)}
                  </select>
                </details>
                <button className="primary" disabled={busy || !prompt.trim()}>Create recipe <ArrowRight size={17} /></button>
              </form>
            </section>}
            <section className="demo-card">
              <div className="demo-image">
                <div className="mini-landscape">
                  <div className="sun" />
                  <div className="mountain back" />
                  <div className="mountain front" />
                  <div className="water" />
                </div>
              </div>
              <div className="demo-copy">
                <span className="eyebrow">TAKE A LOOK AROUND</span>
                <h2>A quiet place to start.</h2>
                <p>
                  Explore a saved recipe and the result flow
                  <br />
                  with our illustrated demo. No models needed.
                </p>
              </div>
              <button
                className="secondary"
                onClick={() => importSource(true)}
                disabled={busy}
              >
                Open demo
                <ArrowRight size={16} />
              </button>
            </section>
            <div className="journey">
              <div>
                <span className="step-number current">01</span>
                <strong>Import</strong>
                <p>Keep the source & recipe</p>
              </div>
              <div>
                <span className="step-number">02</span>
                <strong>Reproduce</strong>
                <p>Find your starting point</p>
              </div>
              <div>
                <span className="step-number">03</span>
                <strong>Remix</strong>
                <p>Follow a different idea</p>
              </div>
              <div>
                <span className="step-number">04</span>
                <strong>Animate</strong>
                <p>Give it a little motion</p>
              </div>
            </div>
            {items.length > 0 && (
              <section className="compact-library" aria-label="Saved images">
                <h2>Your saved images</h2>
                {items.map((item) => (
                  <button
                    className="library-item"
                    key={item.id}
                    onClick={() => open(item)}
                  >
                    {item.media && <img src={item.media.url} alt="" />}
                    <span>
                      <strong>{item.title}</strong>
                      <small>
                        {item.demo ? "Demo collection" : item.source.kind === "authored" ? "Generation recipe" : "Imported recipe"}
                      </small>
                    </span>
                    <ArrowRight size={15} className="push" />
                  </button>
                ))}
              </section>
            )}
            <p className="preview-note">
              Available now: recipe import, saved library, and a demo result
              flow.
              <br />
              {gpu ? "SDXL generation is connected. Imported-source reproduction, remixing and animation need further integration." :
                "Configure a local SDXL runtime to generate new images. Imported-source reproduction, remixing and animation are coming next."}
            </p>
          </div>
        ) : (
          <div className="detail">
            <button
              className="back-button"
              onClick={() => {
                ++loadEpoch.current;
                setSelected(null);
              }}
            >
              <ArrowLeft size={15} />
              Back to workspace
            </button>
            <div className="detail-heading">
              <div>
                <div className="eyebrow">
                  {selected.demo ? "ILLUSTRATED DEMO" : authored ? "NEW IMAGE RECIPE" : "SAVED IMPORT"}
                </div>
                <h1>{selected.title}</h1>
              </div>
              <a
                className="icon-button"
                href={`/api/imports/${selected.id}/manifest`}
                title="Export recipe"
                aria-label="Export recipe"
              >
                <ArrowDownToLine size={18} />
              </a>
            </div>
            <div className="detail-grid">
              <section className="image-column">
                <div className="image-stage">
                  {displayedMedia ? (
                    <img
                      src={displayedMedia.url}
                      alt={selected.title}
                    />
                  ) : (
                    <div className="no-preview">
                      <ImagePlus size={42} />
                      <p>{authored ? "Your image will appear here" : "Source preview unavailable"}</p>
                      <small>{authored ? "Review the recipe, then generate." : "The recovered recipe is saved."}</small>
                    </div>
                  )}
                  <span className="image-label">
                    {tab === "result"
                      ? job?.engine === "comfy" ? "GENERATED OUTPUT · SDXL" : "DEMO OUTPUT · SAMPLE REUSED"
                      : selected.demo
                        ? "SAMPLE ILLUSTRATION"
                        : authored ? "NEW RECIPE" : "SOURCE IMAGE"}
                  </span>
                </div>
                <div className="image-caption">
                  <span>
                    {tab === "result" && job?.image ? `${job.image.width} × ${job.image.height}` : selected.image
                      ? `${selected.image.width} × ${selected.image.height}`
                      : "Dimensions unknown"}
                  </span>
                  <span>
                    <Check size={13} />
                    Saved locally
                  </span>
                </div>
                {selected.source.url && (
                  <a
                    className="source-link"
                    href={selected.source.url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    View original on Civitai ↗
                  </a>
                )}
              </section>
              <section className="recipe-column">
                <div className="tabs">
                  <button
                    className={tab === "recipe" ? "selected" : ""}
                    onClick={() => setTab("recipe")}
                  >
                    Source recipe
                  </button>
                  <button
                    className={tab === "result" ? "selected" : ""}
                    disabled={!job}
                    onClick={() => setTab("result")}
                  >
                    Result{" "}
                    {job?.status === "completed" && (
                      <span className="tiny-dot" />
                    )}
                  </button>
                </div>
                {tab === "recipe" ? (
                  <>
                    <div className="recipe-intro">
                      <span className="round-icon">
                        <Layers3 size={16} />
                      </span>
                      <div>
                        <strong>Every image has a starting point.</strong>
                        <p>
                          {selected.demo
                            ? "An example recipe, paired with an authored illustration."
                            : authored ? "A new SDXL recipe. Its settings and model identity are saved." : "Recovered values stay separate from anything you change."}
                        </p>
                      </div>
                    </div>
                    <div className="field-label">
                      PROMPT
                      <span>
                        {fields?.prompt == null ? "Not found" : "Preserved"}
                      </span>
                    </div>
                    <p className="prompt">
                      {fields?.prompt ??
                        "No text prompt was found in the source metadata."}
                    </p>
                    <div className="stats">
                      {[
                        [
                          "Size",
                          fields?.width && fields?.height
                            ? `${fields.width} × ${fields.height}`
                            : null,
                        ],
                        ["Steps", fields?.steps],
                        ["Guidance", fields?.cfg],
                      ].map(([label, value]) => (
                        <div key={label}>
                          <span>{label}</span>
                          <strong>{value ?? "Unknown"}</strong>
                        </div>
                      ))}
                    </div>
                    {!selected.demo && !authored ? <ModelDownloads importId={selected.id} /> : <><div className="section-heading">
                      <h3>Model dependencies</h3>
                      <span>{selected.recipe.resources.length || "—"}</span>
                    </div>
                    {selected.recipe.resources.length ? (
                      selected.recipe.resources.map((resource, i) => (
                        <div className="model-card" key={i}>
                          <span className="square-icon">
                            <Layers3 size={19} />
                          </span>
                          <div>
                            <strong>{resource.name}</strong>
                            {resource.version_name && <small>{resource.version_name}</small>}
                            <small>
                              {resource.type}
                              {authored ? " · SHA-256 pinned" : resource.version_id
                                ? ` · Version ${resource.version_id}`
                                : " · Exact file unresolved"}
                            </small>
                          </div>
                          <span className="tag">
                            {selected.demo ? "Demo" : authored ? "Pinned" : "Unresolved"}
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className="muted-box">
                        No exact model identity was recovered. Model names alone
                        do not establish matching bytes.
                      </p>
                    )}
                    </>}
                    <details className="advanced">
                      <summary>
                        Source details & advanced
                        <ChevronDown size={16} />
                      </summary>
                      <dl>
                        {Object.entries(fields || {})
                          .filter(([key]) => key !== "prompt")
                          .map(([key, value]) => (
                            <React.Fragment key={key}>
                              <dt>{key.replaceAll("_", " ")}</dt>
                              <dd>{value ?? "Unknown"}</dd>
                            </React.Fragment>
                          ))}
                      </dl>
                      {selected.recipe.resources.some(resource => resource.files?.length) && <>
                        <h4>Provider model files · local bytes unverified</h4>
                        <pre>{JSON.stringify(selected.recipe.resources.map(resource => ({
                          name: resource.name, version: resource.version_id, files: resource.files,
                        })), null, 2)}</pre>
                      </>}
                      <h4>Original evidence</h4>
                    <pre>{selected.raw_json ?? JSON.stringify(selected.raw, null, 2)}</pre>
                      {selected.media && (
                        <>
                          <h4>Source SHA-256</h4>
                          <code className="hash">{selected.media.sha256}</code>
                        </>
                      )}
                    </details>
                    {selected.warning && (
                      <p className="notice">{selected.warning}</p>
                    )}
                    <button
                      className="primary generate"
                      disabled={busy || !!running || (!selected.demo && !(authored && gpu))}
                      onClick={reproduce}
                    >
                      {running ? (
                        <>
                          <LoaderCircle size={17} className="spin" />
                          {selected.demo ? "Preparing demo…" : "Generating…"}
                        </>
                      ) : (
                        <>
                          <WandSparkles size={17} />
                          {selected.demo
                            ? "Run demo preview"
                            : authored && gpu ? "Generate image" : "Reproduction unavailable"}
                          <ArrowRight size={16} />
                        </>
                      )}
                    </button>
                    <p className="honesty">
                      {selected.demo
                        ? "Uses the sample illustration. No model runs or reproduction claims."
                        : authored ? "Runs SDXL on your GPU. No source-match claim is made." : "Your original settings and model identities remain unchanged."}
                    </p>
                  </>
                ) : (
                  <div className="result-panel">
                    <span className="result-icon">
                      {job?.status === "completed" ? (
                        <Check size={26} />
                      ) : running ? (
                        <LoaderCircle size={26} className="spin" />
                      ) : (
                        <CircleHelp size={26} />
                      )}
                    </span>
                    <div className="eyebrow">
                      {job?.status === "completed"
                        ? job?.engine === "comfy" ? "IMAGE GENERATED" : "FLOW VERIFIED"
                        : job?.status?.toUpperCase()}
                    </div>
                    <h2>
                      {job?.status === "completed"
                        ? "A starting point, saved."
                        : running
                          ? "Preparing your preview."
                          : "The job stopped."}
                    </h2>
                    <p>{job?.message}</p>
                    <div className="result-facts">
                      <div>
                        <span>Engine</span>
                        <strong>{job?.engine === "comfy" ? "Comfy · SDXL on GPU" : "Demo · no GPU"}</strong>
                      </div>
                      <div>
                        <span>Source recipe</span>
                        <strong>Preserved</strong>
                      </div>
                      <div>
                        <span>Source match</span>
                        <strong>Not evaluated</strong>
                      </div>
                    </div>
                    <p className="notice">
                      {job?.engine === "comfy" ? "The generated image and its workflow are saved locally. This is a new image; matching an imported source has not been evaluated." :
                        "This demo reuses an illustration. Configure the SDXL runtime to generate new images on your GPU."}
                    </p>
                    {job?.output && <a className="secondary" href={job.output.url} download="remixfun-generated.png">Download image <ArrowDownToLine size={16} /></a>}
                    <button
                      className="secondary"
                      onClick={() => setTab("recipe")}
                    >
                      Return to recipe
                      <ArrowRight size={15} />
                    </button>
                  </div>
                )}
              </section>
            </div>
          </div>
        )}
        <input
          type="file"
          ref={file}
          className="sr-only"
          accept="image/png,image/jpeg,image/webp"
          aria-label="Import image file"
          onChange={(e) => {
            if (e.target.files?.[0]) importSource(false, e.target.files[0]);
          }}
        />
      </main>
      {panel && (
        <div className="modal-backdrop" onClick={() => setPanel(null)}>
          <section
            className="modal"
            ref={modal}
            role="dialog"
            aria-modal="true"
            aria-labelledby="panel-title"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="modal-close icon-button"
              aria-label="Close dialog"
              onClick={() => setPanel(null)}
            >
              <X size={20} />
            </button>
            <span className="square-icon">
              {panel === "settings" ? <Settings2 /> : <Sparkles />}
            </span>
            <h2 id="panel-title">
              {panel === "settings"
                ? "A local-first workspace."
                : "Start with the source."}
            </h2>
            {panel === "settings" ? (
              <>
                <p>
                  Recipes and images are saved in your device’s Remixfun
                  application-data folder. Closing the browser keeps the
                  independent service running.
                </p>
                <div className="result-facts">
                  <div>
                    <span>Service</span>
                    <strong>{health}</strong>
                  </div>
                  <div>
                    <span>Network access</span>
                    <strong>Local only</strong>
                  </div>
                  <div>
                    <span>Generation runtime</span>
                    <strong>{gpu ? "Comfy · SDXL" : "Not connected"}</strong>
                  </div>
                </div>
                <ModelSettings />
              </>
            ) : (
              <>
                <p>
                  Paste a public Civitai image URL, or choose an original PNG
                  with generation metadata. Remixfun saves the recipe and keeps
                  missing settings visible.
                </p>
                <p>
                  If Civitai denies access, upload the original image. Try the
                  illustrated demo to explore a complete saved-result flow
                  without downloading models.
                </p>
                <p className="notice">
                  A similar-looking image is not an exact reproduction. This
                  preview does not generate images.
                </p>
              </>
            )}
          </section>
        </div>
      )}
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
