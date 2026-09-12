"""Render authored research with frozen metrics; never runs reference software."""
from pathlib import Path
from datetime import datetime
from urllib.parse import quote, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT.parent / 'references'
INDEX = []


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def dossier(slug, name, license, platforms, distribution, fit, sources, body):
    evidence = json.loads((ROOT / 'research/evidence' / (slug + '.json')).read_text(encoding='utf-8'))
    gh = evidence.get('github', {})
    captured = datetime.fromisoformat(evidence['collected_at'])
    created = gh.get('created_at')
    age = ((captured - datetime.fromisoformat(created.replace('Z', '+00:00'))).days if created else None)
    repo_url = 'https://github.com/' + evidence['repo']
    hist = evidence['contributors_all']
    recent = evidence['contributors_90d']
    def metric(k):
        v = gh.get(k)
        return f'{v:,}' if isinstance(v, int) else ('unavailable' if v is None else str(v))
    rows = [
        ('Snapshot', evidence['collected_at']),
        ('Repository creation / age', f'{created[:10]} / {age:,} days (about {age / 365.25:.2f} years)' if created else 'Public API unavailable; see local history below'),
        ('Oldest reachable commit', evidence['oldest_reachable_commit'] + ' — can include inherited history'),
        ('Stars / forks / subscribers', ' / '.join(metric(k) for k in ['stargazers_count', 'forks_count', 'subscribers_count'])),
        ('Open issues + PRs', metric('open_issues_count') + ' (GitHub combined count)'),
        ('Archived on GitHub', str(gh.get('archived', 'unavailable'))),
        ('Inspected branch / HEAD', f"{evidence['branch']} / `{evidence['head']}`"),
        ('HEAD commit', evidence['latest_commit']),
        ('Reachable commits, including merges', f"{evidence['commit_count']:,}"),
        ('Historical distinct author names', f"{hist['distinct_author_names']:,}"),
        ('Last 90 days: nonmerge commits / author names', f"{recent['nonmerge_commits']:,} / {recent['distinct_author_names']:,}"),
        ('Source license assessment', license),
        ('Operating systems / hardware scope', platforms),
        ('Distribution model', distribution),
        ('Fit for Remixfun', fit),
    ]
    text = f'# {name}\n\n'
    text += f'[Landscape](../LANDSCAPE.md) · [Repository]({repo_url}) · [Local clone](../../../references/{slug}/) · [Raw snapshot](../evidence/{slug}.json)\n\n'
    text += '> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.\n\n'
    text += '## Repository, popularity, age, and maintenance\n\n| Signal | Evidence |\n|---|---|\n'
    text += '\n'.join(f'| {cell(k)} | {cell(v)} |' for k, v in rows) + '\n\n'
    text += 'Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).\n\n'
    text += '### Contributors visible in this history\n\n| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |\n|---|---:|---|---:|\n'
    for i in range(max(min(len(hist['top']), 5), min(len(recent['top']), 5))):
        a = hist['top'][i] if i < len(hist['top']) else {}
        b = recent['top'][i] if i < len(recent['top']) else {}
        text += f"| {cell(a.get('name', '—'))} | {a.get('commits', '—')} | {cell(b.get('name', '—'))} | {b.get('commits', '—')} |\n"
    text += '\n### Release evidence\n\n'
    if evidence.get('releases'):
        text += 'The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.\n\n| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |\n|---|---|---|\n'
        for rel in evidence['releases']:
            files = [unquote(a.rsplit('/', 1)[-1]) for a in rel.get('assets', [])]
            sample = ', '.join(f'`{x}`' for x in files[:7]) or 'No attached artifacts in captured expansion; check external distribution'
            if len(files) > 7:
                sample += f"; +{len(files)-7} more in snapshot"
            text += f"| [{cell(rel['title'])}]({rel['url']}) | {rel['updated']} | {cell(sample)} |\n"
    else:
        text += 'No GitHub release entries were captured. This does not exclude registry packages, git installation, external installers, or a private release process.\n'
    if evidence['errors']:
        text += '\nCollection limitations: ' + '; '.join(cell(e) for e in evidence['errors']) + '.\n'
    text += '\n' + body.strip() + '\n\n## Source map and citations\n\n'
    mapped = []
    for i, source in enumerate(sources, 1):
        path, purpose = source
        if path.startswith('https://'):
            text += f'[^s{i}]: [{purpose}]({path}), accessed 2026-09-12.\n\n'
            mapped.append({'path': path, 'purpose': purpose})
        else:
            target = REFS / slug / path
            if not target.exists():
                raise FileNotFoundError(f'{slug}: {path}')
            kind = 'tree' if target.is_dir() else 'blob'
            url = f"{repo_url}/{kind}/{evidence['head']}/{quote(path, safe='/')}"
            local = '../../../references/' + slug + '/' + quote(path, safe='/')
            remote = f'[Pinned source]({url})' if gh else 'Local-only baseline; public URL not verified'
            text += f'[^s{i}]: **{purpose}** — {remote}; [local {path}]({local}).\n\n'
            mapped.append({'path': path, 'purpose': purpose, 'url': url if gh else None})
    (ROOT / 'research/projects' / (slug + '.md')).write_text(text.rstrip() + '\n', encoding='utf-8')
    INDEX.append({'slug': slug, 'name': name, 'license': license, 'platforms': platforms,
                  'distribution': distribution, 'fit': fit, 'sources': mapped})


