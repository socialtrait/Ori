# Ori Anti-patterns

The banned list, then the pre-ship checklist. If output matches anything in
§1, it is not Ori — fix before delivering.

## 1 · Banned outright

### Color
- Warm tones: cream, beige, parchment, off-yellow backgrounds
- Any second accent hue (teal, purple, orange "for variety")
- Purple-to-blue gradients, glassmorphism, neon glows — the "AI slop" look
- Colored headings (headings are ink; only eyebrows are blue)
- Green/red anywhere except deltas and risk callouts
- Dark body pages in print artifacts

### Type
- Serif faces, anywhere, for anything
- Italics (use weight 600 or blue)
- Title Case Or ALL-CAPS Headings (uppercase belongs to mono labels)
- Body text below 13px screen / 9.5pt print
- Proportional figures in metrics or tables (must be mono tabular)
- More than three font families in one artifact
- Letter-spaced body text; centered body text; justified text

### Layout & decoration
- Drop shadows in print; more than `--lift`/`--hover` on screen
- Corner radius > 6px; pill buttons; pill tags
- Nested boxes ≥ 3 borders deep; boxes drawn around whole sections "to group"
- Decorative stock imagery, hero illustrations of abstract 3D blobs, emoji
  as icons or bullets
- Full-width paragraphs beyond 70ch; three-column body text
- Section-divider slides; "Thank you" empty closing slides
- The logo as watermark — oversized, cropped, faded, tinted, or redrawn
- More than two logo instances on one page; logos in page footers
- Two adjacent night sections; night sections in print body

### Content
- Placeholder text of any kind reaching the user (`Lorem`, `TBD`, `[Client]`)
- Fabricated metrics, testimonials, customer logos, star ratings
- Simulated-persona quotes presented as human research
- Padding content to fill a sparse page (merge pages instead)
- Restating a chart in its own insight strip
- Topic-label headings where an assertion is possible

## 2 · Pre-ship checklist

Run top to bottom; every line must pass.

**Identity**
- [ ] Meta rail present on page 1 (and every slide/section top)
- [ ] Mark leads every meta rail (white on night); wordmark imprint on covers
      only; resume unbranded; no logo anywhere else
- [ ] Eyebrow + thread rule opens each section; indexes sequential from 01
- [ ] Node square appears ≥1× per page, ≤1× per component
- [ ] Node footer with doc-id and zero-padded pagination (`03 / 08`)
- [ ] `<meta name="generator" content="Ori">` intact

**Color**
- [ ] Background is `#FAFBFE`; cards `#FFFFFF`; nothing warm
- [ ] Exactly one blue hero metric per page; all other values ink
- [ ] Blue ≈ ≤5% of the visual field
- [ ] Semantic colors only on deltas/callouts

**Type**
- [ ] All numbers-as-data in mono tabular
- [ ] Headings sentence case, Inter Display weights 600/650
- [ ] No italics, no serif, no size inventions off the scale

**Structure**
- [ ] Every page 60–85% full; no orphaned headings at page bottom
- [ ] Tables ≤ 6 columns; numeric columns right-aligned mono
- [ ] Every figure: data + `FIG NN` caption + `SOURCE:` line
- [ ] Charts follow series ramp; one highlighted series; no legends when
      ≤3 series (direct labels)
- [ ] Density contract for the artifact type met (see SKILL.md Step 5)

**Content**
- [ ] Zero placeholders; all optional blocks either filled or deleted
- [ ] Every metric sourced or expressed as magnitude
- [ ] Headings are assertions; ghost test passes (slides)
- [ ] Ask/decision stated (one-pager callout, closing slide, final CTA)

**Delivery**
- [ ] Rendered and eyeballed (PDF for print artifacts, browser for landing)
- [ ] PDF metadata set (title/author/keywords/description)
- [ ] Missing materials reported to the user in one line
