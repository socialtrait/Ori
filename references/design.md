# Ori Design Specification · v2

The complete rulebook. Read this tier when producing a **new document**, when a
layout decision isn't covered by `CHEATSHEET.md`, or when reviewing output
against the system. Tokens live canonically in `tokens/ori.css`.

**Source of truth:** *Socialtrait Brand Concept Guidelines V2* (2026-08-26) —
the refined logo, the SF Pro type system, the Solar Horizon + Seagrass color
system, and the image treatment. Ori v2 is that guideline turned into
constraints an agent can obey. Where the guideline is silent (tables, charts,
document geometry), Ori extends it in the guideline's own logic.

The brand idea, in the guideline's words: built around **clarity, restraint,
and a sense of forward motion** — *what feels like the future has, in a sense,
already happened.* Open editorial layouts, calm instrument-grade typography,
and a color system that **moves between light and dark** depending on whether
a moment calls for **atmosphere or function**. Considered and timeless rather
than trend-driven.

Ori (織, *weave*) keeps its name: the refined mark is still four interlaced
circles.

---

## 1 · The Ten Invariants

Non-negotiable. Output violating one of these is not Ori.

1. **Light for function, dark for moments.** Anything people *read* sits on
   Horizon `#FAFAFA`. Solar Horizon atmospheres and Real Black are for key
   moments only — covers, heros, statement and closing slides — where visuals
   outweigh text. Print body pages are always light.
2. **One signal.** Seagrass `#BAFE81` is the only accent, at most once per
   page/slide/viewport. On light it is a **fill under Real Black ink** (marker,
   key metric, chip) — never text, never a rule. On dark it may glow or be ink.
3. **Atmosphere, not decoration.** The blues live in the Solar Horizon
   backgrounds and in data. Headlines are never blue; gradients other than the
   four horizons don't exist.
4. **One family, many widths.** SF Pro (fallback Archivo) carries everything.
   Personality comes from the **width axis**: wide cuts (118–132) for display,
   normal width (100) for reading. No serif, no italics, no second family
   (code alone gets a mono).
5. **Sentence case.** Headlines are sentence case. Uppercase belongs only to
   kickers, labels, and the folio.
6. **Numbers are figures.** Every number is tabular; the figures a page argues
   with are set in the wide display cut.
7. **Open layouts.** Structure comes from 1px hairlines and whitespace, flush
   left, ragged right. No boxes drawn around sections, no nesting deeper than
   one container.
8. **Slight radii.** Corners are softened, never sharp and never toy-round:
   4 · 8 · 12 · 24px. Full circles only for dots and avatars.
9. **Depth is earned.** Soft, cool shadows on photos and screen cards; flat
   everywhere else. Glow belongs to Seagrass alone.
10. **The folio closes every page.** Hairline, lockup, legal line, page
    number. The logo is black or white — never colored, never cropped.

---

## 2 · Color

### 2.1 Brand palette (from the guideline swatches — exact)

| Token | Hex | Guideline name · role |
|---|---|---|
| `--black` | `#1F2937` | **Real Black** — primary text; dark surface |
| `--dust` | `#535B65` | **Dust** — secondary text; panels on dark |
| `--cloud` | `#CCCED1` | **Cloud** — strong hairlines; light secondary panel |
| `--horizon` | `#FAFAFA` | **Horizon** — the light canvas |
| `--seagrass` | `#BAFE81` | **Seagrass** — the signal |
| `--dawn` | `#314188` | **Solar Horizon · Dawn** — hero color direction |
| `--day` | `#3E6FE7` | **Solar Horizon · Day** |
| `--dusk` | `#2A2759` | **Solar Horizon · Dusk** |
| `--twilight` | `#070B2F` | **Solar Horizon · Twilight** (from the asset) |

### 2.2 Derived (fixed steps; don't invent more)

