from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools'))
import pymupdf, requests
OUT=ROOT/'docs/assets'
OUT.mkdir(parents=True,exist_ok=True)
logo=Path(r'C:\Users\keng.h\OneDrive - Aware Corporation Limited\Desktop\OJSATN\วาระ  May 2024 - Apr 2026\Logo\Logo สมาคม สาขาภาคเหนือ .ai')
doc=pymupdf.open(logo)
page=doc[0]
bounds=pymupdf.Rect()
for item in page.get_drawings(): bounds |= item['rect']
bounds &= page.rect
page.set_cropbox(bounds)
(OUT/'logo.svg').write_text(page.get_svg_image(),encoding='utf-8')
page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),alpha=True).save(str(OUT/'logo.png'))
print('Logo crop',bounds)
for name,url in {
    'NotoSansThai.ttf':'https://raw.githubusercontent.com/google/fonts/main/ofl/notosansthai/NotoSansThai%5Bwdth,wght%5D.ttf',
    'NotoSerifThai.ttf':'https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifthai/NotoSerifThai%5Bwdth,wght%5D.ttf',
    'OFL-NotoSansThai.txt':'https://raw.githubusercontent.com/google/fonts/main/ofl/notosansthai/OFL.txt',
    'OFL-NotoSerifThai.txt':'https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifthai/OFL.txt',
}.items():
    r=requests.get(url,timeout=45);r.raise_for_status();(OUT/name).write_bytes(r.content);print(name,len(r.content))
