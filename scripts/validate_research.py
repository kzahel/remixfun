"""Validate research artifacts and frozen checkouts without running reference code."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT.parent / 'references'
catalog = json.loads((ROOT / 'research/catalog.json').read_text(encoding='utf-8'))
source_map = json.loads((ROOT / 'research/source-map.json').read_text(encoding='utf-8'))
errors = []
warnings = []
report_path = ROOT / 'research/evidence/validation.json'


def git(args, cwd):
    p = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return p.stdout.strip()


def check_repo(entry):
    slug = entry['slug']
    evidence_path = ROOT / 'research/evidence' / (slug + '.json')
    doc = ROOT / 'research/projects' / (slug + '.md')
    result = {'slug': slug, 'errors': []}
    try:
        evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
        result['head'] = git(['rev-parse', 'HEAD'], REFS / slug)
        result['clean'] = not git(['status', '--porcelain'], REFS / slug)
        result['dossier_words'] = len(doc.read_text(encoding='utf-8').split())
        if result['head'] != evidence['head']:
            result['errors'].append('Checkout HEAD differs from captured source')
        if not result['clean']:
            result['errors'].append('Reference working tree changed')
        if entry.get('local'):
            result['original_clean'] = not git(['status', '--porcelain'], entry['local'])
            if not result['original_clean']:
                result['errors'].append('Original baseline working tree is not clean')
    except Exception as exc:
        result['errors'].append(str(exc))
    return result


with ThreadPoolExecutor(max_workers=4) as pool:
    repos = list(pool.map(check_repo, catalog))
for repo in repos:
    errors.extend(repo['slug'] + ': ' + e for e in repo['errors'])

expected = {x['slug'] for x in catalog}
actual = {x['slug'] for x in source_map}
if expected != actual:
    errors.append(f'Catalog/source map mismatch: {expected ^ actual}')
docs = list((ROOT / 'research/projects').glob('*.md'))
if {p.stem for p in docs} != expected:
    errors.append('Dossier set differs from catalog')

source_count = 0
for item in source_map:
    for source in item['sources']:
        if not source['path'].startswith('https://'):
            source_count += 1
            if not (REFS / item['slug'] / source['path']).exists():
                errors.append(f"Missing cited source: {item['slug']}/{source['path']}")

markdown_files = list(ROOT.rglob('*.md')) + [REFS / 'README.md']
local_links = 0
for path in markdown_files:
    content = path.read_text(encoding='utf-8')
    definitions = set(re.findall(r'^\[\^([^\]]+)\]:', content, re.M))
    uses = set(re.findall(r'\[\^([^\]]+)\](?!:)', content))
    if uses - definitions:
        errors.append(f'{path.name}: undefined footnotes {uses - definitions}')
    for raw in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', content):
        target = raw.strip('<>')
        if target.startswith(('https://', 'http://', 'mailto:', '#')):
            continue
        local_links += 1
        target = unquote(target.split('#', 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if resolved != report_path and not resolved.exists():
            errors.append(f'{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: missing local link {target}')
    for i, line in enumerate(content.splitlines(), 1):
        if line.endswith((' ', '\t')):
            errors.append(f'{path.name}:{i}: trailing whitespace')
    if '\ufffd' in content:
        errors.append(f'{path.name}: replacement character in text')

result = {
    'validated_at': datetime.now(timezone.utc).isoformat(),
    'status': 'passed' if not errors else 'failed',
    'repository_count': len(repos), 'dossier_count': len(docs),
    'markdown_documents': len(markdown_files), 'local_links_checked': local_links,
    'source_paths_checked': source_count,
    'dossier_words_total': sum(x.get('dossier_words', 0) for x in repos),
    'checks': ['catalog/dossier/evidence coverage', 'clone HEAD matches snapshot', 'reference working trees clean',
               'original local baselines clean', 'cited local source paths exist', 'local Markdown link targets exist',
               'footnote definitions present', 'text encoding and whitespace'],
    'not_tested': ['GPU generation', 'installer/runtime execution', 'reference test suites', 'model downloads',
                   'end-to-end competitor usability', 'remote link availability', 'pixel/visual reproducibility'],
    'repositories': repos, 'errors': errors, 'warnings': warnings,
}
report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k != 'repositories'}, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
