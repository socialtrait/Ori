# Ori Anti-patterns · v2

The banned list, then the pre-ship checklist. If output matches anything in
§1, it is not Ori — fix before delivering.

## 1 · Banned outright

### Retired v1 identity (never resurrect)
- The old blue interlaced logo, Signal Blue `#2F80ED` accents, navy `#213C60`
- Frost `#FAFBFE` canvas, night `#02122A` sections
- IBM Plex Mono labels/data, the meta rail, node squares, thread rules
- Square-cornered "instrument" containers

### Color
- Seagrass as text or lines on light backgrounds; Seagrass more than once per
  page/slide/viewport; Seagrass behind more than three words
- Blue (or any color) headlines; colored body text other than links
- Gradients other than the four Solar Horizons; tinted/recolored horizons;
  horizons behind body copy
- White text on the Day horizon
- Text-heavy dark pages; dark body pages in print artifacts
- Warm tones (cream, beige, parchment) as backgrounds
- Green/red anywhere except deltas, statuses, risk callouts
- Purple-to-pink "AI" gradients, glassmorphism panels, neon glows (the only
  glow is Seagrass's)

### Type
- Any family other than SF Pro / Archivo (mono only inside code)
- Serif, italics, Title Case or ALL-CAPS headlines (caps are for kickers,
  labels, folio)
- Wide display cuts for body text; normal-width cuts for display headlines
- Body below 16px screen / 9pt print
- Blurred type of any kind (progressive blur is for photo edges only)
- Letter-spaced body text; centered body text; justified text

### Layout & decoration
- Boxes drawn around whole sections "to group"; containers nested 2+ deep
- Sharp 0px corners on containers; radii outside 4/8/12/24; pill-shaped
  buttons or tags
- Hard or gray-black shadows; shadows on text; shadows on flat print panels
- Two horizon sections adjacent; more than one horizon page per print doc
- Chapter openers in one-pagers, reports, minutes, resumes; more than 4 in a deck
- Dark, moody, green-cast, or stock-cliché photos; photos as filler;
  placeholder image boxes; abstract 3D blobs; emoji as icons
- The logo colored, outlined, shadowed, cropped, rotated, tiled, or as a
  watermark; more than two logo instances per page; retyped wordmark
- Missing folio; resumes carrying the Socialtrait lockup

### Content
- Placeholder text of any kind reaching the user (`Lorem`, `TBD` without
  owner, `[Client]`)
- Fabricated metrics, testimonials, customer logos, star ratings
- Simulated-persona quotes presented as human research
- Padding content to fill a sparse page (merge pages instead)
- Restating a chart in its own insight callout
- Topic-label headings where an assertion is possible

## 2 · Pre-ship checklist

Run top to bottom; every line must pass.

**Identity**
- [ ] Page head (kicker + meta) on every content page/slide
- [ ] Folio on every page: hairline, lockup, legal line, `NN / TT` (resume:
      unbranded variant)
- [ ] Refined lockup only, black on light/Day, white on Dawn/Dusk/Twilight/Real Black
- [ ] Section heads sequential from `01`
- [ ] `<meta name="generator" content="Ori 2">` and Archivo link intact

**Color**
- [ ] Function pages on Horizon `#FAFAFA`; dark only for the sanctioned moments
- [ ] Exactly one Seagrass signal per page/slide/viewport, on the thing argued
- [ ] Horizons used per rules (Dawn default; Day with black text)
- [ ] Semantic colors only on deltas/statuses/risk

**Type**
- [ ] Wide headlines actually rendering (SF Pro or Archivo), not a system fallback
- [ ] Brand weights/widths per role; sentence case headlines
- [ ] Numbers tabular; key figures in the wide cut
- [ ] No italics, no serif, no off-scale sizes

**Structure**
- [ ] Every print page 60–85% full; no orphaned headings
- [ ] Tables ≤ 6 columns; numbers right-aligned
- [ ] Every figure: data + `Fig NN` caption + `Source:`
- [ ] Charts follow the v2 series ramp; one highlighted series; direct labels
- [ ] Density contract for the artifact type met (see SKILL.md Step 5)

**Content**
- [ ] Zero placeholders; optional blocks filled or deleted
- [ ] Every metric sourced or expressed as magnitude
- [ ] Headings are assertions; ghost test passes (slides)
- [ ] The ask/decision stated (one-pager ask callout, closing slide, final CTA)

**Delivery**
- [ ] Rendered and eyeballed (PDF for print artifacts, browser for landing,
      mobile width for landing)
- [ ] Office outputs generated via `scripts/ori_docx.py` / `ori_pptx.py`
      (never converted from HTML)
- [ ] PDF metadata set (title/author)
- [ ] Missing materials reported to the user in one line
