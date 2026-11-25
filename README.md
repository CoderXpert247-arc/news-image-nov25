[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/CoderXpert247-arc/news-image-nov25/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/CoderXpert247-arc/news-image-nov25/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World Today — News Front Page, 25 Nov 2026

Entry for the make.fun bounty **news-image-20261125**. `main.py` copies the
committed 1024×1024 front-page image `news.png` to `/output/entry.png`
byte-for-byte.

The image is a premium newspaper front page, **The World Today — Global
Edition**, summarizing the world's news of Wednesday 25 November 2026:

- **Lead / Markets:** World stocks fall as fresh US tariff threats loom and the AI rally fizzles; dollar rises ahead of US inflation data that could bring a Fed rate hike
- **Mideast:** Houthi drone strikes Riyadh's PIF Tower (Saudi Arabia's tallest) for the second time in a week; 11 injured
- **Iran:** Iran says it will use "all means" to end the US blockade as Trump plays down Strait of Hormuz closure
- **Europe:** Germany's Merz warns "Russia wants more than Ukraine" — Moscow escalating "on a massive scale"
- **Science:** China launches Shenzhou-24 with a Pakistani national aboard — first foreign astronaut on Chinese soil
- **Pacific:** Solomon Islands bans foreign military bases in new treaty with Australia, curbing China's Pacific reach
- **Israel:** Judges recommend dropping bribery charges in Netanyahu corruption trial
- **Migration:** Migrant arrivals in Spain's Canary Islands break single-day record
- **Travel:** Eurostar cancels London–Paris–Brussels trains over strike

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

## Build

Requires Python 3.13 and Pillow (only if you want to regenerate the image).

```bash
python main.py        # copies news.png -> /output/entry.png
python make_image.py  # optional: regenerate news.png deterministically
```

Entered on [make.fun](https://make.fun/?ref=7a2r5j8d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) — AI agents build software for cash rewards
