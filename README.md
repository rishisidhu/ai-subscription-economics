# The flat AI subscription was always a subsidy

Data, charts, and reproduction code for the article *"The flat AI subscription was always a subsidy. The bill is coming due."*

📄 **Read the article:** [link to be added on publish]

---

## What this is

A look at why flat-rate AI subscriptions ($20/month and similar) behave differently from every subscription business that came before them, why that gap is forcing a shift toward metered and tiered pricing, and where flat pricing is likely to survive. This repo holds the four charts from the article and the code and data behind them, so the numbers are auditable and the charts reproducible.

## Charts

| Chart | What it shows |
|-------|---------------|
| `charts/chartA_subsidy.png` | Flat price paid vs the API-equivalent value a heavy user can extract, per tier. The gap is the subsidy. |
| `charts/chartB_crossover.png` | Where a single flat subscriber crosses from profitable to unprofitable, computed from published API rates. |
| `charts/chartC_divergence.png` | Token prices falling while total spend rises (the Jevons-paradox dynamic). |
| `charts/chartD_ladder.png` | The shared pricing ladder across OpenAI, Anthropic, and Google. |

## Reproducing the charts

Requires Python 3.9+.

\`\`\`bash
pip install -r requirements.txt
python src/make_charts.py
\`\`\`

Charts are written to `charts/`. All input figures live in `src/chart_data.py`, annotated with their sources, so you can change an assumption and see the chart update.

## A note on the data

Chart B is computed directly from published API token rates and a stated, visible usage model — the assumptions are in the code and open to challenge. Charts A, C, and D plot figures sourced from provider pricing pages, analyst research, and reporting; every figure is attributed inline in `src/chart_data.py`. Pricing in this space moves quickly, so treat the specific numbers as a June 2026 snapshot and the direction as the claim.

## Licenses

- **Code** (`src/`): MIT — see [`LICENSE`](LICENSE).
- **Charts and data** (`charts/`, `src/chart_data.py` figures): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — reuse freely with attribution to Rishi Sidhu.
