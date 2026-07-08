# Ori — the Socialtrait document design system

**Ori** (織, *weave*) is Socialtrait's constraint-based design system for
documents. It gives AI agents — and humans — a fixed visual language so that
every one-pager, report, deck, resume, and landing page we produce looks
deliberate, branded, and publishable without a designer in the loop.

The premise (borrowed from systems like [Kami](https://github.com/tw93/Kami)):
agents are already good at content; what they lack is **constraint**. Ori
supplies the constraints and nothing else. Where Kami reads like warm paper —
parchment, serif, editorial calm — Ori reads like a precision instrument:
cool graph-paper surfaces, grotesque sans + mono data, hairline structure,
one Signal Blue accent, and the node-and-thread motif drawn from the
interlaced Socialtrait mark.

## Browse it live

| Artifact | Live preview | Source |
|---|---|---|
| **Specimen — the full style guide** | [specimen.html](https://socialtrait.github.io/Ori/specimen.html) | [view](https://github.com/socialtrait/Ori/blob/main/specimen.html) |
| One-pager | [templates/one-pager.html](https://socialtrait.github.io/Ori/templates/one-pager.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/one-pager.html) |
| Long doc (white paper) | [templates/long-doc.html](https://socialtrait.github.io/Ori/templates/long-doc.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/long-doc.html) |
| Insight report | [templates/report.html](https://socialtrait.github.io/Ori/templates/report.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/report.html) |
| Slides (1280×720) | [templates/slides.html](https://socialtrait.github.io/Ori/templates/slides.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/slides.html) |
| Resume | [templates/resume.html](https://socialtrait.github.io/Ori/templates/resume.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/resume.html) |
| Landing page | [templates/landing-page.html](https://socialtrait.github.io/Ori/templates/landing-page.html) | [view](https://github.com/socialtrait/Ori/blob/main/templates/landing-page.html) |

Start with the **specimen** — it demonstrates every rule by obeying it. The
print artifacts (one-pager, long doc, report, resume) are fixed A4 pages, so
view them on a desktop; print-to-PDF from the browser to see true pagination.

## The look, in one paragraph

Frost `#FAFBFE` canvas, never warm. Inter Display headings in sentence case,
IBM Plex Mono for every label and every number that matters. One accent —
Signal Blue `#2F80ED` — rationed to about 2% of the page. Structure comes
from 1px hairlines and the signature **thread rule**: a 2px line that starts
with a 6px blue node square, opening every section under a mono eyebrow like
`01 · AUDIENCE SIGNAL`. Sharp corners, flat surfaces, flush-left text,
metrics set huge in mono. Dark "night" sections (`#02122A`) exist only on
screens — heros and slide covers. The accent and navy are taken straight
from the official logo assets, the neutrals from socialtrait.ai's CSS, so
output matches the brand by construction.

## Repository map

```
Ori/
├── SKILL.md                    ← agent entrypoint: workflow, artifact map, contracts
├── CHEATSHEET.md               ← one page of rules; read this tier most often
├── README.md                   ← you are here
├── specimen.html               ← living style guide; open in a browser
├── tokens/
│   └── ori.css                 ← canonical tokens + core components
├── references/
│   ├── design.md               ← full spec: invariants, color, type, layout, components, charts
│   ├── writing.md              ← content quality bars per artifact
│   └── anti-patterns.md        ← banned list + pre-ship checklist
├── templates/
│   ├── one-pager.html          ← exec brief; the metric row is the argument
│   ├── long-doc.html           ← white paper / spec, with cover recipe
│   ├── report.html             ← insight report: claim + evidence + "so what"
│   ├── slides.html             ← 1280×720 deck; night cover, pinned takeaways
│   ├── resume.html             ← dense single-page CV
│   └── landing-page.html       ← responsive marketing page; night hero
└── assets/
    └── logo/                   ← official mark + wordmark (blue/white/black)
```

## How agents use it

1. **Read `SKILL.md`** (or install this folder as a Claude Code skill — the
   frontmatter is already skill-compatible).
2. Pick the artifact from the request → copy the matching template.
3. **Edit body content only.** Template CSS is law; tokens change only in
   `tokens/ori.css`.
4. Fill every `<!-- SLOT -->`, delete unused optional blocks, obey the
   density contract.
5. Run the `references/anti-patterns.md` checklist, render, deliver
   HTML + PDF.

To render PDFs: `chrome --headless --print-to-pdf=out.pdf template.html`
(or WeasyPrint). Slides print at their native 1280×720 page size.

## The ten invariants (summary)

1. Cool canvas — Frost, never warm
2. One accent — Signal Blue `#2F80ED`
3. Sans + mono only; serif and italics banned
4. Meaningful numbers are mono tabular
5. 1px hairlines; the only thick line is the 2px thread
6. The blue node square: ≥1× per page, ≤1× per component
7. Flush-left axis; centering only on slide covers and heros
8. Sharp geometry: radius 0/2/6px, nothing rounder
9. Flat: no print shadows, one sanctioned gradient (night hero glow)
10. Color means data: green/red for deltas only

**First principles:** ink argues, mono measures, hairlines structure,
whitespace paces, and blue points at what matters.

---

Ori v1.0 · maintained by Socialtrait · tokens keyed to the official logo assets + socialtrait.ai
