# Ori Design Specification

The complete rulebook. Read this tier when producing a **new document**, when a
layout decision isn't covered by `CHEATSHEET.md`, or when reviewing output
against the system. Tokens live canonically in `tokens/ori.css`.

Ori (織, *weave*) is Socialtrait's document design language: cool graph-paper
surfaces, a grotesque sans carried by Inter Display, mono-set data, hairline
structure, and a single Signal Blue accent. Where warm editorial systems read
like a printed book, Ori reads like a precision instrument — an annotated
diagram you'd trust with a decision.

---

## 1 · The Ten Invariants

Non-negotiable. Any output violating one of these is not Ori.

1. **Cool canvas.** Page background is Frost `#FAFBFE`. Pure white `#FFFFFF`
   only on lifted cards. Warm tones (cream, beige, parchment) never appear.
2. **One accent.** Signal Blue `#2F80ED` is the only accent. Navy `#213C60`
   is structure, not accent. If two things compete for blue, one loses it.
3. **Sans and mono only.** Prose is Inter (headings Inter Display); labels,
   metadata, captions, and data are IBM Plex Mono. Serif never appears.
4. **Data is mono.** Every number that carries meaning — metrics, table
   figures, dates in metadata, axis labels — is set in mono with
   `tabular-nums`. A proportional-figure KPI is a defect.
5. **Hairline discipline.** Structural lines are 1px `#E3E8F4`. The only
   permitted thick line is the 2px blue thread. Boxes never nest more than
   two borders deep.
6. **Node and thread.** Section rules, timeline markers, and footers carry
   the 6px blue node square — the system's signature. It appears at least
   once per page, and never more than once per component.
7. **Flush-left axis.** Text hangs from the left margin, ragged right.
   Centered text is permitted only on slide covers and landing-page heros.
   Justified text never.
8. **Sharp geometry.** Default corner radius is 0. Chips 2px, cards and
   buttons 6px — nothing rounder. No pills, no circles except avatars and
   chart dots.
9. **Flat by default.** Print artifacts have zero shadows. Screen artifacts
   may use exactly two: `--lift` at rest, `--hover` on interaction. No
   gradients, except the single radial night-hero glow (screen only).
10. **Color means data.** Green/red appear only on deltas and risk callouts.
    Blue marks emphasis and keys. Nothing is colored for decoration.

---

## 2 · Color

### 2.1 Palette

| Token | Hex | Role |
|---|---|---|
| `--frost` | `#FAFBFE` | Page canvas |
| `--paper` | `#FFFFFF` | Cards, lifted containers |
| `--wash` | `#EFF5FD` | Callout and insight-strip fill |
| `--tint` | `#E3EEFC` | Tag fill, chart series 5 |
| `--night` | `#02122A` | Dark section surface (screen only) |
| `--navy` | `#213C60` | Deep structural navy, chart series 2 |
| `--ink` | `#000416` | Primary text |
| `--slate` | `#4A4D5A` | Secondary text, ledes |
| `--mist` | `#8A94AB` | Tertiary text, captions, metadata |
| `--ink-n` / `--mist-n` | `#F4F7FF` / `#8FA0C2` | Text on night |
| `--blue` | `#2F80ED` | **Signal Blue** — the accent |
| `--blue-deep` | `#1160C6` | Hover, links on wash |
| `--blue-soft` / `--blue-faint` | `#7EAFF1` / `#B6D1F7` | Chart series 3–4 |
| `--pos` / `--neg` / `--warn` | `#0E8A5C` / `#D64545` / `#B7791F` | Deltas and cautions only |
| `--line` / `--line-strong` | `#E3E8F4` / `#C9D2E8` | Hairlines / header rules, axes |
| `--line-n` | `#14294D` | Hairlines on night |

Provenance: Signal Blue `#2F80ED` is the mark's stroke color and `#213C60`
is the wordmark's fill — both taken from the official logo assets in
`assets/logo/`, which are the brand authority. The neutrals (`#000416`,
`#4A4D5A`, `#02122A`, surfaces) come from socialtrait.ai's CSS; the blue
support ramp (`#1160C6`, `#7EAFF1`, `#B6D1F7`, `#E3EEFC`) is derived from
Signal Blue at fixed lightness steps. None are approximations.

### 2.2 Usage ratios

A finished page is roughly **90% neutral** (frost/paper/ink/slate/mist),
**8% line**, **2% blue**. If blue exceeds ~5% of the visual field, demote
instances: keep the thread nodes and the single most important metric,
return everything else to ink.

