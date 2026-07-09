# Ori Cheatsheet

One page of rules. Enough for content edits and layout tweaks. For new
documents read `references/design.md`; tokens are canonical in
`tokens/ori.css`.

## The ten invariants (memorize)

1. Canvas is Frost `#FAFBFE`; white only on cards; warm tones never.
2. One accent: Signal Blue `#2F80ED`. Navy is structure, not accent.
3. Sans (Inter/Inter Display) for prose, mono (IBM Plex Mono) for labels &
   data. Serif banned. Italics banned.
4. Every meaningful number: mono + `tabular-nums`.
5. Lines are 1px `#E3E8F4`; the only thick line is the 2px blue thread.
6. The 6px blue node square appears ≥1× per page, ≤1× per component.
7. Flush-left, ragged-right. Centering only on slide covers & landing heros.
8. Radius: 0 default, 2px chips, 6px cards max. No pills.
9. No shadows in print; screen gets `--lift`/`--hover` only. One gradient
   exists: the night-hero radial glow.
10. Green/red = deltas, action statuses, risk only. Blue = emphasis.
    No decorative color.

## Colors

| | | | |
|---|---|---|---|
| Frost `#FAFBFE` canvas | Paper `#FFFFFF` cards | Wash `#EFF5FD` callouts | Tint `#E3EEFC` tags |
| Ink `#000416` text | Slate `#4A4D5A` secondary | Mist `#8A94AB` captions | Line `#E3E8F4` rules |
| **Blue `#2F80ED` accent** | Blue-deep `#1160C6` hover | Night `#02122A` dark bg | Navy `#213C60` chart 2 |
| Pos `#0E8A5C` | Neg `#D64545` | Warn `#B7791F` | Line-strong `#C9D2E8` |

Page is ~90% neutral, ~8% line, ~2% blue. Blue priority when rationing:
thread/eyebrow → hero metric → primary chart series → links/button → ink.

## Type scale (screen px / print pt)

| Role | Size | W | LH | Notes |
|---|---|---|---|---|
| Display | 42/32 | 650 | 1.05 | −0.015em, Inter Display |
| H1 | 29/22 | 650 | 1.15 | sentence case, always |
| H2 | 20/15 | 600 | 1.25 | |
| H3 | 15/11.5 | 600 | 1.35 | |
| Lede | 15/11 | 400 | 1.55 | slate, ≤62ch |
| Body | 14/10 | 400 | 1.6 | ≥13px/9.5pt floor |
| Small | 12.5/9 | 400 | 1.5 | |
| Caption | 11/8.5 | 400 | 1.45 | mono, mist |
| Label | 10.5/8 | 500 | 1.35 | mono UPPERCASE +0.08em |
| Metric | 32/24 | 600 | 1.0 | mono tabular |

Emphasis = weight 600 or Signal Blue. Never italics, never underline
(underline is for links only). Blue emphasis ≤ a few words; sentence-length
emphasis is weight-only (long blue spans read as links).

## Spacing (8px base)

4 inline · 8 label→value · 12 paragraphs · 16 component interior ·
24 between components · 32 after blocks · 48 between sections ·
64–96 landing sections. Print ≈ ×0.75 in pt.

## Margins

One-pager 14·16·14·16mm · Long doc 18·20·20·20 · Report 16·18·18·18 ·
Resume 12·14·12·14 · Minutes 16·18·18·18 · Slides 1280×720px pad 56/72 ·
Landing max-w 1120px.

## Signature moves

- **Meta rail** (page top): mono uppercase `Socialtrait · <type> · <date>`,
  hairline below, classification right-aligned.
- **Section head**: `.eyebrow` (mono, blue, `01` index in mist) → H2 →
  `.thread` (2px: 48px blue + node square, then gray).
- **Node footer**: node square + `SOCIALTRAIT / ORI · <doc-id>` + `02 / 08`.
- **Logo**: mark leads the meta rail (12pt/16px; white on night); wordmark =
  cover imprint, bottom-left; resume unbranded. Never a watermark, never
  cropped, never tinted. Max 2 logo instances per page.
- **Night sections**: `#02122A`, screen artifacts only, never adjacent pairs,
  never in print body pages.

## Components, fast

| Need | Do |
|---|---|
| KPI row | `.metric-row` 3–4 cells, 1px seams, label above value, ≤18-char labels |
| Hero number | that one metric-value in blue; all others ink |
| Tag | mono 10px uppercase, tint fill, 2px radius; ≤4 per cluster |
| Table | mono uppercase headers, hairlines only, numeric cols right-mono, total = 2px ink top rule |
| Conclusion | `.callout` wash + 2px blue left + mono label (INSIGHT / SO WHAT) |
| Risk note | `.callout.risk` (red left rule) — text stays ink |
| Quote | 2px gray left rule; mono cite `— NAME`; persona quotes cite persona |
| Persona | `.persona`: tint avatar w/ mono initials, trait tags, one quote |
| Steps/history | `.timeline`: hairline spine + node squares + mono when |
| Slide header | evidence: 30px title + optional context stat/kicker right · statement: 44px display, 2–3/deck |
| Decisions / actions | `.decisions` D-ids + node · actions table A-ids, owner+due always, status chip (open/done/blocked) |
| Code | inline: wash chip · block: night bg, 12px mono, 6px radius |
| Button (landing) | primary blue fill 6px radius; one primary per viewport |
| Icon | 1.5px line stroke, currentColor; no fills, no emoji |
| Divider | 1px `--line`, or `.thread` if opening a section |

## Charts

Series: `#2F80ED` → `#213C60` → `#7EAFF1` → `#B6D1F7` → `#E3EEFC`+stroke.
H-gridlines 1px `#E9EDF6`; bottom axis 1px `#C9D2E8`; axis labels mono 10px
mist; values mono 11px ink. Bars: square corners, gap ≥40%, ≤8×3. Lines:
2px, white-filled dots, ≤12pts×3. Donut ≤5 segments, mono center metric.
Direct-label lines instead of legends when ≤3 series. Caption every figure:
`FIG 01` blue + sentence + `SOURCE:` mono.

## Density contract

Every page 60–85% full. <55% → merge up or promote list→table/figure.
>90% → split. Never pad, never orphan a heading at page bottom.

Per-artifact minimums: slide = 1 assertion title + 1 evidence shape +
pinned takeaway · report section = claim H2 + figure/table + insight strip ·
one-pager = header, lede, metric row, 2–3 sections, footer — exactly one
page · resume bullet = action+scope+result+outcome, one line.

## Quick decisions

| Need | Use |
|---|---|
| Page background | frost, always |
| Emphasize number | mono + blue, never bold-italic |
| De-emphasize | mist, only at caption sizes |
| Two things blue? | demote one to ink |
| Divide sections | thread rule, not whitespace alone |
| Wide table (>6 cols) | split it, or landscape artifact |
| Empty region | add evidence or merge — never a stock image |
| Dark mode? | no such thing; night sections are components |
| Editable / Google Docs · Slides | `scripts/ori_docx.py` / `ori_pptx.py` — docx & pptx ARE Ori-native |
| Rounded corners? | 0 / 2 / 6px. When in doubt, square |
| Which font for a date? | metadata → mono; prose sentence → sans |

**First principles:** ink argues, mono measures, hairlines structure,
whitespace paces, and blue points at what matters.
