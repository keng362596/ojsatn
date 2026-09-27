"""Build the complete static site. Run after migrate.py; no server runtime needed."""
from pathlib import Path
import sys,json,re,html,os
from urllib.parse import urlparse,unquote,urljoin,parse_qs
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools'))
from bs4 import BeautifulSoup
OUT=ROOT/'docs';SOURCE=ROOT/'content/source'
def read(name):return json.loads((SOURCE/name).read_text(encoding='utf-8'))
POSTS=read('posts.json');PAGES=read('pages.json');MEDIA={x['id']:x for x in read('media.json')};ASSETS=read('assets.json')
CONFIG=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
COMMITTEE=json.loads((ROOT/'content/committee.json').read_text(encoding='utf-8'))['members']
NAME='สมาคมนักเรียนเก่าญี่ปุ่น ในพระบรมราชูปถัมภ์ สาขาภาคเหนือ'
SHORT='สมาคมนักเรียนเก่าญี่ปุ่นฯ สาขาภาคเหนือ'
MONTHS=['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
CATS={4:'สมาชิกสัมพันธ์',3:'การสอบ JLPT / EJU',5:'เรียนภาษาญี่ปุ่น',6:'สุนทรพจน์ภาษาญี่ปุ่น',1:'ข่าวสมาคม'}
PAGE_PATH={951:'journal/',804:'committee/',88:'about/',32:'school/',90:'contact/',2:'news/'}
URLS={}
for item in POSTS+PAGES:
    dest=PAGE_PATH.get(item['id'],f"news/{item['id']}/") if item in PAGES else f"news/{item['id']}/"
    URLS[unquote(urlparse(item['link']).path).rstrip('/')]=dest
ID_PATH={x['id']:f"news/{x['id']}/" for x in POSTS};ID_PATH.update(PAGE_PATH)
generated=[];broken=[]
def esc(s):return html.escape(str(s),quote=True)
def plain(s):return BeautifulSoup(s,'html.parser').get_text(' ',strip=True)
def date(s):
    d=datetime.fromisoformat(s);return f'{d.day} {MONTHS[d.month-1]} {d.year+543}'
def asset(u):
    for v in [u,u.replace('http:','https:'),u.replace('https:','http:')]:
        if v in ASSETS:return ASSETS[v]
    return None
def photo(fragment):
    return next((p for u,p in ASSETS.items() if u.endswith(fragment)),None)
def rel(path,target):
    parent=Path(path).parent
    return os.path.relpath(target,parent).replace('\\','/')
def link(path,target,label,cls=''):
    return f'<a class="{cls}" href="{esc(rel(path,target))}">{label}</a>'
def img(path,target,alt='',cls='',eager=False):
    return f'<img src="{esc(rel(path,target))}" alt="{esc(alt)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">' if target else ''
def contact_buttons(path):
    line=f'<a class="button light" href="{esc(CONFIG["line_url"])}" target="_blank" rel="noopener noreferrer">LINE</a>' if CONFIG.get('line_url') else ''
    return f'<div class="actions"><a class="button" href="tel:+6653272331">โทร. 053-272-331</a>{line}<a class="button outline" href="https://www.facebook.com/ojsatn" target="_blank" rel="noopener noreferrer">Facebook</a></div>'
def shell(path,title,body,active='',description=None):
    desc=description or 'เชื่อมสัมพันธ์สมาชิก ส่งเสริมภาษาและวัฒนธรรมญี่ปุ่นในภาคเหนือ ข่าวสาร กิจกรรม การสอบ JLPT และ EJU'
    nav=[('index.html','หน้าแรก','home'),('about/','เกี่ยวกับสมาคม','about'),('news/','ข่าวและกิจกรรม','news'),('exams/','การสอบ JLPT / EJU','exams'),('school/','เรียนภาษาญี่ปุ่น','school'),('journal/','วารสาร','journal')]
    items=''.join(f'<a href="{rel(path,u)}" {"aria-current=\"page\"" if active==k else ""}>{t}</a>' for u,t,k in nav)
    content=f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | {SHORT}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#0c2350"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><link rel="icon" href="{rel(path,'assets/logo.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{rel(path,'assets/site.css')}"><script defer src="{rel(path,'assets/site.js')}"></script></head><body>
    <a class="skip" href="#main">ข้ามไปเนื้อหา</a><div class="topline"><div class="wrap"><span>มิตรภาพ • ภาษา • วัฒนธรรม</span><a href="tel:+6653272331">ติดต่อสมาคม &nbsp; 053-272-331</a></div></div>
    <header class="site-header"><div class="wrap identity"><a class="brand" href="{rel(path,'index.html')}">{img(path,'assets/logo.svg','ตราสมาคมนักเรียนเก่าญี่ปุ่นฯ','logo',True)}<span><strong>สมาคมนักเรียนเก่าญี่ปุ่น</strong><span>ในพระบรมราชูปถัมภ์ <i></i> สาขาภาคเหนือ</span></span></a><div class="header-right"><span>สานสัมพันธ์ไทย–ญี่ปุ่น ณ เชียงใหม่</span>{link(path,'contact/','ติดต่อเรา','button small')}</div><button class="menu-toggle" aria-label="เปิดเมนู" aria-controls="navigation" aria-expanded="false">เมนู <span aria-hidden="true">☰</span></button></div><nav id="navigation" aria-label="เมนูหลัก"><div class="wrap nav-inner">{items}{link(path,'contact/','ติดต่อเรา','mobile-contact')}</div></nav></header>
    <main id="main">{body}</main><section class="contact-strip"><div class="wrap"><div><span class="eyebrow">ยินดีต้อนรับสู่สมาคม</span><h2>มาร่วมเป็นส่วนหนึ่งของมิตรภาพ</h2><p>สอบถามเรื่องสมาชิก กิจกรรม การสอบ และการเรียนภาษาญี่ปุ่น</p></div>{contact_buttons(path)}</div></section>
    <footer><div class="wrap footer-grid"><div class="footer-brand">{img(path,'assets/logo.svg','ตราสมาคม','logo')}<div><strong>สมาคมนักเรียนเก่าญี่ปุ่น</strong><p>ในพระบรมราชูปถัมภ์ สาขาภาคเหนือ</p><p>3/3 ถนนสามล้าน ตำบลพระสิงห์<br>อำเภอเมืองเชียงใหม่ จังหวัดเชียงใหม่ 50200</p></div></div><div><h3>รู้จักสมาคม</h3>{link(path,'about/','ประวัติและวิสัยทัศน์')}{link(path,'committee/','คณะกรรมการบริหาร')}{link(path,'journal/','วารสารสมาคม')}</div><div><h3>ติดต่อและติดตาม</h3><a href="tel:+6653272331">053-272-331</a><a href="https://www.facebook.com/ojsatn" target="_blank" rel="noopener noreferrer">Facebook สมาคม</a>{link(path,'contact/','เวลาเปิดทำการและการเดินทาง')}</div></div><div class="wrap footer-bottom"><span>© {datetime.now().year+543} {SHORT}</span><a href="#main">กลับด้านบน</a></div></footer></body></html>'''
    digits=str.maketrans('๐๑๒๓๔๕๖๗๘๙','0123456789')
    rendered=BeautifulSoup(content,'html.parser')
    for text_node in rendered.find_all(string=True):
        if text_node.parent.name not in ['script','style'] and re.search('[๐-๙]',str(text_node)):
            text_node.replace_with(str(text_node).translate(digits))
    content=str(rendered)
    target=OUT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8');generated.append(path)
def heading(path,title,subtitle,kicker='สมาคมนักเรียนเก่าญี่ปุ่นฯ สาขาภาคเหนือ'):
    return f'<section class="page-head"><div class="wrap"><div class="crumb">{link(path,"index.html","หน้าแรก")} <span>/</span> {esc(title)}</div><span class="eyebrow">{kicker}</span><h1>{title}</h1><p>{subtitle}</p></div></section>'
def cat(post):return next((CATS[x] for x in post['categories'] if x in CATS),'ข่าวสมาคม')
def title(post):
    overrides={1149:'ประกาศผลสอบ JLPT รอบเดือนธันวาคม 2568',1117:'กิจกรรม Workshop From Farm to Fork',1187:'ประกาศห้องสอบ JLPT ครั้งที่ 1/2026 ศูนย์สอบเชียงใหม่',1125:'ประกาศห้องสอบ JLPT ครั้งที่ 2/2025 ศูนย์สอบเชียงใหม่'}
    return overrides.get(post['id'],plain(post['title']['rendered']))
def thumb(post):
    media=MEDIA.get(post.get('featured_media'))
    if media:
        sizes=media.get('media_details',{}).get('sizes',{})
        for size in ['medium_large','large','full']:
            if size in sizes and asset(sizes[size].get('source_url','')):return asset(sizes[size]['source_url'])
        return asset(media.get('source_url',''))
    soup=BeautifulSoup(post['content']['rendered'],'html.parser');im=soup.find('img')
    return asset(im.get('src','')) if im else None
def card(path,post):
    image=thumb(post)
    visual=img(path,image,'', 'card-img') if image else f'<div class="card-placeholder">{img(path,"assets/logo.svg", "")}</div>'
    return f'<article class="news-card" data-category="{esc(cat(post))}" data-year="{int(post["date"][:4])+543}" data-search="{esc(title(post)+" "+plain(post["excerpt"]["rendered"]))}"><a href="{rel(path,ID_PATH[post["id"]])}" class="card-visual" tabindex="-1" aria-hidden="true">{visual}</a><div class="card-body"><div class="meta"><span>{cat(post)}</span><time datetime="{post["date"][:10]}">{date(post["date"])}</time></div><h3>{link(path,ID_PATH[post["id"]],esc(title(post)))}</h3>{link(path,ID_PATH[post["id"]],'อ่านเรื่องราว','text-link')}</div></article>'
def sanitize(raw,path):
    soup=BeautifulSoup(raw,'html.parser')
    for el in soup.select('script,style,form,input,button,object,embed'):el.decompose()
    for el in list(soup.find_all(True)):
        if el.name is None:continue
        if el.name=='h1':el.name='h2'
        for key in list(el.attrs):
            if key.startswith('on') or key in ['style','srcset','sizes','width','height','class','id']:del el[key]
        if el.name=='iframe':
            src=el.get('src','')
            if urlparse(src).netloc in ['www.ojsatn.or.th','ojsatn.or.th'] and '/embed/' in src:el.decompose();continue
            a=soup.new_tag('a',href=src);a.string='เปิดแผนที่ใน Google Maps' if 'google.com/maps' in src else 'เปิดเอกสารหรือสื่อประกอบ';a['class']='button outline';a['target']='_blank';a['rel']='noopener noreferrer';el.replace_with(a);continue
        if el.name=='img':
            original=el.get('src','');local=asset(original)
            if 'fbcdn.net/images/emoji.php/' in original:
                code=Path(urlparse(original).path).stem
                try:el.replace_with(chr(int(code,16)))
                except ValueError:el.replace_with(el.get('alt',''))
                continue
            if local:
                el['src']=rel(path,local);el['loading']='lazy';el['alt']=el.get('alt','')
                if not el.parent or el.parent.name!='a':
                    a=soup.new_tag('a',href=rel(path,local));a['class']='image-link';a['aria-label']='เปิดภาพขนาดเต็ม';el.wrap(a)
            else:
                broken.append({'page':path,'url':original})
                note=soup.new_tag('p');note['class']='missing-media';note.string='ภาพประกอบต้นฉบับนี้ไม่สามารถเปิดได้จากเว็บไซต์เดิม';el.replace_with(note)
        if el.name=='a' and el.get('href'):
            u=html.unescape(el['href']);parsed=urlparse(u)
            if parsed.scheme.lower() in ['javascript','data']:del el['href'];continue
            local=asset(u)
            if local:el['href']=rel(path,local)
            elif parsed.netloc in ['www.ojsatn.or.th','ojsatn.or.th']:
                dest=URLS.get(unquote(parsed.path).rstrip('/'))
                pid=parse_qs(parsed.query).get('p',[None])[0]
                if pid and pid.isdigit():dest=ID_PATH.get(int(pid),dest)
                if dest:el['href']=rel(path,dest)
                elif parsed.path=='/' and not parsed.query:el['href']=rel(path,'index.html')
            if urlparse(el.get('href','')).scheme in ['http','https']:
                el['target']='_blank';el['rel']='noopener noreferrer'
    for table in soup.find_all('table'):
        wrapper=soup.new_tag('div');wrapper['class']='table-scroll';wrapper['tabindex']='0';wrapper['role']='region';wrapper['aria-label']='ตารางข้อมูล เลื่อนแนวนอนได้';table.wrap(wrapper)
    return str(soup)
def home():
    p='index.html';hero=photo('S__447504393.jpg')
    members=[x for x in POSTS if 4 in x['categories'] and x['id']!=1177][:3]
    exam=[x for x in POSTS if 3 in x['categories']][:3]
    body=f'''<section class="hero"><div class="wrap hero-grid"><div class="hero-copy"><span class="eyebrow"><span class="diamond">◇</span> มิตรภาพที่เชื่อมสองวัฒนธรรม</span><h1>สานสัมพันธ์<br>ไทย–ญี่ปุ่น<br><em>จากรุ่นสู่รุ่น</em></h1><p>พื้นที่แห่งมิตรภาพของนักเรียนเก่าญี่ปุ่น<br>ร่วมเรียนรู้ แลกเปลี่ยน และสืบสานสายสัมพันธ์<br>ของชุมชนไทย–ญี่ปุ่นในภาคเหนือ</p><div class="actions">{link(p,'news/','ข่าวสารและกิจกรรม','button')}{link(p,'about/','รู้จักสมาคม','text-link')}</div><div class="hero-note"><span>2528</span><p>จุดเริ่มต้นของการรวมตัว<br>ของนักเรียนเก่าญี่ปุ่นในเชียงใหม่</p></div></div><div class="hero-art"><div class="hero-seal" aria-hidden="true">友<br><span>มิตรภาพ</span></div><figure>{img(p,hero,'งานทำบุญสมาคมและประเพณีล้านนาสระเกล้าดำหัว ปี 2567','hero-image',True)}<figcaption><span>เรื่องราวของเรา</span><strong>เชื่อมผู้คน ผ่านภาษาและวัฒนธรรม</strong><small>งานทำบุญสมาคมและประเพณีล้านนาสระเกล้าดำหัว ปี 2567</small></figcaption></figure><div class="art-corner" aria-hidden="true">◇</div></div></div></section>
    <section class="quick-section"><div class="wrap quick-grid">{''.join(f'<a href="{rel(p,u)}"><span class="quick-number">0{i}</span><div><h2>{t}</h2><p>{d}</p></div></a>' for i,(u,t,d) in enumerate([('news/','สมาชิกและกิจกรรม','พบปะ แลกเปลี่ยน และร่วมกิจกรรม'),('exams/','การสอบ JLPT / EJU','ข่าวการสอบและประกาศศูนย์สอบ'),('school/','เรียนภาษาญี่ปุ่น','เริ่มต้นและต่อยอดการเรียนรู้')],1))}</div></section>
    <section class="section"><div class="wrap"><div class="section-title"><div><span class="eyebrow">ความเคลื่อนไหวของสมาคม</span><h2>ข่าวสารและกิจกรรม</h2></div>{link(p,'news/','ดูข่าวทั้งหมด','text-link')}</div><div class="news-grid">{''.join(card(p,x) for x in members)}</div></div></section>
    <section class="exam-section section"><div class="wrap exam-grid"><div><span class="eyebrow">สำหรับผู้เข้าสอบ</span><h2>ก้าวต่อไป<br>บนเส้นทางภาษาญี่ปุ่น</h2><p>รวมข่าวการสอบ JLPT และ EJU<br>กำหนดการ ประกาศห้องสอบ และผลสอบ</p>{link(p,'exams/','ดูประกาศการสอบทั้งหมด','button outline')}<p class="fine">โปรดตรวจสอบปีและรอบสอบในแต่ละประกาศ</p></div><div class="exam-list">{''.join(f'<a href="{rel(p,ID_PATH[x["id"]])}"><span class="meta">{date(x["date"])}</span><h3>{esc(title(x))}</h3></a>' for x in exam)}</div></div></section>
    <section class="section story-section"><div class="wrap story-grid"><div class="story-picture">{img(p,photo('history05.jpg'),'ภาพประวัติศาสตร์ของสมาคมจากเว็บไซต์เดิม')}<span>จากวันแรก สู่สายสัมพันธ์ที่ยั่งยืน</span></div><div><span class="eyebrow">รากฐานของมิตรภาพ</span><h2>จากการพบปะเล็ก ๆ<br>สู่ชุมชนที่เติบโตไปด้วยกัน</h2><p>สมาคมเป็นพื้นที่เชื่อมโยงนักเรียนเก่าญี่ปุ่น และผู้สนใจภาษาและวัฒนธรรมญี่ปุ่น ผ่านกิจกรรม การเรียนรู้ และการแลกเปลี่ยนระหว่างผู้คน</p>{link(p,'about/','อ่านเรื่องราวของสมาคม','text-link')}<div class="story-links">{link(p,'committee/','คณะกรรมการบริหาร')}{link(p,'journal/','วารสารสมาคม')}</div></div></div></section>'''
    shell(p,'หน้าแรก',body,'home')
def listing(path,items,title_,subtitle,active='news',fixed=False):
    cats=sorted(set(cat(x) for x in items));years=sorted(set(int(x['date'][:4])+543 for x in items),reverse=True)
    controls=f'<div class="filters"><label class="search-label">ค้นหาข่าว<input id="news-search" type="search" placeholder="พิมพ์หัวข้อหรือคำที่ต้องการค้นหา"></label><label>หมวดหมู่<select id="category-filter"><option value="">ทุกหมวดหมู่</option>{"".join(f"<option>{esc(x)}</option>" for x in cats)}</select></label><label>ปี พ.ศ.<select id="year-filter"><option value="">ทุกปี</option>{"".join(f"<option>{x}</option>" for x in years)}</select></label></div>'
    body=heading(path,title_,subtitle)+f'<section class="section"><div class="wrap">{controls}<p id="result-count" role="status" aria-live="polite" class="fine">ทั้งหมด {len(items)} รายการ</p><div class="news-grid searchable">'+''.join(card(path,x) for x in items)+'</div><p id="empty-state" hidden>ไม่พบข่าวที่ตรงกับการค้นหา ลองเปลี่ยนคำค้นหรือเลือกปีอื่น</p><div class="pagination" hidden><button id="prev-page" class="button outline">ก่อนหน้า</button><span id="page-status"></span><button id="next-page" class="button outline">ถัดไป</button></div></div></section>'
    shell(path,title_,body,active)
def article(post):
    p=f'news/{post["id"]}/index.html'
    related=[x for x in POSTS if x['id']!=post['id'] and set(x['categories'])&set(post['categories'])][:3]
    body=f'<div class="wrap article-layout"><article><div class="crumb">{link(p,"index.html","หน้าแรก")} / {link(p,"news/","ข่าวและกิจกรรม")}</div><span class="eyebrow">{cat(post)}</span><h1>{esc(title(post))}</h1><div class="article-meta"><time datetime="{post["date"][:10]}">เผยแพร่ {date(post["date"])}</time><span>สมาคมนักเรียนเก่าญี่ปุ่นฯ สาขาภาคเหนือ</span></div><p class="archive-notice">เนื้อหาตามประกาศ ณ วันที่เผยแพร่ โปรดตรวจสอบกำหนดการและเงื่อนไขก่อนดำเนินการ</p><div class="prose">{sanitize(post["content"]["rendered"],p)}</div><div class="article-end">{link(p,"news/","กลับไปข่าวและกิจกรรม","text-link")}<a href="{esc(post["link"])}" target="_blank" rel="noopener noreferrer">แหล่งที่มาเดิม</a></div></article><aside><span class="eyebrow">อ่านต่อ</span><h2>เรื่องราวที่เกี่ยวข้อง</h2>{"".join(f"<div class=related><small>{date(x['date'])}</small><h3>{link(p,ID_PATH[x['id']],esc(title(x)))}</h3></div>" for x in related)}<div class="aside-contact"><h3>สอบถามสมาคม</h3><p>โทร. 053-272-331</p>{link(p,"contact/","ช่องทางติดต่อ","text-link")}</div></aside></div>'
    shell(p,title(post),body,'news',plain(post['excerpt']['rendered'])[:180])
def about():
    p='about/index.html';source=next(x for x in PAGES if x['id']==88)
    source=dict(source,content=dict(source['content']))
    history=BeautifulSoup(source['content']['rendered'],'html.parser')
    presidents=next(t for t in history.find_all('table') if any(r.find('td') and r.find('td').get_text(strip=True)=='20' for r in t.find_all('tr')))
    additions=json.loads((ROOT/'content/presidents-additions.json').read_text(encoding='utf-8'))['rows']
    for values in additions:
        row=history.new_tag('tr')
        for value in values:
            cell=history.new_tag('td');cell.string=value;row.append(cell)
        (presidents.find('tbody') or presidents).append(row)
    body_rows=presidents.find('tbody') or presidents
    for row in list(body_rows.find_all('tr',recursive=False))[::-1]:body_rows.append(row.extract())
    source['content']['rendered']=str(history)
    timeline=[('2528','เริ่มต้นการรวมตัว','ประชุมนักเรียนเก่าญี่ปุ่นในเชียงใหม่ เมื่อวันที่ 24 สิงหาคม 2528'),('2530','เปิดสำนักงานภาคเหนือ','พิธีเปิดสำนักงานภาคเหนืออย่างเป็นทางการ เมื่อวันที่ 22 กุมภาพันธ์ 2530'),('2539','บ้านของสมาคมในปัจจุบัน','เปิดสำนักงานถนนสามล้าน หน้าวัดพระสิงห์ เมื่อวันที่ 7 เมษายน 2539'),('2559','สาขาภาคเหนือ','จดทะเบียนแก้ไขข้อบังคับเพิ่มเติมให้มีสำนักงานสมาคมสาขาภาคเหนือ เมื่อวันที่ 3 มิถุนายน 2559')]
    body=heading(p,'เรื่องราวของสมาคม','มิตรภาพที่เริ่มต้นจากการพบปะ และเติบโตผ่านความผูกพันระหว่างไทย–ญี่ปุ่น')+f'<section class="section"><div class="wrap"><div class="vision"><span class="eyebrow">วิสัยทัศน์</span><h2>ศูนย์กลางกิจกรรมนักเรียนเก่าญี่ปุ่น ชาวไทย<br>และเครือข่ายในอาเซียน</h2><p>เป็นเลิศด้านการเรียนการสอนภาษาและวัฒนธรรมญี่ปุ่นในประเทศไทย</p></div><div class="timeline">'+''.join(f'<div><strong>{y}</strong><h3>{t}</h3><p>{d}</p></div>' for y,t,d in timeline)+f'</div><div class="center-actions">{link(p,"committee/","รู้จักคณะกรรมการบริหาร","button")}</div><details class="history-full" open><summary>ประวัติสมาคมฉบับเต็มและรายนามประธานในอดีต</summary><p class="archive-notice">บทความประวัติจากเว็บไซต์เดิม เก็บสำนวนและข้อมูลตามต้นฉบับ</p><div class="prose">{sanitize(source["content"]["rendered"],p)}</div></details></div></section>'
    body=body.replace('ประวัติสมาคมฉบับเต็มและรายนามประธานในอดีต','ประวัติสมาคมฉบับเต็มและรายนามประธานตั้งแต่อดีตถึงปัจจุบัน')
    body=body.replace('บทความประวัติจากเว็บไซต์เดิม เก็บสำนวนและข้อมูลตามต้นฉบับ','บทความประวัติจากเว็บไซต์เดิม พร้อมเพิ่มเติมรายนามประธานจนถึงวาระปัจจุบัน')
    shell(p,'เกี่ยวกับสมาคม',body,'about')
def committee():
    p='committee/index.html';source=next(x for x in PAGES if x['id']==804)
    terms=[];soup=BeautifulSoup(source['content']['rendered'],'html.parser')
    for label in soup.find_all('p',recursive=False):
        text=re.sub(r'\s+','',label.get_text())
        match=re.fullmatch(r'ประจำปี(\d{4})[-–](\d{4})',text)
        table=label.find_next_sibling()
        if match and table and table.find('table'):terms.append((match.group(1),match.group(2),table))
    old=''.join(f'<h3>ประจำปี {a}–{b}</h3>'+sanitize(str(t),p) for a,b,t in sorted(terms,key=lambda x:x[0],reverse=True))
    def person(n,r,cls=''):return f'<article class="person{cls}"><h3>{" ".join(f"<span>{esc(w)}</span>" for w in n.split())}</h3><p>{esc(r)}</p></article>'
    lead=[x for x in COMMITTEE if x[1]=='ประธาน'];vice=[x for x in COMMITTEE if x[1].startswith('รองประธาน')]
    board=sorted([x for x in COMMITTEE if x not in lead+vice],key=lambda x:not x[1].startswith('เลขาธิการ'))
    tier=lambda label,cls,people,extra='':f'<div class="org-tier {cls}">{f"<span class=org-label>{label}</span>" if label else ""}<div class="org-row">{"".join(person(n,r,extra) for n,r in people)}</div></div>'
    entries=tier('','org-lead',lead,' person-lead')+tier(f'รองประธาน {len(vice)} ท่าน','org-vice',vice)+tier(f'เลขาธิการและกรรมการบริหาร {len(board)} ท่าน','org-board',board)
    body=heading(p,'คณะกรรมการบริหาร','ร่วมขับเคลื่อนสมาคม เชื่อมโยงสมาชิก และสานสัมพันธ์ไทย–ญี่ปุ่น')+f'<section class="section"><div class="wrap"><div class="section-title"><div><span class="eyebrow">คณะกรรมการชุดปัจจุบัน</span><h2>ผู้ร่วมดูแลบ้านแห่งมิตรภาพ</h2></div><span class="count-badge">15 ท่าน</span></div><div class="org-chart">{entries}</div><details class="history-full"><summary>รายนามคณะกรรมการวาระก่อนหน้า (เรียงจากวาระล่าสุด)</summary><div class="prose">{old}</div></details></div></section>'
    shell(p,'คณะกรรมการบริหาร',body,'about')
def school():
    p='school/index.html';source=next(x for x in PAGES if x['id']==32)
    body=heading(p,'เรียนภาษาญี่ปุ่น','เปิดประตูสู่ภาษา วัฒนธรรม และโอกาสใหม่ ๆ')+f'<section class="section"><div class="wrap"><div class="school-intro"><div><span class="eyebrow">โรงเรียนสอนภาษาญี่ปุ่น</span><h2>เริ่มต้นจากความสนใจ<br>เติบโตไปกับการเรียนรู้</h2><p>เปิดสอนภาษาญี่ปุ่นทุกระดับ ตั้งแต่ไม่มีพื้นฐาน ตัวอักษร ไวยากรณ์ การสนทนา จนถึงระดับสูง JLPT N5–N1</p>{contact_buttons(p)}</div><div class="course-list"><div><span>01</span><h3>ภาษาญี่ปุ่นพื้นฐาน</h3><p>เริ่มต้นตัวอักษรและไวยากรณ์</p></div><div><span>02</span><h3>การสนทนาภาษาญี่ปุ่น</h3><p>เรียนรู้และพัฒนาการสื่อสาร</p></div><div><span>03</span><h3>ภาษาญี่ปุ่นเพื่อการสอบ JLPT</h3><p>ต่อยอดตามระดับความรู้ภาษาญี่ปุ่น</p></div></div></div><div class="section-title"><h2>ข้อมูลหลักสูตรจากโรงเรียน</h2></div><p class="archive-notice">ข้อมูลประชาสัมพันธ์จากเว็บไซต์เดิม กรุณาสอบถามตารางเรียน ค่าเรียน และการเปิดรับสมัครปัจจุบันกับเจ้าหน้าที่</p><div class="prose school-posters">{sanitize(source["content"]["rendered"],p)}</div>{link(p,"school/news/","ข่าวโรงเรียนทั้งหมด","text-link")}</div></section>'
    shell(p,'เรียนภาษาญี่ปุ่น',body,'school')
def journal():
    p='journal/index.html'
    cards=[]
    for i,item in enumerate(read('journals.json')):
        label=plain(item['title'])
        pdf=f'<a class="text-link" href="{rel(p,item["pdf"])}" download>ดาวน์โหลด PDF</a>' if item.get('pdf') else ''
        cover=img(p,item.get('cover'),label,'original-cover')
        cards.append(f'<article class="journal-card"><a href="{rel(p,item["pdf"])}" target="_blank" rel="noopener noreferrer">{cover}</a><div><span class="eyebrow">วารสารสมาชิกสัมพันธ์</span><h2>{esc(label)}</h2><p>เรื่องราว ข่าวสาร และสายสัมพันธ์ของสมาชิกสมาคม</p><a class="button outline" href="{rel(p,item["pdf"])}" target="_blank" rel="noopener noreferrer">เปิดอ่านวารสาร</a>{pdf}<a class="fine" href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">อ่านแบบพลิกหน้าบน Heyzine</a></div></article>')
    shell(p,'วารสารสมาคม',heading(p,'วารสารสมาคม','บันทึกเรื่องราว ความทรงจำ และความเคลื่อนไหวของชุมชนเรา')+'<section class="section"><div class="wrap journal-grid">'+''.join(cards)+'</div></section>','journal')
def contact():
    p='contact/index.html';line=f'<a href="{esc(CONFIG["line_url"])}" target="_blank" rel="noopener noreferrer">เพิ่มเพื่อน LINE</a>' if CONFIG.get('line_url') else '<span>สอบถามช่องทาง LINE ได้ทางโทรศัพท์หรือ Facebook</span>'
    body=heading(p,'ติดต่อสมาคม','ยินดีให้ข้อมูลและต้อนรับทุกการติดต่อ')+f'<section class="section"><div class="wrap contact-grid"><div><span class="eyebrow">พบกันที่เชียงใหม่</span><h2>{NAME}</h2><p>เลขที่ 3/3 ถนนสามล้าน ตำบลพระสิงห์<br>อำเภอเมืองเชียงใหม่ จังหวัดเชียงใหม่ 50200</p><p>สำนักงานตั้งอยู่บริเวณหน้าวัดพระสิงห์วรมหาวิหาร</p><a class="button outline" href="https://www.google.com/maps/search/?api=1&amp;query=สมาคมนักเรียนเก่าญี่ปุ่น+ถนนสามล้าน+เชียงใหม่" target="_blank" rel="noopener noreferrer">เปิดแผนที่การเดินทาง</a></div><div class="contact-details"><div><span>โทรศัพท์</span><a href="tel:+6653272331">053-272-331</a></div><div><span>Facebook</span><a href="https://www.facebook.com/ojsatn" target="_blank" rel="noopener noreferrer">สมาคมนักเรียนเก่าญี่ปุ่นฯ สาขาภาคเหนือ</a></div><div><span>LINE</span>{line}</div><div><span>เวลาทำการ</span><p>จันทร์–ศุกร์ &nbsp; 10:00–20:00 น.<br>เสาร์–อาทิตย์ &nbsp; 09:00–16:00 น.</p></div></div></div></section>'
    qr=f'<section class="section line-section"><div class="wrap line-panel"><a href="{esc(CONFIG["line_url"])}" target="_blank" rel="noopener noreferrer">{img(p,"assets/line-qr.png","QR Code เพิ่มเพื่อน LINE ของสมาคม","line-qr")}</a><div><span class="eyebrow">พูดคุยกับเราได้ทาง LINE</span><h2>สแกนเพื่อเพิ่มเพื่อน</h2><p>เปิดกล้องหรือแอป LINE เพื่อสแกน QR Code<br>หากใช้มือถือ กดปุ่มด้านล่างเพื่อเพิ่มเพื่อนได้ทันที</p><a class="button" href="{esc(CONFIG["line_url"])}" target="_blank" rel="noopener noreferrer">เพิ่มเพื่อนใน LINE</a></div></div></section>' if CONFIG.get('line_url') else ''
    shell(p,'ติดต่อเรา',body+qr)
def aliases():
    for item in POSTS+PAGES:
        old=unquote(urlparse(item['link']).path).strip('/')
        dest=ID_PATH[item['id']]
        if old+'/'==dest or not old:continue
        path=old+'/index.html';target=rel(path,dest)
        f=OUT/path;f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(f'<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={esc(target)}"><meta name="robots" content="noindex"><title>ย้ายหน้าแล้ว</title><a href="{esc(target)}">เปิดหน้าใหม่</a></html>',encoding='utf-8')
    (ROOT/'content/url-map.json').write_text(json.dumps(URLS,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
    home();listing('news/index.html',POSTS,'ข่าวสารและกิจกรรม','ติดตามความเคลื่อนไหวของสมาคม และค้นเรื่องราวย้อนหลังได้ในที่เดียว')
    listing('exams/index.html',[x for x in POSTS if 3 in x['categories']],'การสอบ JLPT / EJU','รวมประกาศการสอบ เรียงตามวันที่เผยแพร่ โปรดตรวจสอบปีและรอบสอบก่อนใช้งาน','exams')
    listing('school/news/index.html',[x for x in POSTS if 5 in x['categories']],'ข่าวโรงเรียนภาษาญี่ปุ่น','ข่าวสารและประกาศย้อนหลังจากโรงเรียน','school')
    for post in POSTS:article(post)
    about();committee();school();journal();contact();aliases()
    shell('404.html','ไม่พบหน้าที่ต้องการ',heading('404.html','ไม่พบหน้าที่ต้องการ','หน้านี้อาจเปลี่ยนที่อยู่หลังปรับปรุงเว็บไซต์')+f'<div class="wrap section">{link("404.html","news/","ค้นหาข่าวและกิจกรรม","button")}</div>')
    (OUT/'.nojekyll').write_text('',encoding='utf-8')
    (ROOT/'content/build-report.json').write_text(json.dumps({'generated_pages':len(generated),'posts':len(POSTS),'committee':len(COMMITTEE),'unavailable_images':broken},ensure_ascii=False,indent=2),encoding='utf-8')
    print('Built',len(generated),'pages;',len(POSTS),'posts;',len(broken),'unavailable image references')
