# Ori Cheatsheet · v2

One page of rules. Enough for content edits and layout tweaks. For new
documents read `references/design.md`; tokens are canonical in
`tokens/ori.css`. Source: *Socialtrait Brand Concept Guidelines V2*.

## The ten invariants (memorize)

1. **Light for function, dark for moments.** Read-pages on Horizon
   `#FAFAFA`; Solar Horizon / Real Black only for covers, heros, statements,
   closes. Print body pages are always light.
2. **One signal:** Seagrass `#BAFE81`, ≤1 dominant use per page/slide/viewport
   (the 8px signal dot on insight/takeaway labels doesn't count). On light
   it's a fill under black ink — never text, never a line.
3. **Atmosphere, not decoration:** blues live in the four horizons and in
   data. Headlines are never blue. No other gradients.
4. **One family, many widths:** SF Pro (fallback Archivo). Wide cuts
   (118–132) display, width 100 reads. No serif, no italics, no mono (except code).
5. **Sentence case** headlines; uppercase only for kickers, labels, folio.
6. **Numbers are figures:** tabular everywhere; key figures in the wide cut.
7. **Open layouts:** 1px hairlines + whitespace, flush left. No boxed sections.
8. **Slight radii:** 4 · 8 · 12 · 24px. Circles only for dots and avatars.
9. **Depth is earned:** soft cool shadows on photos & screen cards; glow is
   Seagrass-only.
10. **Folio on every page:** hairline · lockup · legal line · page no. Logo is
    black or white, never colored. (Resumes: unbranded folio.)

## Colors

| | | | |
|---|---|---|---|
| **Real Black `#1F2937`** text / dark | Dust `#535B65` secondary | Mist `#80868F` captions | Cloud `#CCCED1` strong rule |
| **Horizon `#FAFAFA`** canvas | Paper `#FFFFFF` cards | Fog `#F1F2F4` panels | Rule `#E3E5E8` hairline |
| **Seagrass `#BAFE81`** signal | Day-deep `#2F5BCC` links | Pos `#2F7A12` · Neg `#C23B32` | Warn `#9A6206` |

**Solar Horizon** (`.horizon.dawn|day|dusk|twilight`): Dawn `#314188`
(hero direction, default) · Day `#3E6FE7` (**Real Black text**) · Dusk
`#2A2759` · Twilight `#070B2F`. White text on Dawn/Dusk/Twilight.

## Type (SF Pro → Archivo; width = `font-stretch`)

| Brand style | Size·weight·width | Use | Slides | Print |
|---|---|---|---|---|
| H1 Headline | 128·590·132 | display, covers | 76px | 40pt |
| H2 Headline | 96·700·132 | big statements | 60px | — |
| H3 Wide | 64·510·118 | slide titles, quotes | 44px | 26pt (doc title, w132) |
| H3 | 64·400·110 | chapter openers | 140px+ | 96pt+ |
| H4 Wide | 36·650·118 | section headlines | 26px | 15pt |
| H4 | 36·650·100 | sub-sections | 20px | 11pt |
| Body 1 | 18·591·120 | labels/kickers/UI (caps +.06em at 12px) | 12px | 7pt |
| Body 2 | 18·400·100 | reading text | 18px | 9.5pt |

Emphasis = weight 650. Seagrass marker `.hl` under ≤3 words or one number per
page. Kicker = 14px/9pt, 700, caps. Metric value = H1 cut.

## Spacing & geometry

8px base: 4 · 8 · 12–16 · 20 · 24 · 32–48 · 64–128 (landing). Print ≈ ×0.75pt.
Radii `--r-xs 4` marker/tags · `--r-s 8` print callouts · `--r-m 12`
buttons/cards · `--r-l 24` photos/hero panels.

Margins: One-pager 14·16·12·16mm · Long doc 18·20·14·20 · Report 16·18·14·18 ·
Resume 12·14·10·14 · Minutes 16·18·14·18 · Slides 1280×720 pad 56/72/40 ·
Landing max-w 1200px.

## Signature moves

- **Page head:** bold caps kicker top-left (`INSIGHT REPORT`), quiet Mist meta
  right. No rule under it.
- **Section head:** Cloud hairline → caps index (`01` black + topic mist) →
  assertion in H4 Wide.
- **Seagrass signal:** `.hl` marker · `.metric.key` · `.signal` glowing chip
  (dark) · `.signal-dot` · Seagrass primary button (dark). One per surface.
- **Folio:** Cloud hairline; lockup left; `CONFIDENTIAL MATERIAL. SOCIALTRAIT ©
  2026. ALL RIGHTS RESERVED.` centered; doc-id + `02 / 08` right.
- **Chapter opener:** Fog page, giant numeral + one word, bottom-left. Long
  docs and decks ≥12 slides only.
- **Horizon moment:** full-bleed atmosphere, centered lockup + wide title
  (the guideline cover). One per print doc (its cover).

## Components, fast

| Need | Do |
|---|---|
| KPI row | `.metric-row` 3–4 cells, hairline seams, label above value; one `.key` |
| Tag | Body 1 caps on Fog, 4px; `.signal-tag` once; `.outline` neutral |
| Table | caps Mist head over Cloud rule, Rule rows, `.num` right tabular; total = 1px black top |
| Conclusion | `.callout.insight` (Fog, Seagrass dot label) — one per section |
| The ask | `.callout.ask` — Real Black panel, Cloud label, once per doc |
| Risk | `.callout.risk` / `.warn` — 3px inset semantic bar |
| Quote | H3 Wide cut ~26px, ≤34ch, caps Mist cite; persona quotes cite persona |
| Persona | Paper card 12px, shadow on screen / hairline in print, Fog avatar |
| Key–value | `.spec` — Mist labels left, values right, Rule under each row |
| Timeline | Cloud spine, open dots; current `.now` = Seagrass |
| Photo | `.photo` 24px radius + soft shadow; `.soft` = progressive blur edge |
| Button | 12px radius; light: Real Black; dark: Seagrass + glow. One primary per viewport |
| Code | inline Fog chip · block Real Black panel 12px |

## Charts

Light: `#3E6FE7` → `#314188` → `#9DB8F5` → `#CCCED1`; highlight one series in
Day. Dark: highlight Seagrass, others white 55%/30%. Gridlines 1px `#E3E5E8`
horizontal only; baseline `#CCCED1`. Bars 3px rounded tops, gap ≥40%. Lines
2.5px round. Direct labels (≤3 series). Caption: **Fig 01** + sentence +
`Source:` right in Mist.

## Quick decisions

| Need | Use |
|---|---|
| Page background | Horizon `#FAFAFA` (Fog for chapter openers) |
| Cover / hero | `.horizon.dawn` unless there's a reason |
| Dark slide with real text | `.dark` (Real Black), not a horizon |
| Emphasize a number | wide cut + `.hl` (if it's THE number) — never blue text |
| Two Seagrass things? | remove one |
| Text on Day horizon | Real Black, always |
| Photos? | screen + long-doc evidence only; bright, real, 24px radius, shadow |
| Divide sections | hairline + index (section head), not boxes |
| Editable / Google Docs · Slides | `scripts/ori_docx.py` / `ori_pptx.py` (Archivo) |
| Logo color | black on light & Day; white on Dawn/Dusk/Twilight/Real Black |

**First principles:** light does the work, dark makes the moment, width gives
the voice, hairlines hold the structure, and Seagrass marks what matters.
