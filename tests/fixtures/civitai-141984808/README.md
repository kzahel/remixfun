# Live Civitai metadata excerpt

Captured 2026-09-12 using Python httpx with the application's User-Agent;
no browser or page-script execution. Sources:

- https://civitai.com/images/141984808
- https://civitai.com/api/v1/model-versions/128078

`queries.json` retains the two matching image queries from `__NEXT_DATA__`.
The image record is reduced to identity/access fields; user and social data,
unrelated queries, and cache bookkeeping are omitted. The generation record
is preserved. `model-version.json` retains version identity and files, omitting
gallery images and download URLs. These are live excerpts, not synthetic
settings. Tests wrap them in owned HTML and serve an owned PNG as the preview.

The full page and downloaded JPEG remain in ignored local artifacts.
Page capture SHA-256:
`4d2e8489aac6b95271ade5d6b21da98feece483fb30eb94abae054939862e178`.
The source JPEG is not a lossless original or proof of pixel reproduction.