| Token | Hex | Role |
|---|---|---|
| `--mist` | `#80868F` | Tertiary text — captions, annotations, page numbers (≥ 3.5:1, small text only) |
| `--rule` | `#E3E5E8` | Default hairline (table rows, dividers) |
| `--fog` | `#F1F2F4` | Panel fill (callouts, tags), chapter-opener ground |
| `--paper` | `#FFFFFF` | Cards, table surfaces, photo mats |
| `--day-deep` | `#2F5BCC` | Links and any blue text on light (5.8:1) |
| `--day-soft` / `--day-wash` | `#9DB8F5` / `#EAF0FD` | Chart series 3 / subtle blue fill |
| `--pos` / `--neg` / `--warn` | `#2F7A12` / `#C23B32` / `#9A6206` | Deltas, statuses, risk — nothing else |
| `--on-dark` / `--on-dark-2` | `#FAFAFA` / `#CCCED1` | Text on dark and horizon surfaces |

### 2.3 Light and dark (the guideline's "overview of background color")

| | Light background | Dark background |
|---|---|---|
| Surfaces | Horizon `#FAFAFA` (+ Cloud, Fog, Paper panels) | Real Black `#1F2937` (+ Dust panels) **or** a Solar Horizon |
| Use | Functional pages: more text than visuals | Key hero moments: more visuals than text |
| Artifacts | Every document body page, report, minutes, resume, evidence slides, landing content sections | Long-doc cover, slide cover / statement / close, landing hero and final CTA |
| Text | Real Black, Dust, Mist | Horizon, Cloud; **Day takes Real Black text** |
| Signal | Seagrass as a fill under black ink | Seagrass as glow, chip, or ink |

### 2.4 The Solar Horizon

Four atmospheres, each a soft-focus sky with a luminous band at the horizon
line. **Dawn is the hero color direction** — use it unless there's a reason
not to.

| Horizon | Character | Text | Use |
|---|---|---|---|
| **Dawn** | Indigo with a pale lilac glow | white | Default: covers, heros, statement slides |
| **Day** | Bright sky blue, white glow | **Real Black** (white fails contrast) | Optimistic launches, product moments |
| **Dusk** | Violet with a peach glow | white | Closing slides, reflective beats |
| **Twilight** | Near-black navy, blue glow | white | Dense dark slides, code/tech moments |

HTML uses the CSS recreations in `tokens/ori.css` (`.horizon.dawn|day|dusk|twilight`)
— resolution-free, printable, and self-contained. The original renders ship in
`assets/horizon/*.jpg` (2880×2048) for Office files and anywhere a real image
is needed. Never tint, recolor, crop the glow out, or place a horizon behind
body copy.

### 2.5 Ratios

A light page is ~90% neutral, ~9% line and panel, ≤1% Seagrass. A dark
moment is horizon + type + at most one Seagrass element. If Seagrass appears
twice, remove one.

### 2.6 Contrast floors

Body text ≥ 7:1 (Real Black on Horizon = 14:1). Secondary ≥ 4.5:1 (Dust =
6.6:1). Mist only at caption/label sizes. On Dawn/Dusk/Twilight, body is Cloud
and headings Horizon. On Day, everything is Real Black. Seagrass text is legal
only on Real Black, Dawn, Dusk, Twilight.

---

## 3 · Typography

### 3.1 Family

| Stack | Composition | Carries |
|---|---|---|
| `--font` | **SF Pro** → Archivo → Helvetica Neue → Arial | Everything |
| `--code` | SF Mono → ui-monospace → JetBrains Mono → Menlo | Code only |

SF Pro is the brand typeface (installer: Drive › Brand Guidelines ›
`_Typeface/SF-Pro.dmg`). It can't be web-served, so every template also loads
**Archivo** from Google Fonts — an open-licensed grotesque with a 62–125 width
axis that is the closest free match to SF Pro's wide cuts. Machines with SF
Pro installed render SF Pro; everyone else, and every headless PDF build,
renders Archivo. Width values above 125 clamp to 125 in Archivo — expected.

Width is set with `font-stretch` (maps to the `wdth` axis). Weight uses the
variable `wght` axis — the brand's odd weights (510, 590, 591, 650) are
intentional.

