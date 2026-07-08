# Ori → Office (docx / pptx)

Word and PowerPoint files are **native Ori outputs**, not conversions or
favors. The standard internal workflow is: generate `.docx` → upload to
Google Docs, generate `.pptx` → upload to Google Slides. Agents never ask
whether the user wants "Ori native or editable" — editable *is* native.

HTML stays the canonical rendering (highest fidelity, source of truth for
layout). Office files are generated **directly from the token system** via
`scripts/ori_docx.py` and `scripts/ori_pptx.py` — never by converting the
HTML.

## Deliverables per artifact

| Artifact | Deliver by default |
|---|---|
| One-pager, long doc, report | HTML + PDF + **DOCX** |
| Slides | HTML + **PPTX** |
| Resume | HTML + PDF (DOCX on request — recruiters edit) |
| Landing page | HTML only (it's a website) |

## Fonts

Office files name **Inter** (headings *and* body — Inter Display doesn't
ship to Office; accepted degradation) and **IBM Plex Mono** (labels, data).
Both are on Google Fonts, so Google Docs/Slides render them correctly after
upload (first time on a fresh account: *More fonts…* → add Inter and IBM
Plex Mono). Word desktop without the fonts installed falls back to a system
sans — acceptable; never substitute a different personality.

## Color & type translation

All hex values identical to `tokens/ori.css`. Sizes in pt (px × 0.75).

| Role | docx | pptx |
|---|---|---|
| Title / H1 | Inter bold 22pt ink | cover 40pt, statement 33pt |
| H2 (section) | Inter bold 15pt ink | evidence title 22pt |
| H3 | Inter bold 11.5pt ink | — |
| Body | Inter 10pt ink, 1.5 spacing, 6pt after | 14pt slate, 1.4 |
| Lede | Inter 11pt slate | 16pt mist-n (night) / slate |
| Eyebrow | Plex Mono 8pt blue, caps, +0.6pt tracking | 10pt |
| Meta rail | Plex Mono 8pt mist caps; brand word ink | 9pt |
| Caption / source | Plex Mono 8pt mist | 10pt |
| Metric value | Plex Mono bold 24pt (hero → blue) | 38pt |
| Metric label | Plex Mono 8pt mist caps | 11pt |
| Takeaway | — | label 8pt blue caps + 13pt ink |

## Component degradation contract

What survives, what degrades, what is banned. Degrade honestly — never
fake a fidelity Office can't hold.

| Element | docx | pptx |
|---|---|---|
| Meta rail | Paragraph: inline mark PNG (12pt tall) + mono text, right tab for classification, 0.5pt `line` bottom border | Mark PNG + text boxes + hairline shape |
| Thread rule | Heading paragraph gets 1pt `line` bottom border; **the blue lives in the eyebrow** (two-color borders don't exist in Word) | **Exact**: node square + 2px blue segment + hairline as shapes |
| Node square | `▪` glyph in Signal Blue (footer, timeline) | True 6px square shape |
| Metric row | Table: label row + value row, 0.5pt `line` borders, white fill | Text boxes on hairline-bordered rectangles |
| Callout / insight strip | 1×1 table, `wash` shading, 2¼pt blue left border, mono label line | Rectangle `wash` fill + blue left bar |
| Table | Hairline horizontal rules only; header row mono caps mist with `line-strong` bottom rule; numeric cols right-aligned Plex Mono | pptx table, same rules |
| Quote | Left border 1½pt `line-strong`, indented, mono cite | Text box + left bar shape |
| Night sections | **Banned in docx** (print rule applies) | Flat `night` fill — the radial glow degrades to flat, accepted |
| Weave/watermark | Banned (as everywhere) | Banned |
| Wordmark imprint | PNG on covers, ~42mm wide | White PNG on night cover, ~2.4in |
| Page footer | `▪ SOCIALTRAIT / ORI · DOC-ID` + `PAGE X / Y` field codes, mono 7.5pt | Rail carries pagination (`03 / 08`) |
| Charts | Insert as images rendered per §7 chart rules, with mono caption | Native pptx bar chart (series ramp colors) or image |

PNG logo assets live in `assets/logo/png/` (`mark`, `mark-white`,
`wordmark`, `wordmark-white`) — transparent, rendered from the official
SVGs. Regenerate them if the SVGs ever change.

## Using the generators

Dependencies: `pip install python-docx python-pptx` (the only Python
dependencies in the repo).

```python
from ori_docx import OriDoc
doc = OriDoc(doc_type="Statement of work", doc_id="ST-SOW-007",
             classification="Client confidential", artifact="long-doc")
doc.title("Audience simulation pilot — statement of work")
doc.lede("Scope, timeline, and commercial terms for the Q3 pilot.")
doc.metric_row([{"label": "Studies", "value": "8"}, ...])
doc.section(1, "Scope", "Six simulated studies across two campaigns")
doc.body("...")
doc.callout("The ask", "Countersign by <b>July 18</b> ...")
doc.save("sow.docx")
```

```python
from ori_pptx import OriDeck
deck = OriDeck(occasion="Q3 review", classification="Confidential")
deck.cover("Pilot results", "Simulation predicted the market.", ...)
s = deck.evidence(1, "Headline numbers", "Three pilots, one pattern",
                  context_stat=("Prediction accuracy", "87", "%"))
deck.metric_row(s, [...])
deck.takeaway(s, "Simulation is accurate enough to gate media spend.")
deck.close("Expand the pilot. Ten accounts, this quarter.", ...)
deck.save("deck.pptx")
```

Run `python3 scripts/ori_docx.py` / `python3 scripts/ori_pptx.py` with no
arguments to produce demo files that double as visual regression checks.

## Google upload checklist

- [ ] Fonts render as Inter / IBM Plex Mono (not substituted serif)
- [ ] Meta rail mark visible and small (≈12pt tall), not stretched
- [ ] Hero metric is blue; all other values ink
- [ ] Tables kept hairline rules (Docs sometimes adds default borders —
      if so, the file was edited outside the generator)
- [ ] Footer page fields resolved (`1 / 4`, not `PAGE`)
- [ ] pptx: night cover flat navy, white wordmark bottom-left
