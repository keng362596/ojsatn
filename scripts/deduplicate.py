"""Remove byte-identical local asset duplicates while preserving every URL mapping."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=(ROOT/'docs/assets/archive').resolve()
manifest=ROOT/'content/source/assets.json';assets=json.loads(manifest.read_text(encoding='utf-8'))
hashes={};replace={};saved=0
for p in sorted(BASE.iterdir()):
    assert p.resolve().is_relative_to(BASE) and p.is_file()
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if digest in hashes:
        canonical=hashes[digest]
        replace['assets/archive/'+p.name]='assets/archive/'+canonical.name
        saved+=p.stat().st_size
    else:hashes[digest]=p
for u,p in assets.items():assets[u]=replace.get(p,p)
manifest.write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
for old in replace:
    p=(ROOT/'docs'/old).resolve()
    assert p.is_relative_to(BASE)
    p.unlink()
print('Removed',len(replace),'byte-identical duplicate files; saved',round(saved/1e6,1),'MB')
