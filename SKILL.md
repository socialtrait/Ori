---
name: ori
description: >
  Typeset Socialtrait documents, one-pagers, reports, slide decks, resumes,
  and landing pages in Ori — Socialtrait's document design system (cool
  graph-paper surfaces, Inter Display + IBM Plex Mono, Signal Blue #2F80ED,
  node-and-thread structure). Use whenever asked to make a doc, deck,
  one-pager, insight report, exec summary, PDF, resume/CV, memo, or landing
  page "in our style" / "for Socialtrait" / "presentable".
---

# Ori — Socialtrait document skill

You are typesetting a Socialtrait artifact. Ori is a constraint system:
your job is to pour good content into fixed structure, not to design. The
design decisions are already made and live in `CHEATSHEET.md`,
`references/design.md`, and `tokens/ori.css`.

**Prime directive: copy a template, edit body content only.** Never write
an Ori HTML file from scratch, never modify template CSS except where a
template marks a `<!-- TUNE -->` block.

## Trigger phrases

make this presentable · one-pager · exec summary · insight report ·
audience report · white paper · long doc · deck / slides / PPT · resume /
CV · landing page / microsite · turn this into a PDF · Socialtrait-brand
doc · persona report · pitch page

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
| Resume content | `references/writing.md` §Resume |
| Pre-ship review | `references/anti-patterns.md` checklist |

## Step 4 — Materials & sources

- **Facts:** verify names, dates, metrics against provided material. A
  number without a source becomes a magnitude ("~40%") or is cut. Never
  fabricate metrics, quotes, logos, or testimonials.
- **Logo:** templates already embed the official mark (meta rails) and
  wordmark (cover imprints) inline — leave them exactly where they are.
  Never add more logo instances, and never use the logo as a watermark.
- **Personas/quotes:** quotes from Socialtrait simulations are cited to the
  persona (`— MAYA · SIMULATED GEN-Z SHOPPER`), never passed off as human
  research.
- Report status one-shot before writing: `LOGO OK · METRICS 3/4 SOURCED ·
  IMAGES not required` — then proceed.

## Step 5 — Fill content

- Copy the template into the working directory; keep
  `<meta name="generator" content="Ori">`.
- Fill `<!-- SLOT: ... -->` regions. Delete unused optional blocks —
  never leave placeholder text.
- Follow `references/writing.md` quality bars per artifact.
- Sequential section numbering in eyebrows: `01`, `02`, …
- Set real dates (YYYY-MM-DD), doc-id (`ST-<TYPE>-<NNN>` or slug), page
  counts in footers.

### Density contracts (hard rules)

| Artifact | Contract |
|---|---|
| One-pager | Exactly 1 page: meta rail + H1 + lede + 3–4 metric row + 2–3 threaded sections + footer. Overflow → cut content, never shrink type. |
| Long doc | Cover recipe + numbered chapters; each body page 60–85% full, ≤1 figure per page, 2–4 paragraphs per chapter minimum. |
| Report | Each section: assertion H2 + one evidence shape (chart/table/persona grid) + one insight strip. 3–6 sections. |
| Slides | 1 assertion title (≤2 lines) + 1 evidence shape + pinned takeaway bar per slide. 3–5 content items max. 10–16 slides typical. |
| Resume | 1 page (2 max). Every bullet: Action + Scope + Result + Outcome, one line. 3–5 bullets per role. |
| Landing | Hero + 3–6 sections + final CTA. One primary button per viewport. Sections alternate frost/white; night for hero and/or final CTA only. |

### Slide-specific rules

- **Ghost test:** slide titles read in sequence must carry the whole argument.
- One evidence shape per slide — split slides that mix chart + table.
- No section-divider slides; the eyebrow index does that job.
- Takeaway bar pinned at bottom: wash strip, mono `TAKEAWAY` label.
- Slide figures fit a fixed budget: charts ≤300px tall (the template caps
  this). A chart that needs more room gets its own slide, full width.
- Cover and closing slides are night; body slides are frost.

## Step 6 — Verify before delivering

1. Render (headless Chrome `--print-to-pdf` for print artifacts; open in
   browser for landing).
2. Check: no placeholder text; every figure has data + caption + source;
   page fills 60–85%; footers paginate correctly; exactly one blue hero
   metric per page; node square present; no invariant violations
   (run `references/anti-patterns.md` list).
3. Deliver: HTML + PDF for print artifacts; HTML for landing; state any
   missing materials.

## Feedback protocol

When the user gives vague visual feedback ("feels cramped", "too plain"),
answer with current values and two concrete options, e.g.: "Section gap is
48px. (a) 64px gaps and drop one section, or (b) keep 48px and cut the
third metric row?" Never silently drift from tokens — if the user insists
on off-system styling, apply it and label the file `*-offsystem.html`.

## What Ori is NOT for

Dark-mode documents · rainbow/multi-accent palettes · decorative stock
imagery · rounded-friendly "startup gradient" aesthetics · Material/Tailwind
default looks · animated dashboards (link a real dashboard instead).
