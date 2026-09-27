"""Check generated pages, migrated content, links, images and supplied LINE QR."""
from pathlib import Path
import sys,json
from urllib.parse import urlparse,unquote
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'.tools'))
from bs4 import BeautifulSoup
OUT=ROOT/'docs';errors=[];count=0
for path in OUT.rglob('*.html'):
    count+=1;soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    if not soup.find('html',lang='th'):errors.append(f'{path}: missing Thai lang')
    if not soup.find('meta',attrs={'name':'viewport'}):errors.append(f'{path}: missing viewport')
    if not soup.find('meta',attrs={'http-equiv':'refresh'}) and len(soup.find_all('h1'))!=1:errors.append(f'{path}: expected one h1')
    for el in soup.select('[href],[src]'):
        for attr in ['href','src']:
            u=el.get(attr,'');parsed=urlparse(u)
            if not u or parsed.scheme or parsed.netloc or u.startswith('#'):continue
            target=(path.parent/unquote(parsed.path)).resolve()
            if not target.is_relative_to(OUT.resolve()):errors.append(f'{path}: escapes site {u}')
            elif not target.exists():errors.append(f'{path.relative_to(OUT)}: missing {u}')
    if soup.find('form'):errors.append(f'{path}: unexpected form')
posts=json.loads((ROOT/'content/source/posts.json').read_text(encoding='utf-8'))
for post in posts:
    if not (OUT/f'news/{post["id"]}/index.html').exists():errors.append(f'Missing post {post["id"]}')
committee=BeautifulSoup((OUT/'committee/index.html').read_text(encoding='utf-8'),'html.parser')
assert len(committee.select('.person'))==15
config=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
if config.get('line_url'):
    import zxingcpp
    from PIL import Image
    code=zxingcpp.read_barcodes(Image.open(OUT/'assets/line-qr.png'))
    assert code and code[0].text==config['line_url'],'LINE QR/link mismatch'
result={'checked_html':count,'posts':len(posts),'committee_members':15,'line_qr_matches_link':bool(config.get('line_url')),'errors':errors}
(ROOT/'content/validation-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True,indent=2));sys.exit(bool(errors))
