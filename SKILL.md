---
name: ori
description: >
  Typeset Socialtrait documents, one-pagers, reports, slide decks, resumes,
  meeting minutes, and landing pages in Ori v2 — Socialtrait's design system
  built on the 2026 Brand Guidelines (refined logo, SF Pro wide type, Horizon
  #FAFAFA light pages, Solar Horizon atmospheres, one Seagrass #BAFE81
  signal). Use whenever asked to make a doc, deck, one-pager, insight report,
  exec summary, PDF, resume/CV, memo, meeting minutes/MoM, or landing page
  "in our style" / "for Socialtrait" / "on brand" / "presentable".
---

# Ori — Socialtrait document skill · v2

You are typesetting a Socialtrait artifact. Ori is a constraint system:
your job is to pour good content into fixed structure, not to design. The
design decisions are already made and live in `CHEATSHEET.md`,
`references/design.md`, and `tokens/ori.css` — all derived from the
*Socialtrait Brand Concept Guidelines V2* (2026-08-26).

**Prime directive: copy a template, edit body content only.** Never write
an Ori HTML file from scratch, never modify template CSS except where a
template marks a `<!-- TUNE -->` block.

## Trigger phrases

make this presentable · on brand · one-pager · exec summary · insight report ·
audience report · white paper · long doc · deck / slides / PPT · resume /
CV · landing page / microsite · turn this into a PDF · Socialtrait-brand
doc · persona report · pitch page · meeting minutes / MoM / sync recap

## Step 1 — Intent

Establish four dimensions (ask only if ≥2 are missing; otherwise infer
silently and proceed):

1. **Purpose** — decide / inform / persuade / recruit
2. **Audience** — exec, customer, investor, candidate, engineer
3. **Constraint** — length, deadline, confidentiality, delivery format
4. **Success** — what the reader should do after reading

## Step 2 — Pick the artifact

| Signal in request | Artifact | Template |
|---|---|---|
| one-pager, exec summary, brief, memo-with-numbers | One-pager | `templates/one-pager.html` |
| white paper, spec, proposal, long-form, multi-chapter | Long doc | `templates/long-doc.html` |
| insight report, audience report, persona findings, chart-heavy analysis | Report | `templates/report.html` |
| deck, slides, PPT, presentation, pitch | Slides | `templates/slides.html` |
| resume, CV, candidate profile | Resume | `templates/resume.html` |
| meeting minutes, meeting notes, MoM, sync recap | Minutes | `templates/meeting-minutes.html` |
| landing page, microsite, launch page, waitlist page | Landing | `templates/landing-page.html` |

Ambiguous "report" → if the argument is charts/evidence, use Report; if
it's chapters of prose, use Long doc. Ambiguous "doc" → One-pager if it
fits one page (it usually should).

## Step 3 — Load the right spec tier

| Task | Read |
|---|---|
| Content edit in existing artifact | `CHEATSHEET.md` only |
| Layout tweak | `CHEATSHEET.md` + the template's comments |
| New document | `CHEATSHEET.md` + `references/design.md` + `references/writing.md` |
| Charts/figures needed | `references/design.md` §7 |
| Photos involved | `references/design.md` §8 |
| Resume content | `references/writing.md` §Resume |
| Pre-ship review | `references/anti-patterns.md` checklist |
| Office outputs (docx/pptx) | `references/office.md` + `scripts/ori_docx.py` / `ori_pptx.py` |

## Step 4 — Materials & sources

- **Facts:** verify names, dates, metrics against provided material. A
  number without a source becomes a magnitude ("~40%") or is cut. Never
  fabricate metrics, quotes, logos, or testimonials.
- **Logo:** templates already inline the refined lockup (folio on every page,
  cover lockup) via `assets/logo/symbols.html` — leave it where it is. Never
  add instances, recolor it, or use the retired blue logo.
- **Photos:** only real, bright, natural-light photographs, treated per
  design.md §8. No photo available → no photo (never a stock filler, never a
  placeholder box).
- **Personas/quotes:** quotes from Socialtrait simulations are cited to the
  persona (`— Maya · Simulated Gen-Z shopper`), never passed off as human
  research.
