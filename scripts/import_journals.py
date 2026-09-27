"""Import publicly served journal PDFs and original covers linked by the old website."""
from pathlib import Path
import sys,json,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'.tools'))
from bs4 import BeautifulSoup
import requests
source=ROOT/'content/source';out=ROOT/'docs/assets/journals';out.mkdir(parents=True,exist_ok=True)
page=next(p for p in json.loads((source/'pages.json').read_text(encoding='utf-8')) if p['id']==951)
soup=BeautifulSoup(page['content']['rendered'],'html.parser');items=[]
for frame in soup.find_all('iframe'):
    u=frame['src'];slug=Path(u).stem;item={'url':u,'title':str(frame.previous_sibling).strip()}
    r=requests.get(u,timeout=40);r.raise_for_status();s=BeautifulSoup(r.text,'html.parser')
    cover=s.find('meta',attrs={'property':'og:image'})
    match=re.search(r"heyzine\.load\('([^']+)'",r.text)
    for kind,remote,suffix in [('cover',cover.get('content') if cover else None,'.jpg'),('pdf',match.group(1) if match else None,'.pdf')]:
        if not remote:continue
        try:
            f=requests.get(remote,timeout=60);f.raise_for_status()
            if kind=='pdf' and not f.content.startswith(b'%PDF'):raise ValueError('Not a PDF')
            (out/(slug+suffix)).write_bytes(f.content);item[kind]='assets/journals/'+slug+suffix
            print(slug,kind,len(f.content),flush=True)
        except Exception as e:item[kind+'_error']=str(e);print(slug,kind,'unavailable',flush=True)
    items.append(item)
(source/'journals.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