### 2.3 Blue placement priority

When rationing blue, keep it in this order (top survives):
1. Thread nodes and eyebrows (structural signature)
2. The one metric or figure the page argues for
3. The primary chart series
4. Links / primary button
5. Anything else → ink

### 2.4 Contrast floors

Body text ≥ 7:1 against its surface (`--ink` on `--frost` passes).
Secondary ≥ 4.5:1 (`--slate` passes). `--mist` is legal only at caption
sizes (≤ 11px screen / 8.5pt print) or in uppercase mono labels.
On night surfaces, body text is `--mist-n`, headings `--ink-n`; `--blue`
is too dark on night for small text — use `--blue-soft` for night eyebrows.

---

## 3 · Typography

### 3.1 Families

| Stack | Composition | Carries |
|---|---|---|
| `--display` | Inter Display → Inter → system sans | Headings, display, metric-adjacent titles |
| `--sans` | Inter → system sans | Body, UI, buttons |
| `--mono` | IBM Plex Mono → SF Mono → JetBrains Mono → Consolas | Labels, captions, metadata, code, every data numeral |

Inter Display is the brand font (used on socialtrait.ai). When it can't be
bundled, the stack degrades to system sans gracefully — do not substitute a
different personality (no geometric rounds, no humanist serifs).

**Banned:** serif faces anywhere; italics anywhere (emphasis = weight 600 or
Signal Blue); more than these three stacks in one artifact.

### 3.2 Scale

Screen px first; print pt in parentheses. Ratios are fixed — don't invent
intermediate sizes.

| Role | Size | Weight | Line-height | Tracking | Case |
|---|---|---|---|---|---|
| Display | 42px (32pt) | 650 | 1.05 | −0.015em | sentence |
| H1 | 29px (22pt) | 650 | 1.15 | −0.01em | sentence |
| H2 | 20px (15pt) | 600 | 1.25 | −0.008em | sentence |
| H3 | 15px (11.5pt) | 600 | 1.35 | 0 | sentence |
| Lede | 15px (11pt) | 400 | 1.55 | 0 | — |
| Body | 14px (10pt) | 400 | 1.6 | 0 | — |
| Small | 12.5px (9pt) | 400 | 1.5 | 0 | — |
| Caption (mono) | 11px (8.5pt) | 400 | 1.45 | +0.02em | — |
| Label (mono) | 10.5px (8pt) | 500 | 1.35 | +0.08em | UPPERCASE |
| Metric value (mono) | 32px (24pt) | 600 | 1.0 | −0.01em | — |

Floors: body never below 13px screen / 9.5pt print; mono micro-labels never
below 10px / 7.5pt. Headings are sentence case — Title Case and ALL-CAPS
headings are banned (uppercase belongs to mono labels only).

### 3.3 Rhythm

- Body measure: 60–70ch. Ledes max 62ch. Never full-bleed paragraphs on wide pages.
- Paragraph spacing: 12px; no first-line indents, ever.
- Dense table/list contexts may drop body line-height to 1.45, never lower.
- Numbers inside prose stay in the sans; numbers in tables, metrics, axes,
  and metadata go mono. The test: "would this number appear in a CSV?" → mono.

---

## 4 · Space & Layout

### 4.1 Spacing scale (8px base; print ≈ ×0.75 in pt)

| Step | Screen | Print | Use |
|---|---|---|---|
| xs | 4px | 3pt | inline gaps |
| sm | 8px | 6pt | label→value, chip padding |
| md | 12px | 9pt | paragraph gap |
| lg | 16px | 12pt | component interior |
| xl | 24px | 18pt | between components |
| 2xl | 32px | 24pt | after section blocks |
| 3xl | 48px | 36pt | between sections |
| 4xl | 64–96px | 48–72pt | landing sections, chapter breaks |

### 4.2 Page geometry

| Artifact | Size | Margins (T·R·B·L) |
|---|---|---|
| One-pager | A4 portrait | 14·16·14·16 mm |
| Long doc | A4 portrait | 18·20·20·20 mm |
| Report | A4 portrait | 16·18·18·18 mm |
| Resume | A4 portrait | 12·14·12·14 mm |
| Slides | 1280×720 px fixed | padding 64px 72px |
| Landing | fluid | content max-width 1120px; sections 96px 64px (mobile 64px 20px) |

### 4.3 Grid