### 3.2 The brand type styles (1:1 from the guideline, at desktop size)

| Style | Size | Weight | Width | Ori role |
|---|---|---|---|---|
| H1 Headline | 128px | 590 | 132 | Display: covers, heros, statement titles |
| H2 Headline | 96px | 700 | 132 | Big section statement (landing, close) |
| H3 Headline Wide | 64px | 510 | 118 | Slide titles, cover subtitles, quotes |
| H3 Headline | 64px | 400 | 110 | Chapter openers, calm display |
| H4 Headline Wide | 36px | 650 | 118 | Section headlines (assertions) |
| H4 Headline | 36px | 650 | 100 | Sub-sections, card titles |
| Body 1 | 18px | 591 | 120 | Labels, kickers, buttons, UI — the "instrument" voice |
| Body 2 | 18px | 400 | 100 | Reading text |

### 3.3 Scale per medium

Ratios follow the brand styles; sizes are fixed per medium — don't invent
intermediates.

| Role (brand style) | Screen (landing) | Slides 1280×720 | Print A4 |
|---|---|---|---|
| Display (H1) | clamp 56–128px, lh .98, −.025em | 76px | 40pt (cover) |
| Statement (H2) | clamp 40–96px, lh 1.0 | 60px | — |
| Title wide (H3W) | clamp 30–64px | 44px (evidence title) | 26pt (doc H1, w132) |
| Section (H4W) | clamp 22–36px | 26px | 15pt |
| Sub-section (H4) | 22–36px | 20px | 11pt |
| Lede | 22px, Dust | 20px | 12pt, Dust |
| Body (Body 2) | 18px, lh 1.55 | 18px | 9.5pt, lh 1.5 |
| Small | 15px | 15px | 8.5pt |
| Label (Body 1, caps, +.06em) | 12px | 12px | 7pt |
| Kicker (700, caps) | 14px | 14px | 9pt |
| Metric value (H1 cut) | 44px | 56px | 26pt |
| Folio | 9px | 9px | 6pt |

Floors: body ≥ 16px screen / 9pt print; labels ≥ 11px / 6.5pt; folio legal
line may go to 6pt (it is a legal mark, not reading text).

### 3.4 Rhythm and rules

- Measure 60–70ch for body; ledes ≤ 46ch on screen, ≤ 62ch in print.
- Paragraph gap = 0.9 × line-height; no indents; never justified.
- Display tracking tightens with size (−.015 to −.03em); labels open up
  (+.04 to +.06em); body is 0.
- Emphasis: weight 650. Italics are banned. Underline is for links only.
- The Seagrass marker (`.hl`) may sit under **one** word, phrase (≤ 3 words),
  or number per page — the thing the page argues.
- Numbers are always `tabular-nums` (set on `body`).

### 3.5 No blurred type

The guideline floats progressive blur for large headlines. Ori doesn't use it:
in practice it reads as a rendering fault and costs the headline its
legibility. Type is always sharp. Blur survives only as a photo treatment
(`.photo.soft`, §8).

---

## 4 · Space, geometry, layout

### 4.1 Spacing (8px base; print ≈ ×0.75 in pt)

4 inline · 8 label→value · 12–16 paragraphs · 20 component interior · 24
between components · 32–48 between sections · 64–128 landing sections.

### 4.2 Radii

| Token | Value | Use |
|---|---|---|
| `--r-xs` | 4px | Seagrass marker, tags, inline code |
| `--r-s` | 8px | Print callouts, inputs, small cards |
| `--r-m` | 12px | Buttons, cards, screen callouts, code blocks |
| `--r-l` | 24px | Photos, hero panels, large cards |

### 4.3 Elevation

`--shadow-card` (screen cards), `--shadow-photo` (every photo, print
included), `--glow` (Seagrass only). Shadows are cool-tinted (Dawn, low alpha)
— never gray-black, never hard-edged.

### 4.4 Page geometry

