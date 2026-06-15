# Chart data + provenance — AI subscription economics post
# Compiled June 15, 2026. Every number traces to a cited source.
# Used by make_charts.py. Kept separate so the data is auditable.

# ---------------------------------------------------------------------------
# API LIST RATES (USD per 1M tokens, input/output), Anthropic, June 2026
# Source: Anthropic pricing coverage (finout.io, cloudzero.com, morphllm.com),
#         all reporting the same published rates.
API_RATES = {
    "Haiku 4.5":  (1, 5),
    "Sonnet 4.6": (3, 15),
    "Opus 4.8":   (5, 25),
    "Fable 5":    (10, 50),   # launched June 9 2026; exactly 2x Opus 4.8
}

# ---------------------------------------------------------------------------
# CONSUMER / DEVELOPER FLAT TIERS (USD per month), June 2026
# Source: OpenAI, Anthropic, Google pricing pages + coverage (fritz.ai,
#         techjacksolutions.com, usagebox.com).
FLAT_TIERS = {
    "OpenAI":    {"Free/Go": 8,  "Plus": 20, "Pro": 100, "Pro max": 200},
    "Anthropic": {"Free": 0,     "Pro": 20,  "Max 5x": 100, "Max 20x": 200},
    "Google":    {"Free": 0,     "AI Pro": 20, "Ultra 5x": 100, "Ultra": 200},
}

# ---------------------------------------------------------------------------
# CHART A — "What you pay vs what a heavy user can extract" (THE CENTERPIECE)
# For each Anthropic tier: flat monthly price, and the API-equivalent value a
# heavy user can pull through it before throttling. The gap = the subsidy.
#
# Sources:
#  - Max 20x heavy user "consumes equivalent of $600-$1,500/mo for flat $200":
#    finout.io Claude Code Pricing 2026.
#  - Real developer dashboard: $200 Max 20x -> $1,588 API-equiv in one month:
#    productcompass.pm (Claude Code Pricing).
#  - Pro $20 ~ 6-7M Sonnet input tokens/mo breakeven; Max $100 ~ 33M:
#    lowcode.agency Claude Code Pricing.
#  - Effective subsidies of 12-175x on flat-rate logins (Anthropic's own stated
#    rationale for the June 15 split): morphllm.com / Anthropic Help Center.
#
# All three ranges are sourced from Verdent's usage-profile estimates, which map
# each plan to the API-equivalent monthly cost of a representative usage profile
# (verdent.ai/guides/claude-code-pricing-2026). Using one consistent source for
# all three bars rather than mixing. Top end corroborated by cloudzero.com
# ("over $1,200 for heavy users running Opus on large codebases") and a real
# developer dashboard observation of $1,588 (productcompass.pm), shown as a marker.
SUBSIDY = [
    # tier, flat_price, heavy_user_api_equiv_low, heavy_user_api_equiv_high
    ("Pro\n$20",      20,  50,   100),   # Verdent: light profile ~$50-100/mo API-equiv
    ("Max 5x\n$100",  100, 130,  260),   # Verdent: daily-developer profile ~$130-260/mo
    ("Max 20x\n$200", 200, 400,  1200),  # Verdent: power-user profile ~$400-1,200+/mo
]
# Real-world observed data point (not a range): one developer's dashboard showed a
# $200 Max 20x plan generating $1,588 of API-equivalent usage in a month. — productcompass.pm
SUBSIDY_OBSERVED = ("Max 20x\n$200", 1588)

# ---------------------------------------------------------------------------
# CHART B — Crossover for a single subscriber (COMPUTED, unchanged method)
# Computed from Sonnet 4.6 published rate ($3/$15 per 1M tokens) with a stated
# per-interaction token model. Break-even ~1,300 interactions/mo for flat $20.
CROSSOVER = {
    "in_tokens_per_task": 1500,
    "out_tokens_per_task": 700,
    "in_rate_per_token": 3 / 1e6,
    "out_rate_per_token": 15 / 1e6,
    "flat_revenue": 20.0,
}

# ---------------------------------------------------------------------------
# CHART C — Cheaper tokens, bigger bills (REAL ENDPOINTS, no invented curve)
# Drawn as two honest before/after points per series, NOT a smooth interpolation,
# because no public monthly time-series exists. The four numbers below are real:
#
# Token price (GPT-3.5-equivalent inference, per 1M tokens):
#   $20.00 (Nov 2022) -> $0.07 (Oct 2024) = ~280x drop.
#   Source: Stanford HAI AI Index 2025 (via searchenginejournal.com, medium.com/@horecny).
# Enterprise AI budget (average, per year):
#   $1.2M (2024) -> $7M (2026) = ~5.8x rise.
#   Source: FinOps Foundation 2026 State of FinOps (via oplexa.com).
# Headline framing "280x down / 320% up over two years": oplexa.com.
DIVERGENCE = {
    "price_start": 20.00, "price_start_label": "Nov 2022",
    "price_end":   0.07,  "price_end_label":   "Oct 2024",
    "spend_start": 1.2,   "spend_start_label": "2024",   # $M/yr
    "spend_end":   7.0,   "spend_end_label":   "2026",   # $M/yr
}

# ---------------------------------------------------------------------------
# REAL-WORLD ANCHOR (used in caption, not a chart): Uber
# Source: Bloomberg (via Natalie Lung), The Information, Fortune, ZeroHedge.
#  - Burned entire 2026 AI-tools budget in 4 months (by April).
#  - ~5,000 engineers; adoption 32% -> 84%; 84-95% monthly active.
#  - Per-engineer bills $150-$2,000/mo; power users $500-$2,000.
#  - Now capped at $1,500/mo per engineer per tool.
#  - CTO Praveen Neppalli Naga on record; ~$1,200 tokens in a 2-hour demo.
UBER = {
    "engineers": 5000,
    "adoption_start": 0.32,
    "adoption_end": 0.84,
    "per_engineer_low": 150,
    "per_engineer_high": 2000,
    "cap": 1500,
}
