# OJSATN — เว็บไซต์สมาคมนักเรียนเก่าญี่ปุ่นฯ สาขาภาคเหนือ

เว็บภาษาไทยแบบ static พร้อมใช้กับ GitHub Pages โดยเผยแพร่โฟลเดอร์ `docs/` ได้ทันที ไม่ต้องมี Node.js, WordPress หรือฐานข้อมูลบนเซิร์ฟเวอร์

## เปิดดูและเผยแพร่

- ดูในเครื่อง: `python -m http.server 4173 --bind 127.0.0.1 --directory docs` แล้วเปิด `http://127.0.0.1:4173/`
- GitHub → **Settings → Pages → Deploy from a branch → main → /docs → Save**
- URL หลังเปิด Pages: `https://keng362596.github.io/ojsatn/`
- ยังไม่ได้ตั้ง custom domain หรือเปลี่ยน DNS ของเว็บไซต์เดิม
- เมื่อต้องการใช้โดเมนจริง ให้ตั้ง Custom domain ใน Pages และ DNS ตามคำแนะนำ GitHub แล้วตรวจ HTTPS ก่อนเปลี่ยนเว็บไซต์หลัก

ลิงก์และไฟล์ภายในใช้ relative paths เพื่อรองรับทั้ง project path `/ojsatn/` และ custom domain

## เนื้อหา

- ข่าวเดิม 118 รายการ ตั้งแต่ปี 2565–2569 พร้อมหน้ารายละเอียดครบทุก ID
- หน้าข้อมูลเดิม 6 หน้า นำมาจัดหมวดใหม่ พร้อมเก็บต้นฉบับใน `content/source/`
- วารสาร 4 ฉบับ เก็บ PDF และปกต้นฉบับไว้ในเว็บไซต์ พร้อมลิงก์ Heyzine
- คณะกรรมการปัจจุบัน 15 ท่าน ตามทั้งสองกรอบสีส้มในภาพที่ผู้ใช้ให้ ส่วนรายนามเดิมเก็บในหัวข้อวาระก่อนหน้า
- โลโก้ SVG และ PNG แปลงจาก Illustrator ต้นฉบับของผู้ใช้ โดยใช้เส้นเวกเตอร์และสีเดิม
- QR LINE เก็บภาพต้นฉบับที่ผู้ใช้ส่ง ปุ่ม LINE ใช้ URL ที่อ่านจาก QR: `https://lin.ee/X4f1mtq`
- ไม่มีแบบฟอร์มสมัครหรือระบบสมาชิก ผู้ชมติดต่อทางโทรศัพท์ LINE หรือ Facebook
- เมนูและส่วนที่เขียนใหม่เป็นภาษาไทย เนื้อหาประกาศเก่ายังคงข้อความอังกฤษ/ญี่ปุ่นที่มีในต้นฉบับ

## อัปเดตเนื้อหา

ติดตั้ง Python 3.12 ขึ้นไป และ `pip install -r requirements.txt` จากนั้น:

```text
python scripts/build.py
python scripts/check.py
```

- `content/committee.json` — รายชื่อและตำแหน่งคณะกรรมการปัจจุบัน
- `content/site.json` — ลิงก์ LINE และค่าตั้งต้นเว็บไซต์
- `content/source/posts.json` — ข่าว พร้อมวันที่ หมวด และเนื้อหา HTML ต้นฉบับ
- `content/source/pages.json` — หน้าข้อมูลต้นฉบับ
- `content/source/journals.json` — วารสารและไฟล์ PDF/ปก
- `docs/assets/site.css` — รูปแบบ responsive
- `docs/assets/site.js` — เมนูมือถือ ค้นหา กรอง และแบ่งหน้าข่าว
- `scripts/build.py` — แม่แบบ HTML และกระบวนการสร้างเว็บทั้งหมด

หลังแก้ source ให้ build, check และ commit ทั้ง source กับ `docs/` เสมอ ไม่แก้ generated HTML โดยตรง

`scripts/migrate.py` ใช้สำหรับนำเข้าจาก WordPress ครั้งแรกเท่านั้น การรันซ้ำจะเขียนทับ snapshot เนื้อหาเดิม ควรตรวจ diff ก่อนนำผลมาใช้ ไม่จำเป็นต้องรันเพื่ออัปเดตข่าวปกติ

## บันทึกการย้ายและการตรวจ

- `content/url-map.json` — ตาราง URL เก่า → หน้าใหม่ พร้อมหน้า redirect สำหรับ path เดิม
- `content/source/assets.json` — URL ไฟล์ต้นทาง → สำเนาในเว็บใหม่
- `content/source/migration-report.json` — จำนวนที่สำรวจและรายการลิงก์ที่เปิดไม่ได้ตอนนำเข้า
- `content/source/recovered-assets.json` — ลิงก์เก่าที่กู้คืนจาก path ใหม่ได้
- `content/build-report.json` — รายการภาพประกอบที่ยังหาไม่ได้
- `content/validation-report.json` — ตรวจลิงก์/ไฟล์ในเว็บ จำนวนข่าว กรรมการ และ QR LINE
- `content/QA.md` — ผลการตรวจการใช้งานและข้อจำกัด

ไฟล์สื่อที่มี bytes เหมือนกันถูกเก็บเพียงสำเนาเดียว แต่รักษา mapping ทุก URL ไว้ ภาพประกอบผล JLPT ปี 2565 หนึ่งภาพและเอกสาร EJU ภายนอกบางลิงก์หายจากต้นทางอยู่แล้ว รายละเอียดอยู่ในรายงาน หน้าเก็บข่าวแสดงหมายเหตุเมื่อไม่มีภาพต้นฉบับ

กำหนดการสอบและหลักสูตรย้อนหลังแสดงวันที่และหมายเหตุให้ตรวจสอบก่อนใช้งาน ไม่ยกประกาศเก่าเป็นการเปิดรับสมัครปัจจุบัน

## ฟอนต์และแหล่งข้อมูล

Noto Sans Thai / Noto Serif Thai เก็บไว้ภายในเว็บ ภายใต้ SIL Open Font License (ดูไฟล์ `docs/assets/OFL-*.txt`)
ข้อมูลและภาพสมาคมมาจาก `https://www.ojsatn.or.th/` ตามคำสั่งเจ้าของงาน โลโก้ รายชื่อปัจจุบัน และ QR LINE อ้างอิงไฟล์/ภาพที่ผู้ใช้ส่ง
