# Logo assets

Official Socialtrait assets. Templates resolve these filenames directly —
do not rename.

| File | Content | Use on |
|---|---|---|
| `mark.svg` | Interlaced-knot mark, Signal Blue `#2F80ED` | Light surfaces: doc footers/meta areas, landing nav |
| `mark-white.svg` | Mark in white | Night surfaces |
| `mark-black.svg` | Mark in black | Grayscale/print-fax contexts only |
| `wordmark.svg` | Mark + "socialtrait" (`#2F80ED` + navy `#213C60`) | Covers, slide covers, landing navs |
| `wordmark-white.svg` | Wordmark in white | Night surfaces |
| `wordmark-black.svg` | Wordmark in black | Grayscale contexts only |

These files are the **brand color authority**: Ori's `--blue` (`#2F80ED`)
and `--navy` (`#213C60`) tokens are keyed to them. If the logo assets ever
change, update `tokens/ori.css` to match.

Usage rules (see `references/design.md` §9): never recolor, outline, shadow,
or rotate; clear space of one petal-width; minimum 20px / 15pt; never
typeset the company name to imitate the wordmark.
