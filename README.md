# FORM / AI — A nine-week interactive AI research learning LMS

An independent, browser-based learning tracker built from **HTML, CSS, Tailwind CDN (optional), vanilla JavaScript, IndexedDB, and optional Lucide/Chart.js CDNs**. No React, build framework, account, backend, external AI API or ChatGPT integration is needed.

## Quick start

1. Download `index.html` and open it in a modern browser.
2. Prefer a stable local origin for reliable data storage: put the file in its own folder, run `python3 -m http.server 8000` from that folder and open `http://localhost:8000/`.
3. Select **Daily lessons** to study, practice and take a short quiz. Complete all three checkpoints to mark the day complete.
4. Open **Interactive labs**, **Weekly projects** and **Readiness assessment** for additional learning tools.
5. Every screen has a shareable hash URL, including nested lesson paths such as `#/learn/week-2/derivatives-and-sensitivity` (week/day slugs plus optional tab: `…/practice`, `…/quiz`, `…/notes`). Stopping the timer plays a beep; the focus length and beep can be tuned in **Settings → Focus timer & sound**.
6. Use **Settings → Export JSON backup** regularly. **Import JSON** restores progress on another device/browser.

The learning experience works without downloading Python packages, but actual Python examples need to be copied into a local Python environment or notebook. See official reference links inside each week.

## Contents

- 9 weeks = **63 distinct daily lessons**. Weeks 1–8 form the core path; Week 9 is an optional capstone.
- 63 copyable Python/shell starter snippets (one per day), teaching notes and short multiple-choice checks.
- 3 milestones per day: **concept learned → practice verified → quiz passed**.
- 9 weekly applied projects with four independently tracked tasks and local reflection/evidence fields.
- 6 interactive math/concept labs: tensor memory; gradient descent; toy text segmentation; attention softmax; LoRA parameter counts; old/new capability retention.
- Model-lifecycle flowchart with clickable conceptual nodes.
- Search across the curriculum, notes and bookmarks, adjustable focus timer (1–120 min, with a completion beep), manual study-time recording.
- Dynamic charts and weekly progress analytics based on saved user data.
- 7-skill, 0–21 self-rated readiness assessment with local recommendations.
- Light and dark **monochrome** themes, mobile navigation, and JSON export/import/reset.

## Technology and privacy

The **single HTML file embeds all curriculum data, source JS and primary CSS**. It requests these optional UI enhancements from public CDNs when the browser is online:

- Tailwind browser CDN: `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4` — explicitly intended by Tailwind for development/learning demos, not production bundling.
- Lucide icons: `https://unpkg.com/lucide@0.468.0/dist/umd/lucide.js`
- Chart.js: `https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js`

The interface remains usable if these CDNs are blocked: it has its own CSS and SVG chart fallbacks; only decorative icons may be absent.

**Progress is stored locally.** The app first tries IndexedDB, then localStorage. If browser security blocks both, it shows `Memory only (export often)` and an exported backup is essential. Clearing site data can also delete progress. This app does not upload progress to any server. Clicking an external reference link contacts that reference website, and CDN resources may contact their hosts.

The app runs **numerical JavaScript demonstrations**, not Python training, neural model inference or real GPU experiments. Example benchmark values in lessons and labs are explicitly hypothetical. Do not confuse practice checkmarks with formal skill validation.

## Source files (in this ZIP)

- `index.html` — standalone downloadable LMS.
- `app.js` — all interactive UI and persistence code.
- `template.html` — static HTML and CSS template.
- `curriculum.json` — curriculum, quiz, weekly project, and resource data.
- `snippets.json` — Python/shell examples by day.
- `build.py` — rebuilds `index.html` from the editable sources (`python3 build.py`).
- `previews/` — reference screenshots of the interface.

## Editing and extending

To modify the course, edit `curriculum.json` or `snippets.json`, change `app.js` or `template.html`, then run `python3 build.py`. You do not need Node.js to build the app. Keep exactly one stable ID per day (`d1`–`d63`) to preserve compatibility with existing backups. If you change the state schema, add an explicit versioned migration and test backup import before distributing.

## Content boundaries

- Core: Weeks 1–2 numerical computing, gradient descent, PyTorch.
- Core: Weeks 3–4 tokenization, embeddings, transformers, attention and inference.
- Core: Weeks 5–6 LoRA, QLoRA, datasets, fine-tuning and model evaluation.
- Core: Weeks 7–8 continual learning, model retention and lifecycle observability.
- Optional: Week 9 original experiment, analysis and reproducible research report.

This is an educational tracker and experiment notebook, not a trained AI model or an automated research system.
