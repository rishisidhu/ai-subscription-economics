# The Great AI Pricing Unwind Has Started

Data, charts, and reproduction code for the article *"The Great AI Pricing Unwind Has Started: the flat AI subscription was always a subsidy, and the bill is coming due."*

📄 **Read the article:** https://medium.com/p/875294b9210f

---

## What this is

A look at why flat-rate AI subscriptions ($20/month and similar) behave differently from every subscription business that came before them, why that gap is forcing a shift toward metered and tiered pricing, and where flat pricing is likely to survive. This repo holds the four charts from the article and the code and data behind them, so the numbers are auditable and the charts reproducible.

## Charts

| Chart | What it shows |
|-------|---------------|
| `charts/chartA_subsidy.png` | Flat price paid vs the API-equivalent value a heavy user can extract, per tier, derived from Anthropic's published session limits and rates. The gap is the subsidy. |
| `charts/chartB_crossover.png` | Where a single flat subscriber crosses from profitable to unprofitable, computed from one agent interaction at published Sonnet rates with prompt caching. |
| `charts/chartC_divergence.png` | Token prices collapsing while total enterprise spend rises (the Jevons-paradox dynamic). |
| `charts/chartD_ladder.png` | The shared pricing ladder across OpenAI, Anthropic, and Google. |

## Reproducing the charts

Requires Python 3.9+ and [pipenv](https://pipenv.pypa.io/).

```bash
pipenv install
pipenv run python src/make_charts.py
```

Charts are written to `charts/`. All input figures live in `src/chart_data.py`, annotated with their sources, so you can change an assumption and see the chart update. The Chart A extraction model is in `src/extraction_model.py` and can be run on its own:

```bash
pipenv run python src/extraction_model.py
```

## A note on the data

Charts A and B are *computed*, not borrowed. Chart A derives each tier's extractable value from Anthropic's published per-window message limits and API rates (with prompt caching); the full method is in `src/extraction_model.py`. Chart B is computed from published Sonnet rates and a stated, visible usage model. Both sets of assumptions are in the code and open to challenge. Charts C and D plot figures sourced from analyst research (Stanford HAI, Menlo Ventures) and provider pricing pages; every figure is attributed inline in `src/chart_data.py`. Pricing in this space moves quickly, so treat the specific numbers as a June 2026 snapshot and the direction as the claim.

## Licenses

- **Code** (`src/`): MIT — see [`LICENSE`](LICENSE).
- **Charts and data** (`charts/`, `src/chart_data.py` figures): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — reuse freely with attribution to Rishi Sidhu.