- Report status one-shot before writing: `LOGO OK · METRICS 3/4 SOURCED ·
  PHOTOS none` — then proceed.

## Step 5 — Fill content

- Copy the template into the working directory; keep
  `<meta name="generator" content="Ori 2">` and the Archivo font link.
- Fill `<!-- SLOT: ... -->` regions. Delete unused optional blocks —
  never leave placeholder text.
- Follow `references/writing.md` quality bars per artifact.
- Sequential section indexes: `01`, `02`, …
- Set real dates (YYYY-MM-DD), doc-id (`ST-<TYPE>-<NNN>` or slug), and
  folio page numbers (`02 / 08`).
- Place the page's **one Seagrass signal** on the thing the page argues.

### Density contracts (hard rules)

| Artifact | Contract |
|---|---|
| One-pager | Exactly 1 page, light: page head + title + lede + 3–4 metric row (one `.key`) + 2–3 sections + `.callout.ask` + folio. Overflow → cut content, never shrink type. |
| Long doc | Dawn horizon cover + contents + chapter openers (≥3 chapters) + body pages 60–85% full, ≤1 figure per page, folio every page. |
| Report | Light. Each section: assertion section-head + one evidence shape (chart/table/persona grid) + one `.callout.insight`. 3–6 sections. |
| Slides | Evidence slide = kicker + assertion title (≤2 lines) + one evidence shape + pinned takeaway + folio. 3–5 content items max. 10–16 slides; dark only for cover, 2–3 statements, close; chapter openers only when ≥12 slides (max 4). |
| Resume | 1 page (2 max), unbranded folio. Every bullet: Action + Scope + Result + Outcome, one line. 3–5 bullets per role. |
| Minutes | TL;DR (≤25 words) + logistics `.spec` + agenda + numbered topics with outcome headings + decisions (D-ids) + actions table (A-ids; owner + due always) + next meeting. 1–3 pages, light. |
| Landing | Dawn horizon hero (wide headline, Seagrass CTA) + 3–6 light sections + dark final CTA (Dusk/Twilight) + public folio. One primary button per viewport; never two horizons adjacent. |

### Slide-specific rules

- **Ghost test:** slide titles read in sequence must carry the whole argument.
- One evidence shape per slide — split slides that mix chart + table.
- **Light = functional** (evidence, most slides). **Dark = moment** (cover,
  statements, close) — more visuals than text.
- Takeaway pinned at bottom: hairline + bold `Takeaway` + one sentence; it
  usually holds the slide's Seagrass signal.
- Figures ≤300px tall; a chart that needs more gets its own slide.

## Step 6 — Verify before delivering

1. Render (headless Chrome `--print-to-pdf --virtual-time-budget=8000` for
   print artifacts so Archivo loads; browser for landing).
2. Check: no placeholder text; every figure has data + caption + source;
   pages 60–85% full; folio on every page with correct pagination; exactly
   one Seagrass signal per page; wide headlines actually rendering (not a
   system fallback); run the `references/anti-patterns.md` checklist.
3. Deliver, per artifact: print artifacts → HTML + PDF + **DOCX**
   (`scripts/ori_docx.py`); slides → HTML + PDF + **PPTX**
   (`scripts/ori_pptx.py`); landing → HTML. Office files are Ori-native —
   never ask whether the user wants "native or editable". The internal path
   is docx → Google Docs, pptx → Google Slides (see `references/office.md`).
4. State any missing materials.

## Feedback protocol

When the user gives vague visual feedback ("feels cramped", "too plain"),
answer with current values and two concrete options, e.g.: "Section gap is
48px. (a) 64px gaps and drop one section, or (b) keep 48px and move the
metric row onto a Dawn horizon band?" Never silently drift from tokens — if
the user insists on off-system styling, apply it and label the file
`*-offsystem.html`.

## What Ori is NOT for

Rainbow / multi-accent palettes · blue headlines · gradients other than the
Solar Horizons · glassmorphism and neon "AI" aesthetics · dark text-heavy
pages · stock imagery and 3D blobs · Material/Tailwind default looks ·
animated dashboards (link a real dashboard instead).
