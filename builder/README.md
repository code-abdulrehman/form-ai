# FORM / AI Learning LMS — v2

A complete standalone learning workspace for an **8-week core AI research curriculum + optional Week 9 capstone**. It is built with **HTML, CSS, vanilla JavaScript, IndexedDB** and optional CDN libraries. It requires **no account, backend, ChatGPT integration, API key, Node.js, or production build server**.

## Run the application

1. Regenerate the release from the project root: `python3 builder/build.py` — it writes `index.html` to the **project root**, alongside `manifest.webmanifest`, `sw.js` and `icons/` (icons need Pillow; skipped gracefully without it). Open `index.html` in a current Chromium, Firefox or Safari browser.
2. For PWA install/offline support serve the folder over the local web origin below.
2. For reliable IndexedDB persistence, use a local web origin by opening a terminal in this folder and running:

   ```bash
   python3 -m http.server 8000
   ```

   Then go to `http://localhost:8000/`.
3. Study through **Daily lessons**. Each day has an explicit **Mark day complete** / **Reopen lesson** action. Individual learning, practice and quiz milestones are tracked separately.
4. Use **Settings** to set the focus duration, toggle the finish sound, choose a quiz attempt limit, and export/import a progress backup.

The app will attempt **IndexedDB**, fall back to **localStorage** if needed, and otherwise run in memory with an explicit warning. Clearing site data, moving to another origin, or using private browsing can remove locally stored progress. **Export JSON regularly.** You can import the backup on another device/browser.

## What's included

| Feature | Included |
|---|---|
| Learning path | 9 weeks / 63 days: Weeks 1–8 core + optional Week 9 research capstone |
| Per-day lesson | Six explicit objectives, four collapsible in-depth sections, five practical steps, three stretch challenges, evidence checklist and notes |
| Lesson completion | One-click manual day completion, one-click reopen, and independent learned / practiced / quiz mastery statuses |
| Assessments | Four graded questions per day (252 total), scored result view, detailed explanations, attempts history, best score, 75% mastery threshold, retakes |
| Attempt settings | Unlimited (default), 3, 5, or 10 maximum attempts per daily quiz; per-day quiz reset confirmation |
| References | Five individually tracked directed readings per day (315 day-level entries); 91 additional week-level curated links with learning goals |
| Practice code | Copyable Python/shell starter and runnable challenge snippets for all 63 days, plus experiment checklist code |
| Interactive labs | 32 built-in live numeric simulations; configurable controls, charts, result snapshots, copied JSON results, copyable Python equivalents |
| Custom labs | Create/edit/delete up to 40 formula-driven labs using linear, quadratic, sigmoid, memory, or loss examples; change inputs and copy generated Python |
| Python cells | Editable notebook-style code and output; optionally run supported Python/NumPy snippets in a Pyodide Web Worker when online |
| Activity | 52-week activity contribution calendar (auto-scrolled to the current month) with active days, learning actions, current and longest streak |
| Focus sessions | Configurable 1–180 minute focus timer, start/pause/reset, optional completion chime, logged study time |
| Weekly projects | Nine independent project boards and recorded evidence and progress |
| Learning analytics | Weekly progress, research readiness score, charts, and a local rule-based study coach |
| Personal progress | Day notes, checklists, bookmarks, search, theme choice, JSON backup/import/reset and local persistent storage |
| PWA | Installable web app: web manifest, service worker offline app-shell cache and generated PNG icons |
| UI | Responsive slate + mauve themes (Poppins headings, Nunito Sans body) with accessible custom JavaScript-powered dropdowns and keyboard controls |

The lab library is **not a replacement for Jupyter and real GPU training**: the interactive charts are numerical JavaScript demonstrations; optional browser Python uses a separate runtime downloaded from a CDN, supports common Python and NumPy examples, and **does not include PyTorch, Transformers, PEFT or CUDA**. For those, copy the code into a configured local Jupyter or other Python notebook. The client-side worker is not a security sandbox; only run code you understand.

## Editable source files

- `index.html` — fully standalone, generated HTML (contains CSS, JS and all course data inline).
- `template.html` — HTML shell; contains injection markers consumed by `build.py`.
- `styles.css` — complete editable application stylesheet.
- `app.js` — main user interface, routing, persistence, quizzes, learning progress, focus timer, labs and settings.
- `extra_labs.js` — 26 additional built-in lab definitions and calculations (combined with the six core labs in `app.js` = 32).
- `curriculum.json` — 9 weeks, 63 days, lesson guides, four-question quizzes, readings and projects.
- `snippets.json` — the 63 original Python/shell starter examples.
- `challenge_snippets.json` — 63 additional standalone Python practice cells.
- `build.py` — merges all the editable sources into the single `index.html`.
- `regression_test.py` — optional browser regression checks; needs Python Playwright and a local Chromium install.
- `CHANGELOG.md` — feature list for v2.

### Rebuild the standalone HTML

Edit any source file (except generated `index.html`), then run:

```bash
python3 build.py
```

This writes a new `index.html`. You may rename it however you like, host it on your own site, or run it directly from the local development server.

**Keep existing daily lesson IDs `d1`–`d63` unchanged** if you want old progress/backups to continue mapping to their lessons. v1 backups are migrated to the v2 state schema; existing completed days, notes, milestones and project progress are preserved where possible. Quizzes generated for v2 naturally do not have historical answers from a v1 backup.

## Local data and network access

The single HTML file contains all required course content, CSS, numeric lab logic, chart fallbacks and persistence code. It optionally downloads:

- Tailwind browser CDN — `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4` (development convenience; most UI is defined in our own CSS).
- Lucide icon bundle — `https://unpkg.com/lucide@0.468.0/dist/umd/lucide.js`.
- Chart.js — `https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js`.
- Pyodide Python runtime **only when the user invokes the Python cell runner** — `https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js` and runtime dependencies.
- Official learning links — only when the user explicitly opens them.

The app has no telemetry, analytics service, remote database, AI API, cloud synchronization or user accounts. Exporting progress writes a JSON file to the browser's downloads. JSON backups include notes, quiz history, research lab states, custom labs and settings; treat exported backup files as personal data. Audio completion is locally generated by the browser using WebAudio after user interaction; device autoplay restrictions may mute it.

## Curriculum outline

1. Weeks 1–2: Python scientific computing, tensors, gradients, autograd, neural networks and optimization.
2. Weeks 3–4: Tokenization, embeddings, attention, transformers, pretrained inference.
3. Weeks 5–6: LoRA/QLoRA, dataset processing, checkpoints, evaluation design.
4. Weeks 7–8: Continual-learning experiments, retention, economic evaluation and research dashboard.
5. Week 9 (optional): A model-longevity capstone experiment and research write-up.

## Accuracy and limits

- Some example model accuracies, training losses, and synthetic samples are **illustrations**, not published research results.
- The quiz is self-study material; a checked day or passed quiz does not independently certify engineering competence.
- Browser Python execution requires a network connection at first use and may be restricted by browser security policies; copy the code to a local notebook when unavailable.
- Formula-based custom labs deliberately restrict the allowed expressions to known presets; this is not a general-purpose Python plugin interface.
- The initial direct-file (`file://`) experience can have browser-dependent storage restrictions. Use `localhost` for the most predictable local experience.
