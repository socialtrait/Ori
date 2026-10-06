# Solar Horizon assets

The four official atmospheres from *Brand Concept Guidelines V2*
(`Drive › Brand Guidelines › _Solar Horizon Assets`), 2880×2048 JPG.

| File | Horizon | Text on it | Role |
|---|---|---|---|
| `horizon-dawn.jpg` | Dawn — indigo, lilac glow | white | **Hero color direction** (default) |
| `horizon-day.jpg` | Day — bright sky blue, white glow | **Real Black** | Optimistic / product moments |
| `horizon-dusk.jpg` | Dusk — violet, peach glow | white | Closings, reflective beats |
| `horizon-twilight.jpg` | Twilight — near-black navy, blue glow | white | Dense dark moments |

HTML artifacts don't load these files — they use the CSS recreations in
`tokens/ori.css` (`.horizon.dawn|day|dusk|twilight`), which stay
self-contained and print cleanly. The JPGs are for the Office generators
(pptx backgrounds) and any medium that needs a real image.

Never tint, crop out the horizon glow, overlay patterns, or put body copy on
a horizon. See `references/design.md` §2.4.
