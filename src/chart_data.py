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
# ---------------------------------------------------------------------------
# CHART A — "What you pay vs what you can take"
# Extraction ranges DERIVED from Anthropic's own published figures (no third party).
# Full method in src/extraction_model.py; summary here.
#
# PRIMARY SOURCES
#   Per-window message limits — Anthropic Help Center (support.anthropic.com/.../11014257):
#     Pro ~45 msg / 5h window;  Max 5x "at least 225 / 5h";  Max 20x "at least 900 / 5h".
#     Session window resets every 5 hours.
#   Rates + caching — Anthropic pricing (platform.claude.com/docs/en/about-claude/pricing):
#     Sonnet 4.6 $3/$15 per MTok (band low);  Opus 4.8 $5/$25 (band high);
#     cache read 0.1x input;  5-min cache write 1.25x input.
#
# REASONED ASSUMPTIONS (deliberately moderate; stated so they can be challenged)
#   Cadence: 2 fully-used 5h windows/day x 22 working days = 44 windows/month.
#            (Below the theoretical 4-5 windows/day ceiling; a committed daily pro, not 24/7.)
#   Per agent turn, WITH prompt caching (how heavy agent users actually run):
#     12,000 cached-context tokens replayed at 0.1x  + 1,500 fresh input at full price
#     + 1,500 cache-write at 1.25x  + 1,200 output at full price.
#   Band = Sonnet rates (low) to Opus rates (high).
#
# COMPUTED -> DISPLAYED (display values rounded DOWN on both ends, never above the model,
# so the shown subsidy is conservative):
#   Pro      computed $63-105   -> displayed $60-100     (~5x the $20 fee)
#   Max 5x   computed $314-523  -> displayed $300-500    (~5x the $100 fee)
#   Max 20x  computed $1,256-2,094 -> displayed $1,250-2,000 (~6-10x the $200 fee)
SUBSIDY = [
    # tier, flat_price, heavy_user_api_equiv_low, heavy_user_api_equiv_high
    ("Pro\n$20",      20,  60,   100),
    ("Max 5x\n$100",  100, 300,  500),
    ("Max 20x\n$200", 200, 1250, 2000),
]
# Real-world validation point (not part of the model): a developer's published dashboard
# logged $1,588 of API-equivalent usage in one month on a $200 Max 20x plan
# (Pawel Huryn, productcompass.pm). It sits INSIDE our independently-derived Max 20x band,
# which is why we keep it as a corroborating marker rather than an anchor.
SUBSIDY_OBSERVED = ("Max 20x\n$200", 1588)

# ---------------------------------------------------------------------------
# CHART B — Crossover for a single subscriber (COMPUTED).
# Models one AGENT INTERACTION with prompt caching, priced at Sonnet 4.6.
#
# DEFINITION OF AN "INTERACTION": one agent turn. The agent resends the growing
# conversation as context, the model responds, the agent acts on it. This is the
# unit that loops dozens of times to complete a single task.
#
# PER-INTERACTION TOKEN MODEL (with prompt caching, same basis as Chart A):
#   cached_context  12,000 tokens  billed at cache-read 0.1x input
#   fresh_input      1,500 tokens  billed at full input
#   cache_write      1,500 tokens  billed at 1.25x input
#   output             700 tokens  billed at full output
# Rates: Sonnet 4.6 $3 input / $15 output per 1M tokens (Anthropic pricing page).
#   -> cost/interaction ~= $0.0242  -> break-even ~826 interactions/mo vs flat $20.
# (Without caching the same agent turn costs ~$0.051 and breaks even at ~390; caching
#  RAISES the break-even. We model the cheaper, caching case to stay conservative.)
CROSSOVER = {
    "cached_tokens": 12000,
    "fresh_in_tokens": 1500,
    "cache_write_tokens": 1500,
    "out_tokens": 700,
    "in_rate_per_token": 3 / 1e6,
    "out_rate_per_token": 15 / 1e6,
    "cache_read_rate_per_token": 0.30 / 1e6,   # 0.1x input
    "cache_write_rate_per_token": 3.75 / 1e6,  # 1.25x input
    "flat_revenue": 20.0,
}

# ---------------------------------------------------------------------------
# CHART C — Cheaper tokens, bigger bills (REAL ENDPOINTS, no invented curve)
# Drawn as two honest before/after points per series, NOT a smooth interpolation,
# because no public monthly time-series exists. All four numbers are real:
#
# Token price (GPT-3.5-equivalent inference, per 1M tokens):
#   $20.00 (Nov 2022) -> $0.07 (Oct 2024) = ~280x drop.
#   Source: Stanford HAI AI Index 2025, Ch.1 (Research & Development).
#   hai.stanford.edu/ai-index/2025-ai-index-report/research-and-development
# Total enterprise generative-AI spend (market-wide, per year):
#   $11.5B (2024) -> $37B (2025) = 3.2x rise.
#   Source: Menlo Ventures, "2025: The State of Generative AI in the Enterprise"
#   menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise
DIVERGENCE = {
    "price_start": 20.00, "price_start_label": "Nov 2022",
    "price_end":   0.07,  "price_end_label":   "Oct 2024",
    "spend_start": 11.5,  "spend_start_label": "2024",   # $B, enterprise GenAI spend
    "spend_end":   37.0,  "spend_end_label":   "2025",   # $B
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
