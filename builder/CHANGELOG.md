# FORM / AI — v2 release notes

- Replaced the header storage text pill with an **icon-only storage indicator** (device icon for IndexedDB, Save for localStorage fallback, Offline-database for memory; cloud-off + red ring on save failure). Hovering shows the exact persistence mode, and a soft pulse confirms each save.
- The dashboard **Study time** stat now shows quick-log buttons (+15m/+25m/+45m) and **counts an in-progress focus session live** while the timer runs, updating every tick.
- The **Study activity calendar auto-scrolls horizontally to the current month** on render (heatmap wraps internally on small screens).
- Analytics stat grid extended to six cards: Lesson completion, Lessons started, Practice verified, Knowledge checks passed, **Total session time**, **Quiz attempts** (with passed count and average score).
- **Weekly breakdown** table rows are now clickable — clicking `W1 · Python & numerical ML` opens that week's lessons.

- Added **streak tracking** to every activity-summary row (dashboard + analytics): "current streak" (counts yesterday if today has no activity yet) and "longest streak", computed from real saved study dates.
- Hardened the **service worker**: navigation requests for the app shell are now **network-first** (offline falls back to the cached copy), so a new build is picked up on the very next load instead of being served stale from cache — this caused "my changes are missing / still not responsive" symptoms after the first PWA install. The page also auto-reloads once when an updated service worker takes control.

- Added **direct study-time logging** to the dashboard ("Study time" card: +15/+25/+45 min buttons) and the analytics page ("Record study time now": +15/+25/+45/+60 min buttons) — minutes are recorded against the recommended lesson with a toast naming it, and every stat, chart and the heatmap update immediately. The logged-day title is now included in the confirmation toast everywhere (including the lesson Notes tab).
- Removed the stale generated `builder/index.html`; `builder/build.py` writes only to the project root (`index.html` + `manifest.webmanifest` + `sw.js` + `icons/`).

- Reworked the **focus timer** controls: dedicated icon-only play/pause button (icons + color swap with session state, "Resume" affordance when paused), reset as a separate icon action, and a slim mauve **progress bar under the controls** that fills as the session runs, resets to empty, and reads full at completion.
- Analytics: **"Lessons started"** now counts lessons touched by any milestone, quiz attempt or note; added a **Study activity calendar** section (52-week heatmap) to the analytics page alongside a new **"Daily study actions — last 30 days"** line chart with day-based axis labels; removed the "GitHub-style" wording in favor of "52 weeks of study actions".
- Fixed horizontal overflow on small screens (grid columns now use `minmax(0, …)` so wide children like the heatmap scroll internally instead of stretching the page); verified no overflow from 360px to 1680px.

- Re-themed the whole interface from monochrome black/white to a **slate color scale with a single mauve primary accent** in light and dark modes; heatmap, charts, quiz states, code surfaces and focus rings follow the accents.
- Added **Google Fonts**: Poppins for headings/brand/stats and Nunito Sans (variable) for body text.
- Redesigned the lesson **"Detailed concept explanations"** deep dives as numbered expandable panels (mauve index chip, rotating chevron, open-state ring and accent border).
- Reworked the dark-theme dashboard hero: mauve-glow gradient card, hairline border, mauve CTA and re-tinted decorative circles so it reads as an elevated surface instead of blending into the background.
- Added **PWA support**: `builder/build.py` now emits `index.html` to the **project root** together with `manifest.webmanifest`, a cache-versioned `sw.js` (offline app shell; CDN fonts/Lucide/Chart.js cached at runtime) and Pillow-generated PNG icons (180, 192, 512, plus 192/512 maskable), with the slate-900 rounded-square and mauve serif ƒ logo. Favicon is now an inline SVG in the same style; apple-touch-icon and manifest links go into `<head>` and the service worker registers on https/localhost.
- Import/export backup retained and verified: exports include the full v2 state (milestones, quiz history, notebook, activity, settings); import validates version 1/2 backups and migrates v1 data.

- Added explicit direct completion / reopen button to every daily lesson while retaining separate competency checkpoints.
- Expanded all 63 lessons to six objectives, four collapsible explanations, five practice steps, three challenges and a richer evidence checklist.
- Added 63 additional copyable practical Python cells; retained the 63 original starter examples.
- Replaced single knowledge checks with 4-question graded quizzes per lesson (252 questions total), results, answer explanations, dated attempt history and configurable retake limits.
- Added 315 directed per-day reading entries with specific study goals, plus 91 week-level curated resources.
- Expanded six existing experiments with 26 extra labs (32 built-in), calculation charts, JSON export and editable Python equivalents.
- Added user-created configurable numeric labs, including editing and deletion.
- Added a dedicated Python notebook-like view with optional Pyodide Python/NumPy execution in a worker and copyable console output.
- Replaced recent activity with a GitHub-style 52-week contribution heatmap using actual saved study events.
- Added user-adjustable focus intervals and optional generated completion sounds.
- Added keyboard-accessible custom dropdown controls and mobile layout enhancements.
- Improved local state normalization, preserving v1 completion progress and allowing JSON migration to v2.
- Converted the development source into modular HTML/CSS/JS/JSON files while generating one self-contained HTML release.
