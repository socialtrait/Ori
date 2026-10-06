# Ori — the Socialtrait document design system · v2

**Ori** (織, *weave*) is Socialtrait's constraint-based design system for
documents. It gives AI agents — and humans — a fixed visual language so that
every one-pager, report, deck, resume, minutes, and landing page we produce looks
deliberate, branded, and publishable without a designer in the loop.

The premise (borrowed from systems like [Kami](https://github.com/tw93/Kami)):
agents are already good at content; what they lack is **constraint**. Ori
supplies the constraints and nothing else.

**v2 is a complete revamp** onto the *Socialtrait Brand Concept Guidelines V2*
(2026-08-26): the refined logo, SF Pro's wide cuts as the brand voice, light
Horizon pages for function, Solar Horizon atmospheres for moments, and a
single Seagrass signal. The v1 look (Frost canvas, Inter + Plex Mono, Signal
Blue, node-and-thread) is retired.

## Browse it live

| Artifact | Live preview | Source |
|---|---|---|
| **Specimen — the full style guide** | [specimen.html](https://socialtrait.github.io/Ori/specimen.html) | [view](https://github.com/socialtrait/Ori/blob/main/specimen.html) |
| One-pager | [templates/one-pager.html](https://socialtrait.github.io/Ori/templates/one-pager.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/one-pager.html) |
| Long doc (white paper) | [templates/long-doc.html](https://socialtrait.github.io/Ori/templates/long-doc.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/long-doc.html) |
| Insight report | [templates/report.html](https://socialtrait.github.io/Ori/templates/report.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/report.html) |
| Slides (1280×720) | [templates/slides.html](https://socialtrait.github.io/Ori/templates/slides.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/slides.html) |
| Resume | [templates/resume.html](https://socialtrait.github.io/Ori/templates/resume.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/resume.html) |
| Meeting minutes | [templates/meeting-minutes.html](https://socialtrait.github.io/Ori/templates/meeting-minutes.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/meeting-minutes.html) |
| Landing page | [templates/landing-page.html](https://socialtrait.github.io/Ori/templates/landing-page.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/landing-page.html) |

Start with the **specimen** — it demonstrates every rule by obeying it. The
print artifacts (one-pager, long doc, report, resume, minutes) are fixed A4
pages; print-to-PDF from the browser to see true pagination.

## The look, in one paragraph

Horizon `#FAFAFA` pages for anything people read, Real Black `#1F2937` ink,
Dust and Cloud greys, structure from 1px hairlines and open space. Headlines in
**SF Pro's wide cuts** (width 118–132; Archivo stands in where SF Pro isn't
installed), reading text at normal width, everything tabular. Key moments —
covers, heros, statement and closing slides — move to the **Solar Horizon**:
Dawn, Day, Dusk, Twilight, soft-focus skies with a glowing horizon line. One
accent, **Seagrass** `#BAFE81`, marks the single thing each page argues: a
marker under a number, a glowing chip on a horizon. Corners are slightly
softened; photos are bright and real, with large radii, a cool shadow, and a
softly blurred edge. Every page closes with the guideline's folio: hairline,
lockup, legal line, page number.

## Repository map

```
Ori/
├── SKILL.md                    ← agent entrypoint: workflow, artifact map, contracts
├── CHEATSHEET.md               ← one page of rules; read this tier most often
├── README.md                   ← you are here
├── specimen.html               ← living style guide; open in a browser
├── tokens/
│   └── ori.css                 ← canonical tokens + core components (v2)
├── references/
│   ├── design.md               ← full spec: invariants, color, type, layout, components, charts, photos, logo
│   ├── writing.md              ← content quality bars per artifact
│   ├── office.md               ← docx/pptx translation spec (Google Docs/Slides workflow)
│   └── anti-patterns.md        ← banned list + pre-ship checklist
├── templates/
│   ├── one-pager.html          ← exec brief; the metric row is the argument
│   ├── long-doc.html           ← white paper / spec: Dawn cover, chapter openers
│   ├── report.html             ← insight report: claim + evidence + insight
│   ├── slides.html             ← 1280×720 deck: light evidence, dark moments
│   ├── resume.html             ← dense single-page CV (unbranded)
│   ├── meeting-minutes.html    ← TL;DR, decisions (D-ids), actions (A-ids)
│   └── landing-page.html       ← responsive marketing page; Dawn hero
├── scripts/
│   ├── ori_docx.py             ← Ori-native Word generator (docx → Google Docs)
│   └── ori_pptx.py             ← Ori-native PowerPoint generator (pptx → Google Slides)
└── assets/
    ├── logo/                   ← refined 2026 lockup, mark, wordmark (SVG, PNG, inline symbols)
    └── horizon/                ← Solar Horizon originals (Dawn, Day, Dusk, Twilight)
```

## How agents use it

1. **Read `SKILL.md`** (or install this folder as a Claude Code skill — the
   frontmatter is already skill-compatible).
2. Pick the artifact from the request → copy the matching template.
3. **Edit body content only.** Template CSS is law; tokens change only in
   `tokens/ori.css`.
4. Fill every `<!-- SLOT -->`, delete unused optional blocks, obey the
   density contract, place the page's one Seagrass signal.
5. Run the `references/anti-patterns.md` checklist, render, and deliver
   per the `references/office.md` contract (HTML + PDF, plus DOCX/PPTX
   where those are native).

To render PDFs:
`chrome --headless --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=out.pdf template.html`
(the time budget lets the Archivo webfont load). Slides print at their native
1280×720 page size. For editable internal sharing, `.docx` and `.pptx` are
**native outputs** generated straight from the tokens — upload to Google Docs /
Slides; spec in `references/office.md`.

## Typeface

The brand typeface is **SF Pro** (installer in the brand Drive folder,
`_Typeface/SF-Pro.dmg`). SF Pro can't be web-served, so every template also
loads **Archivo** (open-licensed, Google Fonts) — its 62–125 width axis is the
closest free match to SF Pro's wide cuts. Install SF Pro locally to see the
true brand face; everyone else, and every headless PDF build, gets Archivo.

## The ten invariants (summary)

1. Light for function, dark for moments
2. One signal — Seagrass `#BAFE81`, once per surface, a fill on light
3. Atmosphere, not decoration — blues live in the Solar Horizons and data
4. One family, many widths — SF Pro (Archivo fallback); no serif, no italics
5. Sentence-case headlines; caps only for kickers, labels, folio
6. Numbers are tabular figures; key figures in the wide cut
7. Open layouts — hairlines and whitespace, never boxed sections
8. Slight radii — 4 · 8 · 12 · 24px
9. Depth is earned — soft cool shadows on photos and cards; glow is Seagrass-only
10. The folio closes every page; the logo is black or white

**First principles:** light does the work, dark makes the moment, width gives
the voice, hairlines hold the structure, and Seagrass marks what matters.

---

Ori v2.0 · maintained by Socialtrait · built on Brand Concept Guidelines V2 (2026-08-26)
