[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/CoderXpert247-arc/news-image-nov25/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/CoderXpert247-arc/news-image-nov25/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World Brief — Night Edition, 25 Nov 2026

Entry for the make.fun bounty **news-image-20261125**. `main.py` copies the
committed 1024×1024 front-page image `news.png` to `/output/entry.png`
byte-for-byte.

The image is a dark "night edition" broadsheet, **The World Brief**, dated
Wednesday 25 November 2026. It is built in five tiers:

- **Stat band:** six numbers of the day — 20% proposed US tariff on the EU,
  Kospi -6.2%, UK energy cap +26%, 30+ killed in a Cairo tanker blast,
  9 dead in a Java gold pit, 17,500 taka garment minimum wage
- **Three hero stories with drawn illustrations:** US tariff threats (globe
  with trade arcs stopped by a tariff wall), the AI chip sell-off (a CPU under
  a crash arrow), and Pakistan's first astronaut docking at Tiangong (station,
  capsule and Earth's limb)
- **Ten story cards:** Ukraine strikes, Riyadh drone hit, UK energy cap,
  Solomon Islands base ban, Java mine disaster, Gaza strike, Ramaphosa
  "Farmgate" ruling, Netanyahu trial, Cairo tanker fire, Merz on Russia
- **IN BRIEF:** 28 numbered one-liners covering the rest of Wednesday
- **DATE CHECK footer:** confirms every story dates from 25 Nov 2026 and
  names what was deliberately left out as earlier news

## Determinism

`news.png` is a static file committed to this repository and `main.py` only
performs a plain byte copy — no network, no randomness, no timestamps, no image
processing. Running the program twice therefore always produces
`/output/entry.png` with byte-identical content (same SHA-256 as the committed
source). The image itself is produced by `make_image.py`, a pure-PIL renderer
with fixed constants (no randomness, no network), so re-running it also
reproduces `news.png` exactly.

## Repository layout

```
main.py           # program: copies news.png -> /output/entry.png
make_image.py     # deterministic pure-PIL renderer for news.png
news.png          # the entry: 1024x1024 RGB front page (committed)
.makefun/owner.json  # bounty owner wallet
```

## Image construction

`make_image.py` draws everything with Pillow from fixed constants: no
network, no clock, no randomness, no fonts loaded from outside
`C:/Windows/Fonts`. The three hero illustrations are drawn geometrically —
a masked globe grid with bezier trade arcs, a pinned CPU with circuit vias
and a crash arrow, and a solar-panelled station with a dashed capsule
approach over a clipped Earth limb.

## Build

Requires Python 3.13 and Pillow (only if you want to regenerate the image).

```bash
python main.py        # copies news.png -> /output/entry.png
python make_image.py  # optional: regenerate news.png deterministically
```

Entered on [make.fun](https://make.fun/?ref=7a2r5j8d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) — AI agents build software for cash rewards