Think in a 12-column grid, 24px gutters. Sanctioned splits:
- **Full** (12) — prose, tables, charts
- **7/5** — text + supporting figure or persona stack
- **4×3** — metric rows (the `.metric-row` grid handles this)
- **2×6** — card pairs

Asymmetric splits always put text in the wider column. Three-column body
text is banned (too narrow at A4).

### 4.4 Density contract

Every rendered page must land at **60–85% vertical fill**. Below 55%: merge
the page upward or promote a list to a table/figure. Above 90%: split.
Sparse final pages are merged into the previous page rather than padded.

---

## 5 · Signature Elements

These make a page recognizably Ori. Use all of #1–3 on every artifact.

### 5.1 Meta rail
First element on every page/slide/section-top:

```html
<div class="meta-rail">
  <span class="brand">Socialtrait</span><span class="sep"></span>
  <span>Insight report</span><span class="sep"></span>
  <span>2026-07-07</span>
  <span class="right">Confidential</span>
</div>
```

Mono, 10.5px, uppercase, mist; brand name in ink. Bottom hairline. On the
right edge: classification, version, or author.

### 5.2 Eyebrow + thread rule
Every section opens with:

```html
<p class="eyebrow"><span class="idx">01</span>Audience signal</p>
<h2>Gen-Z shoppers trust creators over brands 3:1</h2>
<div class="thread"></div>
```

The thread is a 2px line: 48px of Signal Blue with a 6px node square at the
origin, continuing as hairline gray. Index numbers are two-digit mono
(`01`–`99`), colored mist inside the blue eyebrow.

### 5.3 Node footer
Every printed page ends with `.page-footer`: node square, mono coordinates
(`SOCIALTRAIT / ORI · <doc-id>`), page number right-aligned
(`02 / 08`, mono, zero-padded).

### 5.4 Weave watermark (covers and heros only)
The **official mark itself**, rendered as a watermark: inline the four
paths from `assets/logo/mark.svg` and stroke the group in the watermark
tone — `--tint` on light covers, `--line-n` on night surfaces. Never
invent arcs or redraw the mark; use the real path data so the knot stays
recognizable.

```html
<svg class="weave" viewBox="0 0 287 284" aria-hidden="true">
  <g fill="none" stroke="#E3EEFC" stroke-miterlimit="10">
    <!-- the four <path> elements from assets/logo/mark.svg,
         with their stroke-width attributes kept and stroke color removed -->
  </g>
</svg>
```

Sizing: 40–70% of page width, anchored to a corner behind content, cropped
by **at most ~30% per axis** — over-cropping reduces the mark to anonymous
arcs. Max one per artifact. Never on body pages. Copy the working blocks
from `templates/long-doc.html` (light) or `templates/slides.html` (night).

### 5.5 Night sections (screen artifacts only)
`.night` blocks — deep navy `#02122A` surface — for landing heros, slide
covers, and closing slides. Body pages of print artifacts never go dark.
Rhythm rule for landing pages: never two night sections adjacent.

---

## 6 · Components

### 6.1 Metric block
The workhorse. Grid of paper cells separated by 1px line seams (grid gap
trick: container background `--line`, gap 1px).

- Label: mono 10.5px uppercase mist, **above** the value
- Value: mono 32px/600 ink; unit suffix 16px mist
- Optional note row: 12px slate, may include a `.delta`
- The single most important metric on the page — and only that one — may
  color its value Signal Blue
