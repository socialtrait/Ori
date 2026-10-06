# Ori → Office (docx / pptx) · v2

Word and PowerPoint files are **native Ori outputs**, not conversions or
favors. The standard internal workflow is: generate `.docx` → upload to
Google Docs, generate `.pptx` → upload to Google Slides. Agents never ask
whether the user wants "Ori native or editable" — editable *is* native.

HTML stays the canonical rendering (highest fidelity, source of truth for
layout). Office files are generated **directly from the token system** via
`scripts/ori_docx.py` and `scripts/ori_pptx.py` — never by converting the
HTML. Every hex value in both generators is copied from `tokens/ori.css`;
change the tokens first, then the generators.

## Deliverables per artifact

| Artifact | Deliver by default | Office surface |
|---|---|---|
| One-pager, long doc, report | HTML + PDF + **DOCX** | light only |
| Meeting minutes | **DOCX** (primary — lives in Google Docs) + HTML + PDF | light only |
| Slides | HTML + **PPTX** | Horizon evidence slides; horizon / Real Black moments |
| Resume | HTML + PDF (DOCX on request — recruiters edit) | light, **unbranded** folio |
| Landing page | HTML only (it's a website) | — |

## Font: Archivo, everywhere

Both generators name **Archivo** for every run (headings, body, labels,
numbers) and **JetBrains Mono** for code only.

Why Archivo:
- It is Ori's declared fallback for SF Pro (`--font` in `tokens/ori.css`),
  so the Office files match what every headless PDF build already renders.
- It is open-licensed (OFL) and ships in **Google Docs / Slides** (*More
  fonts…* → Archivo), so the upload path renders it with no install.
- SF Pro can't be embedded or redistributed, and Google Workspace doesn't
  offer it.

What Office can't hold: the **width axis**. Docs, Slides, Word, and
PowerPoint all use Archivo at its normal width — the wide display cuts
(118–132) don't exist there. Headings take their character from **weight
(bold) and size** instead; body is regular. Brand weights 510/590/591/650
collapse to Office's regular/bold pair: 650 and 700 → bold, 590/591 → bold
for display and labels-as-emphasis, 400/510 → regular. Accepted degradation.

Both generators declare Archivo with a sans PANOSE / pitch family, so Word
or PowerPoint on a machine without the font substitutes a grotesque (Arial /
Helvetica), never a serif. Install Archivo locally (Google Fonts) to see the
files as designed in desktop Office.

## Color & type translation

All hex values identical to `tokens/ori.css`. docx sizes follow the **Print
A4** column of design.md §3.3; pptx sizes follow the **Slides 1280×720**
column (pt = px × 0.75).

| Role (brand style) | Color | docx | pptx |
|---|---|---|---|
| Cover display (H1) | Horizon on horizon | — (docx has no dark cover) | 57pt bold, centred, −1.2pt |
| Statement (H2) | Horizon / Real Black on Day | — | 45pt bold |
| Title (H3W) | Real Black | 26pt bold, exact 1.08 | evidence title 33pt bold |
| Section (H4W) | Real Black | 15pt bold, exact 1.2 | — (slides use the title) |
| Sub-section (H4) | Real Black | 11pt bold | 15pt |
| Lede | Dust (Cloud on dark) | 12pt, 1.45 | 15pt |
| Body (Body 2) | Real Black | 9.5pt, at-least 1.5 | 13.5pt, 1.3 |
| Small / notes | Dust | 8.5pt | 11.25pt |
| Label (Body 1 caps) | Mist | 7pt caps, +0.42pt tracking | 9pt caps, +0.6pt |
| Kicker | Real Black (Horizon on dark) | 9pt bold caps | 10.5pt bold caps |
| Metric value | Real Black | 26pt bold, unit at .45 in Dust | 42pt bold, unit .45 Dust |
| Quote (H3W at reading size) | Real Black | 14pt regular, ≤ 34ch | 24pt regular |
| Folio | Real Black legal, Mist page no. | 6pt caps | 6.75pt caps |
| Links / blue text on light | Day-deep `#2F5BCC` | — | — |
| Chart series on light | Day `#3E6FE7` → Dawn `#314188` → Day-soft `#9DB8F5` → Cloud `#CCCED1` | image per §7 | native chart |
| Semantic | Pos `#2F7A12` · Neg `#C23B32` · Warn `#9A6206` | statuses, risk | deltas |

Neutrals: Real Black `#1F2937`, Dust `#535B65`, Mist `#80868F`, Cloud
`#CCCED1` (strong hairline), Rule `#E3E5E8` (default hairline), Fog
`#F1F2F4` (panels), Horizon `#FAFAFA` (canvas). Signal: Seagrass `#BAFE81`.
Headlines are never blue; Seagrass is never text on light.

## Component degradation contract

What survives, what degrades, what is banned. Degrade honestly — never
fake a fidelity Office can't hold.

| Element | docx | pptx |
|---|---|---|
| Canvas | Page colour Horizon `#FAFAFA` (screen + Google Docs; Word prints white unless background printing is on) | Horizon slide background |
| Page head (§5.1) | Header paragraph: kicker 9pt bold caps + right tab → meta in Mist caps. Repeats every page; no rule beneath | Kicker top-left (index in Mist + topic bold), meta (occasion) right in Mist |
| Section head (§5.2) | Paragraph with Cloud top border · index line (`01` bold black + topic Mist caps) · 15pt bold headline; keep-with-next | Kicker carries the index; the slide title is the assertion |
| Seagrass marker `.hl` | `<hl>…</hl>` markup → run shading `#BAFE81` + Real Black bold (square corners — Word can't round run shading) | — (use the key metric or a chip) |
| Key metric | Run shading Seagrass behind the value only (marker, not a filled cell) | Rounded Seagrass rectangle (4px radius) behind the value, width estimated from glyph count |
| Metric row (§6.1) | 3-row table, explicit per-cell borders: Cloud top, Rule bottom, Rule seams; no outer box | Line shapes: Cloud top, Rule bottom, Rule seams |
| Callout (§6.4) | 1×1 table, Fog shading, 11/15pt padding, bold caps label; `insight` adds a Seagrass `●`; `risk`/`warn` add a 3pt semantic left bar + coloured label. **Corners square** (Word tables can't round) | — (use takeaway / chip) |
| The ask | `ask()` = callout on Real Black, Seagrass label, Horizon text — once per document | `close(cta=…)` chip |
| Takeaway | — | Cloud hairline + 9px dot + bold caps label + one sentence, pinned above the folio. Dot is Seagrass **unless the slide already spent its signal** (then Real Black) |
| Signal chip | — | Rounded rect (12px radius), Seagrass fill, Real Black bold ink, Seagrass glow effect (Google Slides drops the glow — accepted) |
| Table (§6.3) | Caps Mist header over Cloud; Rule row dividers; numbers right; `total=True` → Real Black top rule + bold; `key_row` → 3pt Seagrass left bar + bold | Native table, "No Style, No Grid", same rules via cell lines |
| Quote (§6.5) | 14pt regular, right indent to ~34ch, no marks, no rule, cite caps Mist | Text box 24pt + caps Mist cite |
| Spec list / logistics (§6.7) | Table: caps Mist labels, values 8.5pt, Rule under each row, Cloud on top | — |
| Minutes set | `agenda` (indexed hairline rows, owner/timebox right), `decisions` (D-ids), `actions` (A-ids; status as Fog-shaded caps tag in Dust / Pos / Neg — never Seagrass), `smallprint` | — |
| Chapter opener (§5.5) | Own section: page head suppressed, Fog-shaded 1×1 table filling the text block (Word can't colour one page), 72pt regular numeral + title bottom-left, folio only | Fog slide, 112pt regular numeral + title bottom-left, folio only |
| Horizon moments (§5.6) | **Banned** (print rule: docx is light only) | Real JPG from `assets/horizon/` full-bleed, cropped from the top so the luminous band stays. Cover = Dawn, statement = Real Black or Twilight, close = Dusk. Day takes Real Black text + black lockup |
| Folio (§5.4) | Footer: Cloud top border · lockup PNG 9pt tall left · legal line 6pt caps centred · `DOC-ID · PAGE / NUMPAGES` (fields, zero-padded `\# "00"`) right in Mist | Line shape + lockup PNG 14px + centred legal line + `DOC-ID · 03 / 09` right. White variant (18% hairline, white lockup) on dark/horizon |
| Resume folio | Unbranded: candidate name left, `PAGE / NUMPAGES` right; no lockup, no legal line, no page head | — |
| Public artifacts | `public=True` → legal line becomes `Socialtrait © 2026` | same |
| Charts (§7) | `figure()` inserts a PNG rendered per §7 + figcap (bold `Fig 01`, caption, `Source:` right in Mist) | Native, editable: `bar_chart` (single series + `highlight=i` → Day bar, rest Cloud; multi-series → Day/Dawn/Day-soft/Cloud), `line_chart` (Day highlight, end dot with Horizon ring, direct labels instead of a legend), `donut_chart` (ring, Horizon separators, centred metric) + `legend_list`, `figcap`. Gridlines Rule, baseline Cloud, no value spine, transparent chart area. **Bar top radii degrade to square** |
| Radii | Not available in Word tables/shading — square, accepted | Rounded rectangles with small `adj` (4 / 12px) |
| Shadows, blur | Banned (print) | Banned (screen-only effects) |
| Italics | Never — emphasis is `<b>` (bold) | Same |

PNG logo assets live in `assets/logo/png/` — `lockup-black.png` on light,
`lockup-white.png` on dark and Dawn/Dusk/Twilight (480px tall, transparent,
rendered from the SVGs). The mark alone and the wordmark alone are never
used in Office files. Regenerate the PNGs if the SVGs change.

## Using the generators

Dependencies: `pip install python-docx python-pptx` (Pillow, a
python-pptx dependency, renders the docx demo chart).

```python
from ori_docx import OriDoc
doc = OriDoc(doc_type="Statement of work", doc_id="ST-SOW-007",
             date="2026-10-07", classification="Client confidential",
             meta=("Arlo Foods",), artifact="long-doc")   # one-pager|report|minutes|resume
doc.title("Audience simulation pilot — statement of work")
doc.lede("Scope, timeline, and commercial terms for the Q4 pilot.")
doc.metric_row([{"label": "Studies", "value": "8"},
                {"label": "Duration", "value": "10", "unit": "wks", "key": True}, ...])
doc.callout("Insight", "Panels answer <b>after</b> the decision.")   # kind=note|risk|warn
doc.section(1, "Scope", "Eight simulated studies across two campaigns")
doc.body("Success is interval coverage ≥ <hl>80%</hl> on holdout cells.")
doc.table(["Phase", "Weeks", "Fee"], rows, data_cols=(1, 2), total=True, key_row=1)
doc.figure("chart.png", "Variants tested per campaign.", source="pilots, 2026")
doc.quote("The simulation caught it in four hours.", "Dana · VP Growth")
doc.chapter(2, "Minutes")                 # long docs with ≥ 3 chapters only
doc.logistics(left_pairs, right_pairs); doc.agenda([("Scope", "Suraj · 15 min")])
doc.decisions([...]); doc.actions([{"action": ..., "owner": ..., "due": ..., "status": "open"}])
doc.ask("Countersign by <b>October 10</b>.")   # the one ask per document
doc.smallprint("<b>Next meeting:</b> 2026-10-21.")
doc.save("sow.docx")
```

```python
from ori_pptx import OriDeck
deck = OriDeck(occasion="Q4 pilot review", date="2026-10-07",
               classification="Confidential", doc_id="ST-DECK-012")
deck.cover("Pilot results", "Simulation predicted the market.", lede, presenter)  # bg="dawn"
s = deck.evidence(1, "Headline numbers", "Three pilots, one pattern",
                  context_stat=("Prediction accuracy", "87", "%"))  # or context_kicker=
deck.metric_row(s, [{"label": ..., "value": "87", "unit": "%", "key": True}, ...])
deck.takeaway(s, "Simulation is accurate enough to gate media spend.")
s = deck.evidence(2, "Speed", "Answers land inside the campaign cycle")
deck.bar_chart(s, cats, [("Variants", [2, 4, 3, 24])], highlight=3, w=px(640))
deck.figcap(s, "Creative variants tested per campaign.", "pilots, 2026")
deck.bullets(s, [...], x=MX + px(700), w=px(436))
deck.chapter(2, "Evidence")                    # decks of ≥ 12 slides, max 4
deck.table(s, headers, rows, data_cols=(1, 2), total=True, key_row=2)
deck.quote(s, "We stopped arguing about creative.", "Dana · VP Growth")
deck.line_chart(s, cats, series, value_range=(60, 95))
deck.donut_chart(s, cats, values, center_value="12", center_label="Cells")
deck.statement(5, "The point", "Simulation is an earlier panel.")   # bg="black"|"twilight"|…
deck.close("Decision requested", "Expand the pilot.", lede,
           contact="suraj@socialtrait.ai", cta="Approve the expansion")  # bg="dusk"
deck.save("deck.pptx")
```

Positions in `ori_pptx` are template px on the 1280×720 canvas — use
`px()`; `MX`/`CW` are the side margin and content width, `BODY_Y` the top
of the evidence body, `TAKE_Y` the takeaway line (keep content above it).

**API changes from v1.** Same class names and method vocabulary; v1
callers keep working. Additions: `meta`, `public`, `candidate` (docx) and
`doc_id`, `public` (pptx) constructor args; metric `unit` and `key` (legacy
`hero` still accepted); `ask()`, `figure()`, `chapter()`, `<hl>` markup,
table `total` / `key_row` / `widths`, agenda items as `(text, who)` tuples
(docx); `chapter()`, `signal()`, `quote()`, `table()`, `line_chart()`,
`donut_chart()`, `legend_list()`, `figcap()`, `bg=` on cover / statement /
close, `cta=` on close, bar-chart `highlight` / `horizontal` (pptx).
`statement()` is now a dark moment (Real Black by default), not a light
slide.

Run `python3 scripts/ori_docx.py [out.docx]` / `python3 scripts/ori_pptx.py
[out.pptx]` to produce demo files that exercise every component and double
as visual regression checks. With no argument they write to the system
temp dir — never into the repo.

## Google upload checklist

- [ ] Fonts render as **Archivo** (not a substituted serif or Arial). First
      time on an account: *Font → More fonts…* → add Archivo.
- [ ] Page head: kicker left, meta right in grey; no rule beneath.
- [ ] Folio on every page/slide: hairline, black lockup (white on dark),
      centred legal line, page number right. Docs: page fields resolved
      (`03 / 08`, not `PAGE`).
- [ ] Exactly **one Seagrass** element per page/slide (marker, key metric,
      insight dot, takeaway dot, or chip) — never Seagrass text on light.
- [ ] Tables kept hairline rules only (Docs sometimes adds default borders —
      if so, the file was edited outside the generator).
- [ ] Docs page colour is Horizon `#FAFAFA` (*File → Page setup*); callouts
      Fog, the ask Real Black.
- [ ] Slides: cover on the Dawn horizon, close on Dusk with the Seagrass
      chip; evidence slides on Horizon. Day horizon slides use black text.
- [ ] Slides charts: Google Slides imports native charts as **static
      images** — edit charts in PowerPoint (or rebuild as linked Sheets
      charts) before upload if they must stay live.
- [ ] Glow on the signal chip is dropped by Google Slides — expected.
