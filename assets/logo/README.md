# Logo assets · refined 2026

The refined Socialtrait logo from *Brand Concept Guidelines V2* — "the logo to
use going forward across all applications." The previous blue interlaced logo
is retired; don't reintroduce it.

| File | Content | Use |
|---|---|---|
| `lockup-black.svg` / `lockup-white.svg` | Mark + wordmark — **the primary logo** | Folios, covers, landing nav |
| `mark-black.svg` / `mark-white.svg` | Mark only | Only where the lockup can't fit (favicons, ≤24px slots) |
| `wordmark-black.svg` / `wordmark-white.svg` | Wordmark only | Kept for completeness — Ori never uses it alone |
| `png/*.png` | Transparent PNG, 480px tall | Office generators (`scripts/ori_*.py`) |
| `symbols.html` | `<symbol id="st-lockup">` / `<symbol id="st-mark">`, `fill="currentColor"` | Paste once into HTML templates; reference with `<use href="#st-lockup"/>` |

**Color:** black on light surfaces and the Day horizon; white on Real Black and
the Dawn, Dusk, Twilight horizons. Never colored, never Seagrass, never a
gradient. In HTML the symbols follow CSS `color`, so set `color: var(--black)`
or `var(--on-dark)`.

**Provenance:** the brand team delivered the refined logo as PNG only
(`Drive › Brand Guidelines › _Logo Refined`). These SVGs are vector traces of
the logo as rendered in the guideline PDF (page 6), checked by overlay against
the source. If the brand team publishes master vectors, replace these files
with them — keep the filenames — and regenerate `png/` and `symbols.html`.

Rules (see `references/design.md` §9): clear space = the mark's inner aperture
width; minimum lockup height 9pt / 12px; never crop, rotate, outline, shadow,
watermark, or retype the wordmark.
