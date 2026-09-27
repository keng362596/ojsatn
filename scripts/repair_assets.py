from pathlib import Path
import json,hashlib,requests
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'content/source/assets.json'
assets=json.loads(P.read_text(encoding='utf-8'))
report=json.loads((P.parent/'migration-report.json').read_text(encoding='utf-8'))
recovered=[]
for item in report['failures']:
    u=item['url']
    if '/blog/wp-content/' not in u: continue
    replacement=u.replace('http:','https:').replace('/blog/wp-content/','/wp-content/')
    try:
        r=requests.get(replacement,timeout=20);r.raise_for_status()
        name=hashlib.sha256(replacement.encode()).hexdigest()[:18]+Path(replacement).suffix
        dest='assets/archive/'+name
        (ROOT/'docs'/dest).write_bytes(r.content)
        assets[u]=dest;assets[replacement]=dest
        recovered.append({'original':u,'replacement':replacement})
        print('Recovered',replacement,flush=True)
    except Exception as e: print('Unavailable',replacement,str(e),flush=True)
P.write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
(P.parent/'recovered-assets.json').write_text(json.dumps(recovered,ensure_ascii=False,indent=2),encoding='utf-8')