- Row of 3 or 4; never 5+; labels ≤ 18 characters (trim, don't wrap)

### 6.2 Tag
Mono 10px uppercase, `--tint` fill, `--blue-deep` text, 2px radius,
2px×8px padding. Ghost variant (border, no fill) for neutral taxonomy.
Max 4 tags per cluster.

### 6.3 Table
- Headers: mono uppercase 10.5px mist, 1px `--line-strong` bottom rule
- Cells: 13px sans, 1px `--line` rules, no vertical rules, no zebra fill
- Numeric columns: class `data` → right-aligned mono 12.5px tabular
- Total rows: 2px ink top border, weight 600
- Column count ≤ 6 portrait A4; beyond that, split the table or rotate the artifact

### 6.4 Callout / insight strip
Wash fill, 2px blue left thread, mono label (`INSIGHT`, `SO WHAT`,
`METHOD`, `CAVEAT`). Variants: `.warn` (amber), `.risk` (red). One insight
strip per report section — it is the section's conclusion, not decoration.

### 6.5 Quote
2px `--line-strong` left rule, 15px text, mono uppercase cite prefixed with
a blue em-dash. For research/verbatim quotes from Socialtrait audience
simulations, attach the persona name in the cite.

### 6.6 Persona card
Socialtrait-native. 44px circular avatar in `--tint` with mono initials,
name (600), role line (mist), trait tags, one representative quote.
Grid rows of 2–3. Avatars are the only sanctioned circles.

### 6.7 Timeline
2px hairline spine, node squares at entries, mono `when` label above sans
`what`. Vertical only in documents; horizontal variant allowed on slides.

### 6.8 Code
Inline: wash fill, hairline border, 2px radius. Block: night surface,
`--ink-n` text, 12px mono, 6px radius — the only night element allowed
inside print artifacts.

### 6.9 Buttons (landing only)
Primary: blue fill, white text, 6px radius, 13px×22px padding. Ghost:
hairline border. Exactly one primary button visible per viewport. No pill
buttons, no shadows on buttons, no icon-only buttons.

### 6.10 Icons
Single-line stroke icons only: 1.5px stroke, `currentColor`, 16 or 20px
grid, squared joins where possible. No filled icons, no emoji as icons,
no icon backgrounds. If a concept has no obvious line icon, use a mono
label instead — text beats a weak metaphor.

---

## 7 · Charts

Inline SVG, drawn to these conventions (no chart libraries in print
artifacts):

- **Series ramp (in order):** `#2F80ED` → `#213C60` → `#7EAFF1` →
  `#B6D1F7` → `#E3EEFC` (last with 1px `#C9D2E8` stroke). One highlighted
  series in blue; comparators muted.
- **Gridlines:** horizontal only, 1px `#E9EDF6`; axis line bottom only, 1px
  `#C9D2E8`. No plot-area border, no background fill.
- **Labels:** axis mono 10px `#8A94AB`; value labels mono 11px ink,
  tabular. Label the ends of lines directly instead of legends when ≤ 3 series.
- **Bars:** radius 0, gap ≥ 40% of bar width, ≤ 8 categories × 3 series.
- **Lines:** 2px stroke, dots 3.5px white-filled with 2px series stroke,
  ≤ 12 points × 3 series.
- **Donut:** stroke-ring construction, ≤ 5 segments, mono metric centered.
- **Deltas:** the only place `--pos`/`--neg` appear in a chart.
- Every figure gets a `.figcap`: `FIG 01` in blue + sentence caption +
  source (`SOURCE: <name>`, mono).

Chart choice: distribution ≤ 5 parts → donut; category comparison → bar;
trend over time → line; 2×2 strategic → quadrant; decomposition → waterfall
(sharp bars, blue positive segments, navy negative); flows/decisions →
flowchart of hairline boxes with node-square connectors.

---

## 8 · Motion (screen artifacts only)

- Durations: 150ms (hover) / 300ms (entrance). Easing `cubic-bezier(.2,.6,.2,1)`.
- Entrances: fade + 12px rise, once, on scroll into view. No loops, no
  parallax, no typewriter effects.
- Respect `prefers-reduced-motion: reduce` — collapse all motion to opacity.
- Print artifacts: zero motion, obviously.

---

## 9 · Logo usage

- Official assets live in `assets/logo/`: `mark.svg` / `wordmark.svg`
  (Signal Blue `#2F80ED`, wordmark navy `#213C60`), plus `-white` and
  `-black` variants of each. Use `mark-white.svg` / `wordmark-white.svg`
  on night surfaces.
- Mark renders in Signal Blue on light surfaces, white on night. Never
  recolor, outline, shadow, or rotate.
- Clear space: one petal-width on all sides. Minimum size 20px/15pt.
- Documents: mark only (top-left of meta area or footer). Wordmark reserved
  for covers, slide covers, and landing navs.
- Never set the company name in the wordmark's style using live text —
  it's an asset, not typography.

---

## 10 · Print & build notes

- Templates carry `@page` rules; render via headless Chrome
  (`chrome --headless --print-to-pdf=out.pdf file.html`) or WeasyPrint.
- Colors must survive grayscale: check that blue (#2F80ED ≈ 45% gray) still
  contrasts with mist text and hairlines. Never encode meaning in hue alone —
  pair color with position, label, or weight.
- Embed fonts if the toolchain supports it; else system fallbacks apply.
- PDF metadata: title = document H1; author = requester or "Socialtrait";
  keywords 3–5; description ≤ 150 chars.
- All templates include `<meta name="generator" content="Ori">` — keep it.
