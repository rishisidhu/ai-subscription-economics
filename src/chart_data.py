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
#    finout.io (Claude Code pricing analysis, 2026).
#  - Real developer dashboard: $200 Max 20x -> $1,588 API-equiv in one month:
#    productcompass.pm (pricing dashboard).
#  - Pro $20 ~ 6-7M Sonnet input tokens/mo breakeven; Max $100 ~ 33M:
#    lowcode.agency (pricing analysis).
#  - Effective subsidies of 12-175x on flat-rate logins (Anthropic's own stated
#    rationale for the June 15 split): morphllm.com / Anthropic Help Center.
#
# We use conservative low-end heavy-user extraction so the chart understates
# rather than overstates the gap.
SUBSIDY = [
    # tier, flat_price, heavy_user_api_equiv_low, heavy_user_api_equiv_high
    ("Pro\n$20",      20,  120,  500),    # power user, ~6-7M+ tokens, well past breakeven
    ("Max 5x\n$100",  100, 400,  900),    # 33M+ token-equivalent heavy use
    ("Max 20x\n$200", 200, 600,  1588),   # finout $600-1500 + observed $1,588 dashboard
]

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
# CHART C — Cheaper tokens, bigger bills (SOURCED magnitudes, indexed)
# Source: 2026 inference-cost analyses; Goldman Sachs Research (60-70%/yr token
# price decline; 24x consumption growth by 2030); Gartner (90% cheaper inference
# by 2030, via Fortune). Token price ~280x down over 2yr; enterprise spend ~320% up.
DIVERGENCE = {
    "token_price_drop_factor": 280,   # over ~2 years
    "spend_growth_multiple": 4.2,     # +320% => 4.2x
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
