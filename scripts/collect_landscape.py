"""Clone reference sources and capture public, dated repository evidence.

Does not install packages, run cloned code, fetch model weights, or alter existing
checkouts. Reference clones retain default-branch history, but omit LFS payloads.
No credentials are read. Public GitHub API rate-limit failures are preserved.
"""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT.parent / "references"
EVIDENCE = ROOT / "research" / "evidence"
CATALOG = json.loads((ROOT / "research" / "catalog.json").read_text())
NOW = dt.datetime.now(dt.timezone.utc)
ENV = {**os.environ, "GIT_LFS_SKIP_SMUDGE": "1", "GIT_TERMINAL_PROMPT": "0"}


def run(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, env=ENV, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:])
    return result.stdout.strip()


def fetch(url, is_json=False):
    request = urllib.request.Request(url, headers={"User-Agent": "Remixfun-Landscape-Research",
                                                  "Accept": "application/vnd.github+json" if is_json else "*/*"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read().decode("utf-8", "replace")
        return json.loads(data) if is_json else data


def collect(entry):
    slug, repo = entry["slug"], entry["repo"]
    target = REFERENCES / slug
    result = {**entry, "collected_at": NOW.isoformat(), "path": target.as_posix(), "errors": []}
    try:
        if not target.exists():
            args = ["git", "-c", "core.longpaths=true", "clone", "--single-branch"]
            if "local" in entry:
                args += ["--no-hardlinks", entry["local"], str(target)]
            else:
                args += ["--filter=blob:none", "https://github.com/" + repo + ".git", str(target)]
            run(args)
        result["head"] = run(["git", "rev-parse", "HEAD"], target)
        result["branch"] = run(["git", "branch", "--show-current"], target)
        result["latest_commit"] = run(["git", "log", "-1", "--format=%cI %s"], target)
        result["commit_count"] = int(run(["git", "rev-list", "--count", "HEAD"], target))
        result["shallow"] = run(["git", "rev-parse", "--is-shallow-repository"], target) == "true"
        result["oldest_reachable_commit"] = run(["git", "log", "--format=%aI", "--reverse"], target).splitlines()[0]
        for label, since in [("all", None), ("90d", (NOW - dt.timedelta(days=90)).isoformat())]:
            args = ["git", "shortlog", "-sn", "--no-merges", "HEAD"]
            if since:
                args.append("--since=" + since)
            rows = run(args, target).splitlines()
            people = []
            for row in rows:
                count, name = row.strip().split("\t", 1)
                people.append({"name": name, "commits": int(count)})
            result["contributors_" + label] = {"distinct_author_names": len(people), "top": people[:12],
                                              "nonmerge_commits": sum(x["commits"] for x in people)}
        result["tags"] = run(["git", "tag", "--sort=-creatordate"], target).splitlines()[:15]
        result["dirty"] = run(["git", "status", "--short"], target)
        if "local" in entry:
            result["source_dirty"] = run(["git", "status", "--short"], entry["local"])
    except Exception as exc:
        result["errors"].append("clone/history: " + str(exc))
    try:
        meta = fetch("https://api.github.com/repos/" + repo, True)
        keys = ["full_name", "html_url", "description", "created_at", "updated_at", "pushed_at", "stargazers_count",
                "forks_count", "subscribers_count", "open_issues_count", "archived", "disabled", "fork",
                "default_branch", "language", "license", "homepage", "size", "topics"]
        result["github"] = {key: meta.get(key) for key in keys}
        if meta.get("parent"):
            result["github"]["parent"] = meta["parent"]["full_name"]
    except Exception as exc:
        result["errors"].append("repository API: " + str(exc))
    try:
        atom = fetch("https://github.com/" + repo + "/releases.atom")
        ns = {"a": "http://www.w3.org/2005/Atom"}
        feed = ET.fromstring(atom)
        releases = []
        for node in feed.findall("a:entry", ns)[:5]:
            link = node.find("a:link", ns).attrib["href"]
            item = {"title": node.findtext("a:title", namespaces=ns),
                    "updated": node.findtext("a:updated", namespaces=ns), "url": link,
                    "notes_html": node.findtext("a:content", namespaces=ns)}
            try:
                tag = link.split("/tag/", 1)[1]
                assets = fetch("https://github.com/" + repo + "/releases/expanded_assets/" + tag)
                item["assets"] = sorted(set(html.unescape(x) for x in re.findall(r'href="([^"]*/releases/download/[^"]+)"', assets)))
                item["assets_source"] = "https://github.com/" + repo + "/releases/expanded_assets/" + tag
            except Exception as exc:
                item["asset_error"] = str(exc)
            releases.append(item)
        result["releases"] = releases
    except Exception as exc:
        result["errors"].append("release feed: " + str(exc))
    (EVIDENCE / (slug + ".json")).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(slug + ": " + result.get("head", "CLONE FAILED")[:12] + "; " + str(len(result.get("releases", []))) + " releases; " + str(len(result["errors"])) + " errors", flush=True)
    return result


if __name__ == "__main__":
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    REFERENCES.mkdir(parents=True, exist_ok=True)
    selected = [x for x in CATALOG if len(sys.argv) == 1 or x["slug"] in sys.argv[1:]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(collect, selected))
    print("Finished " + str(len(results)) + " references.", flush=True)