| Artifact | Size | Margins (T·R·B·L) |
|---|---|---|
| One-pager | A4 portrait | 14·16·12·16 mm |
| Long doc | A4 portrait | 18·20·14·20 mm |
| Report | A4 portrait | 16·18·14·18 mm |
| Resume | A4 portrait | 12·14·10·14 mm |
| Minutes | A4 portrait | 16·18·14·18 mm |
| Slides | 1280×720 px | padding 56px 72px 40px |
| Landing | fluid | content max-width 1200px; sections 128px 64px (mobile 72px 20px) |

The folio sits inside the bottom margin on every print page.

### 4.5 Grid

12 columns, 24px gutters. Sanctioned splits: full · 7/5 · 4×3 (metrics) ·
6/6 (card pairs) · **annotation rail** (2/10: a narrow left column of quiet
labels beside content — the guideline's type-spec layout). Text goes in the
wider column. Three-column body text is banned.

### 4.6 Density contract

Every print page lands at **60–85% fill**. Below 55%: merge up or promote a
list to a table/figure. Above 90%: split. Dark moments are the exception —
they are allowed to be mostly air.

---

## 5 · Signature elements

Use #1, #2, #4 on every artifact; #3 for every section; #5–#6 where the
artifact calls for them.

### 5.1 Page head — kicker + quiet meta

```html
<div class="page-head">
  <span class="kicker">Insight report</span>
  <span class="meta"><span>Gen-Z beauty panel</span><span>2026-10-07</span><span>Confidential</span></span>
</div>
```
Top-left, bold uppercase kicker (the guideline's `OVERVIEW`) naming the
artifact or chapter. Metadata right-aligned in Mist. No rule beneath — the
layout is open.

### 5.2 Section head — hairline, index, assertion

```html
<header class="section-head">
  <span class="index"><b>01</b>Audience signal</span>
  <h2 class="h4w">Trust follows the face, not the logo</h2>
</header>
```
A 1px Cloud rule, a quiet uppercase index line (number in Real Black, topic in
Mist), then the assertion headline in the wide cut. Indexes run `01`, `02`…

### 5.3 The Seagrass signal

One **dominant** signal per page/slide/viewport — a marker, key metric,
chip, or Seagrass CTA. The 8px **signal dot** (insight-callout label,
takeaway label, timeline `.now`) is a wayfinding mark, not the signal: it
doesn't count toward the one, but keep it to one per section. Pick the form
that fits the surface:

| Form | Class | Where |
|---|---|---|
| Marker | `.hl` | Under the one word/number the page argues (light or dark) |
| Key metric | `.metric.key` | The hero metric in a metric row |
| Signal chip | `.signal` | Glowing chip on dark/horizon — a status, a label, a CTA |
| Signal dot | `.signal-dot` | Live/status indicator; insight-callout label |
| Primary CTA | `.btn.primary` on dark | Landing hero / final CTA |

### 5.4 Folio — on every page

```html
<footer class="folio">
  <svg class="lockup" viewBox="0 0 1086.6 165.7"><use href="#st-lockup"/></svg>
  <span class="legal">Confidential material. Socialtrait © 2026. All rights reserved.</span>
  <span class="pageno">ST-RPT-014 · 02 / 08</span>
</footer>
```
Exactly the guideline's page foot: Cloud hairline, lockup bottom-left
(14px screen / 9pt print), centered legal line in micro caps, doc-id and
zero-padded page number right. Public artifacts (landing, external decks
marked public) swap the legal line for `Socialtrait © 2026`.

**Exception — resumes are unbranded.** A resume is the candidate's document:
its folio is the same hairline + micro caps, but carries the candidate's name
left and `1 / 1` right — no lockup, no legal line.

### 5.5 Chapter opener

```html
<section class="chapter page"><span class="num">02</span><span class="title">Typography</span> … folio</section>
```
Fog page, giant numeral and one-word title stacked bottom-left — weight
400 at the display width (132), the calm cut of the guideline's divider pages. **Long docs** (one per chapter, ≥ 3 chapters) and
**decks of ≥ 12 slides** (one per act, max 4). Never in one-pagers, reports,
minutes, resumes. A chapter opener carries nothing else but the folio.

### 5.6 Horizon moments

Full-bleed `.horizon.<dawn|day|dusk|twilight>` surfaces. Layout for covers:
centered lockup (white; black on Day) above a centered H3W-cut title — the
guideline's cover. Heros may align left. Every horizon page still gets a
folio (white-on-dark variant). Max one horizon per print document (its cover);
landing pages never stack two horizon sections back-to-back.

---

## 6 · Components

### 6.1 Metric row
Spec-sheet grid: Cloud top rule, Rule bottom rule, hairline seams between
cells, no boxes. Label above (Body 1 caps, Mist); value in the H1 cut
(590/w132), tabular; unit at .45em in Dust. Exactly one `.key` cell gets the
Seagrass marker. 3–4 cells; labels ≤ 18 characters.

### 6.2 Tag
Body 1 caps 11px on Fog, 4px radius. `.signal-tag` (Seagrass) for one "new /
live / recommended" flag; `.outline` for neutral taxonomy. ≤ 4 per cluster.

### 6.3 Table
Header in Body 1 caps (Mist) over a Cloud rule; rows divided by Rule
hairlines; no vertical rules, no zebra. Numbers right-aligned tabular
(`.num`). Totals: 1px Real Black top rule, weight 650. One `tr.key` row may
carry a 3px Seagrass inset bar. ≤ 6 columns on A4 portrait.

### 6.4 Callout
Fog panel, 12px radius (8px print), bold caps label. Variants: `.insight`
(Seagrass dot in the label — one per report section), `.ask` (Real Black
panel, Cloud label — the decision or request; once per document; it does not
spend the page's Seagrass signal),
`.risk` / `.warn` (3px inset semantic bar).

### 6.5 Quote
Set in the H3W cut at reading-display size (26px screen / 14pt print),
≤ 34ch, no quote marks block, no rule. Cite in Body 1 caps Mist. Quotes from
Socialtrait simulations cite the persona: `— Maya · Simulated Gen-Z shopper`.

### 6.6 Persona card
Paper card, 12px radius, `--shadow-card` on screen (hairline border in print),
48px Fog avatar circle with initials, name 650, role in Mist, ≤ 3 tags, one
quote. Grid rows of 2–3.

### 6.7 Spec list (`.spec`)
The guideline's annotation column: quiet Mist labels left, values right,
Rule hairline under each row. Use for logistics, document metadata,
key–value facts.

### 6.8 Timeline
1px Cloud spine; open 9px dots with a Real Black ring; the current step
`.now` fills Seagrass with a glow. Label caps Mist above a 650 title.

### 6.9 Photos
See §8. `.photo` = 24px radius + `--shadow-photo`; `.photo.soft` adds the
progressive blur at the lower edge.

### 6.10 Buttons (screen)
12px radius, Body 1 at 15px. Primary on light = Real Black fill / Horizon
text; primary on dark/horizon = **Seagrass fill + glow** / Real Black text
(this counts as the viewport's signal). Ghost = inset Cloud hairline. One
primary per viewport. No icon-only buttons.

### 6.11 Code
Inline: Fog chip, 4px radius, SF Mono. Block: Real Black panel, 12px radius,
Horizon text.

### 6.12 Icons
1.5px line icons, round joins (slight radii), `currentColor`, 16/20/24px. No
filled icons, no emoji, no icon tiles.

---

## 7 · Charts

Inline SVG (no chart libraries in print artifacts).

- **Series on light:** `#3E6FE7` Day → `#314188` Dawn → `#9DB8F5` Day-soft →
  `#CCCED1` Cloud. Highlight one series in Day; step the rest down.
- **Series on dark/horizon:** highlight `#BAFE81` Seagrass; others Horizon at
  55% / 30% opacity.
- **Gridlines** horizontal only, 1px `#E3E5E8`; baseline 1px `#CCCED1`. No
  plot border, no fill.
- **Labels:** axis 11px Mist; values 12px Real Black, weight 591, tabular.
  Direct-label lines instead of legends (≤ 3 series).
- **Bars:** top corners 3px radius, gap ≥ 40% of bar width, ≤ 8 categories ×
  3 series. **Lines:** 2.5px, round joins, end-point dot 6px with a 2px
  Horizon ring. **Donut:** stroke ring, ≤ 5 segments, metric centered in the
  H1 cut.
- **Deltas** are the only place Pos/Neg appear in a chart.
- Every figure has a `.figcap`: bold `Fig 01` + one-sentence caption +
  `Source: …` right-aligned in Mist.

Chart choice: share of ≤ 5 parts → donut; compare categories → bar; trend →
line; 2×2 strategy → quadrant (hairline axes, Fog quadrant fills);
decomposition → waterfall; process → flow of 8px-radius hairline boxes.

---

## 8 · Photography

From the guideline's image treatment:

- **Do:** brighter tones, realism, natural light. Real photographs are the
  baseline for any AI image editing — edit for cohesion, don't generate from
  nothing.
- **Treatment:** large corner radii (24px), the soft cool drop shadow, and an
  optional progressive blur toward one edge (`.photo.soft`).
- **Don't:** dark, moody, or green-cast imagery; stock clichés; illustrations
  of abstract 3D blobs; images as filler for sparse pages.
- Photos appear on screen artifacts (landing, decks) and long-doc chapters
  where they are evidence. One-pagers, reports, minutes, and resumes stay
  photo-free.
- Every photo has a reason and, where it's evidence, a caption.

---

## 9 · Logo

The refined logo (2026): the mark rebuilt from four equal circles plus two
concentric inner circles on a shared grid, unified into one path with slight
corner radii; the wordmark given ownable detail. *This is the logo to use going
forward across all applications.* The previous blue logo is retired.

**Files** (`assets/logo/`): `lockup-*` (mark + wordmark — the primary logo),
`mark-*`, `wordmark-*`, each in `black` and `white`, as SVG and PNG
(`png/`). `symbols.html` holds the inline `<symbol>` block templates paste
once.

**Rules**
- Black (Real Black via `currentColor`) on light; white on dark and on Dawn,
  Dusk, Twilight; black on Day. Never colored, never Seagrass, never a
  gradient, outline, shadow, or rotation.
- **Lockup** is the default. **Mark alone** only where the lockup can't fit
  legibly (favicons, app tiles, ≤ 24px slots). **Wordmark alone** never.
- Placement per surface: folio lockup on every page (9pt print / 14px
  screen); cover lockup centered above the title (28–40px); landing nav lockup
  22px. Max two instances per printed page (cover + folio) — or per
  viewport on scrolling pages.
- Clear space: the mark's inner-aperture width on all sides. Minimum lockup
  height 9pt / 12px.
- Never watermark, crop, bleed, or tile the logo. Never retype "socialtrait"
  in a font to imitate it.

---

## 10 · Motion (screen)

- Durations 200ms (hover) / 600ms (entrances). Easing
  `cubic-bezier(.2,.7,.1,1)` — calm, forward.
- Entrances: fade + 16px rise, once. No
  loops, no parallax, no typewriter effects.
- `prefers-reduced-motion: reduce` collapses all motion.

---

## 11 · Print & build notes

- Templates carry `@page` rules; render via headless Chrome
  (`chrome --headless --print-to-pdf=out.pdf --virtual-time-budget=8000 file.html`
  — the budget lets the Archivo webfont load).
- Print colors: `-webkit-print-color-adjust: exact` is set so horizons, Fog
  panels, and Seagrass print.
- Grayscale check: Seagrass prints as a light tint — never encode meaning in
  Seagrass alone; pair it with position, weight, or a label.
- PDF metadata: title = document H1; author = requester or "Socialtrait".
- Every template keeps `<meta name="generator" content="Ori 2">`.
