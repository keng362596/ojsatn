# OJSATN preview verification — 27 September 2026

## Completed

- WordPress REST import: 118 published posts, 6 pages, 5 categories, 396 media records.
- Generated 128 content pages plus 121 compatibility redirect pages (249 HTML files total).
- Checked every local HTML link and asset reference: no missing local targets.
- Every content page has a Thai document language, responsive viewport and one primary heading.
- Current committee contains all 15 people in the two orange boxes supplied by the user. Meeting attendance labels are not published as committee roles.
- Original user-supplied LINE QR is stored unchanged. Decoded URL and all LINE buttons match `https://lin.ee/X4f1mtq`.
- Imported all 4 publicly available Heyzine journal PDFs and original cover images; checked links in browser.
- Browser: menu opens on mobile; Thai news listing search found SUMI-E; no-result message works; clearing the search restores results; exam category returns 44 posts, filtered to 2569 returns 4; pagination advances to page 2 of 4.
- Browser geometry: home, about, committee, exams, school, journal, contact and a news detail at 390 / 768 / 1440 px; no horizontal page overflow in 24 cases.
- Additional home, journal and contact checks at 360 / 1024 px; no horizontal overflow in 6 cases.
- Fonts are local, without a third-party font request at runtime.
- No registration/contact forms, backend, database, analytics or live WordPress dependency.
- Original same-byte duplicate assets were deduplicated; all source URL mappings retained.

## Limits and remaining review

- Browser screenshot capture repeatedly timed out. Functional and DOM/geometry checks passed, but a screenshot-based visual review has **not** been completed. Review the local preview before enabling production Pages or changing the custom domain.
- One original archive image is unavailable: the JLPT result image in post 73 (2022). The new article displays a readable missing-image note and keeps the rest of the article.
- Two historical external EJU document paths (`EJUapply.PDF`, `EJUhowto.pdf`, including tracked variants) return 404. Original historical links remain; no unrelated or newer application document has been substituted.
- Four obsolete contact images from the old site's `/blog/` path were unavailable. Current contact data is reproduced as text, Facebook is linked, and LINE uses the user's newly supplied QR.
- Historical announcements retain source wording, including any English/Japanese already present. New UI and editorial copy are Thai.
- Historical schedules/course posters are not presented as current open enrollment; verify current details with the association.
- Custom domain, DNS and GitHub Pages publication settings have not been changed.

Run `python scripts/build.py` followed by `python scripts/check.py` after content or template changes. See `validation-report.json`, `build-report.json` and `source/migration-report.json` for machine-readable evidence.
