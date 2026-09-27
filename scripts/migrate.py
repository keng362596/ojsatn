"""Read-only import of public OJSATN WordPress content and referenced media."""
from pathlib import Path
import sys, json, hashlib, time, re
from urllib.parse import urljoin, urlparse, unquote
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.tools'))
import requests
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'content' / 'source'
ASSETS = ROOT / 'docs' / 'assets' / 'archive'
DATA.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)
BASE = 'https://www.ojsatn.or.th/'
session = requests.Session()
session.headers['User-Agent'] = 'OJSATN-authorized-website-migration/1.0'
def get(url):
    for attempt in range(3):
        try:
            r = session.get(url, timeout=45); r.raise_for_status(); return r
        except Exception:
            if attempt == 2: raise
            time.sleep(1)
def collection(kind):
    out = []; page = 1
    while True:
        r = get(f'{BASE}wp-json/wp/v2/{kind}?per_page=100&page={page}')
        out.extend(r.json())
        if page >= int(r.headers.get('X-WP-TotalPages', 1)): break
        page += 1
    (DATA / f'{kind}.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(kind, len(out), flush=True)
    return out
if __name__ == '__main__':
    all_data = {k:collection(k) for k in ['posts','pages','categories','media']}
    homepage = get(BASE).text
    (DATA/'homepage.html').write_text(homepage, encoding='utf-8')
    urls = set(); links = set()
    for item in all_data['media']:
        if item.get('source_url'): urls.add(item['source_url'])
    for content in [homepage] + [i['content']['rendered'] for k in ['posts','pages'] for i in all_data[k]]:
        soup = BeautifulSoup(content, 'html.parser')
        for el in soup.select('[src], [href], [srcset]'):
            for attr in ['src','href']:
                if el.get(attr):
                    u = urljoin(BASE, el[attr]); links.add(u)
                    if '/wp-content/uploads/' in u: urls.add(u.split('#')[0])
            for v in el.get('srcset','').split(','):
                if v.strip():
                    u = urljoin(BASE,v.strip().split()[0])
                    if '/wp-content/uploads/' in u: urls.add(u)
    manifest_path = DATA / 'assets.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    failures = []
    for n,u in enumerate(sorted(urls)):
        if u in manifest and (ROOT/'docs'/manifest[u]).exists(): continue
        ext = Path(unquote(urlparse(u).path)).suffix.lower()
        if not re.fullmatch(r'\.[a-z0-9]{1,5}', ext): ext = '.bin'
        name = hashlib.sha256(u.encode()).hexdigest()[:18] + ext
        try:
            r = get(u); (ASSETS/name).write_bytes(r.content)
            manifest[u] = 'assets/archive/' + name
        except Exception as e: failures.append({'url':u, 'error':str(e)})
        if n % 30 == 0:
            manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2), encoding='utf-8')
            print('assets',n+1,'/',len(urls),flush=True)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2), encoding='utf-8')
    report = {'counts':{k:len(v) for k,v in all_data.items()},'asset_candidates':len(urls),'downloaded_assets':len(manifest),'failures':failures,'external_links':sorted(u for u in links if urlparse(u).netloc not in ['www.ojsatn.or.th','ojsatn.or.th',''])}
    (DATA/'migration-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='external_links'},ensure_ascii=True),flush=True)