def finish():
    (ROOT / 'research/source-map.json').write_text(json.dumps(INDEX, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    text = '# Repository comparison matrix\n\nSnapshot: 2026-09-12. Figures come from the linked evidence files; definitions and limits are in [METHODOLOGY.md](METHODOLOGY.md). Dates and activity refer to the inspected branch, not necessarily the latest shipped product. Full contributor names, release samples, architecture, and citations are in each dossier.\n\n'
    text += '| Project | Created | Stars | Forks | Author names: history / 90d | Nonmerge commits: 90d | HEAD date | Archived |\n|---|---|---:|---:|---:|---:|---|---|\n'
    for item in INDEX:
        d = json.loads((ROOT / 'research/evidence' / (item['slug'] + '.json')).read_text(encoding='utf-8'))
        g = d.get('github', {})
        text += f"| [{item['name']}](projects/{item['slug']}.md) | {(g.get('created_at') or 'unknown')[:10]} | {g.get('stargazers_count','—')} | {g.get('forks_count','—')} | {d['contributors_all']['distinct_author_names']} / {d['contributors_90d']['distinct_author_names']} | {d['contributors_90d']['nonmerge_commits']} | {d['latest_commit'][:10]} | {g.get('archived','unknown')} |\n"
    text += '\n## License, platform, and distribution\n\nThese are software-source assessments. Models, bundled components, paid services, and branded binaries can have additional terms. “Cross-platform” never implies every model and GPU combination works.\n\n| Project | Source license | OS / hardware | Distribution | Role |\n|---|---|---|---|---|\n'
    for x in INDEX:
        text += f"| [{x['name']}](projects/{x['slug']}.md) | {cell(x['license'])} | {cell(x['platforms'])} | {cell(x['distribution'])} | {cell(x['fit'])} |\n"
    (ROOT / 'research/REPOSITORY-MATRIX.md').write_text(text, encoding='utf-8')
    project_index = '# Project dossiers\n\n28 source and architecture reviews, captured 2026-09-12. Each dossier includes popularity/age, historical and recent contributors, release evidence, OS/runtime distinctions, license findings, architecture, workflow coverage, and comparison with Dreamtime.\n\n'
    project_index += '| Project | Role in this survey |\n|---|---|\n'
    for x in INDEX:
        project_index += f"| [{x['name']}](projects/{x['slug']}.md) | {cell(x['fit'])} |\n"
    project_index += '\nStart with the [landscape synthesis](LANDSCAPE.md), then use the [repository matrix](REPOSITORY-MATRIX.md) to compare metrics and distribution. Source evidence is linked within each dossier.\n'
    (ROOT / 'research/PROJECTS.md').write_text(project_index, encoding='utf-8')
    refs = '# Remixfun research references\n\n28 source references acquired on 2026-09-12. Main report: [Remixfun landscape](../remixfun/research/LANDSCAPE.md). These are research checkouts; their programs, installers, and model downloads have not been run.\n\nPublic clones keep default-branch history using Git blob filtering. LFS payloads and submodules were not fetched. Dreamtime and Desktop Release Kit were cloned from the existing local repositories. Existing originals were not modified.\n\n| Clone | Research dossier | Upstream |\n|---|---|---|\n'
    for x in INDEX:
        d = json.loads((ROOT / 'research/evidence' / (x['slug'] + '.json')).read_text(encoding='utf-8'))
        refs += f"| [{x['slug']}]({x['slug']}/) | [{x['name']}](../remixfun/research/projects/{x['slug']}.md) | [{d['repo']}](https://github.com/{d['repo']}) |\n"
    refs += '\nUse [collect_landscape.py](../remixfun/scripts/collect_landscape.py) to collect new evidence deliberately. It does not update existing checkouts; fetch/checkout a new revision explicitly when a new review is intended. Preserve the existing dated evidence before refreshing it.\n'
    (REFS / 'README.md').write_text(refs, encoding='utf-8')
    print(f'Wrote {len(INDEX)} dossiers, source map, matrix, and reference index.')
