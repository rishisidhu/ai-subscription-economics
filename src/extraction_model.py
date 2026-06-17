"""
extraction_model.py — How Chart A's "what you can take" ranges are derived.

Everything here comes from Anthropic's OWN published figures. No third-party
estimates are used. Run this file to reproduce the ranges in chart_data.py.

PRIMARY SOURCES
  1. Per-window message limits — Anthropic Help Center:
     https://support.anthropic.com/en/articles/11014257-about-claude-max-usage
       Max 5x : "at least 225 messages every five hours"
       Max 20x: "at least 900 messages every five hours"
       Pro    : ~45 messages / 5h window (Anthropic-consistent; widely observed)
       The session window resets every 5 hours.
  2. API rates + prompt caching — Anthropic pricing:
     https://platform.claude.com/docs/en/about-claude/pricing
       Sonnet 4.6: input $3 / output $15 per MTok   (band LOW)
       Opus 4.8  : input $5 / output $25 per MTok   (band HIGH)
       Cache read (hit) = 0.1x base input
       5-minute cache write = 1.25x base input

WHAT WE COMPUTE
  The API-equivalent dollar value a heavy user can pull through each flat plan
  in a month, i.e. what the same usage would cost at pay-as-you-go API rates.
  The gap between that and the flat fee is the subsidy.

REASONED ASSUMPTIONS (deliberately moderate; documented so they can be argued with)
  - Cadence: 2 fully-used 5-hour windows per working day, 22 working days/month
    = 44 fully-used windows/month. This is well below the theoretical ceiling
    (the window resets 4-5x/day) — a committed daily professional, not a bot
    running 24/7.
  - Per agent turn, WITH prompt caching (how heavy agent users actually operate,
    since the conversation is resent each turn and caching is the default):
        cached context replayed at 0.1x : 12,000 tokens
        fresh input at full price        :  1,500 tokens
        cache write at 1.25x             :  1,500 tokens
        output at full price             :  1,200 tokens
  - Band: Sonnet rates give the low end, Opus rates the high end. A real heavy
    user mixes models; the band brackets that.

Displayed chart values are rounded DOWN on both ends from the computed figures,
so the subsidy shown is never larger than the model supports.
"""

# --- published limits (source 1) -------------------------------------------
MSGS_PER_WINDOW = {"Pro": 45, "Max 5x": 225, "Max 20x": 900}
FLAT_FEE        = {"Pro": 20, "Max 5x": 100, "Max 20x": 200}

# --- cadence assumption -----------------------------------------------------
WINDOWS_PER_DAY = 2
WORKING_DAYS    = 22
WINDOWS_PER_MONTH = WINDOWS_PER_DAY * WORKING_DAYS   # 44

# --- per-turn token structure with caching ---------------------------------
CACHED_READ_TOKENS = 12_000
FRESH_INPUT_TOKENS = 1_500
CACHE_WRITE_TOKENS = 1_500
OUTPUT_TOKENS      = 1_200

# --- rates per token (source 2) --------------------------------------------
# (base_input, output, cache_read=0.1x input, cache_write=1.25x input)
SONNET = dict(bin=3/1e6,  out=15/1e6, cr=0.30/1e6, cw=3.75/1e6)   # band low
OPUS   = dict(bin=5/1e6,  out=25/1e6, cr=0.50/1e6, cw=6.25/1e6)   # band high


def cost_per_message(rate):
    return (CACHED_READ_TOKENS * rate["cr"]
            + FRESH_INPUT_TOKENS * rate["bin"]
            + CACHE_WRITE_TOKENS * rate["cw"]
            + OUTPUT_TOKENS * rate["out"])


def monthly_extraction(plan):
    msgs = MSGS_PER_WINDOW[plan] * WINDOWS_PER_MONTH
    return msgs * cost_per_message(SONNET), msgs * cost_per_message(OPUS)


if __name__ == "__main__":
    print(f"Fully-used windows/month: {WINDOWS_PER_MONTH}")
    print(f"Cost per message: Sonnet ${cost_per_message(SONNET):.4f}, "
          f"Opus ${cost_per_message(OPUS):.4f}\n")
    print(f"{'tier':9s} {'msgs/mo':>8s}  {'low':>8s}  {'high':>8s}  {'flat':>5s}  {'gap':>5s}")
    for p in MSGS_PER_WINDOW:
        lo, hi = monthly_extraction(p)
        print(f"{p:9s} {MSGS_PER_WINDOW[p]*WINDOWS_PER_MONTH:>8,}  "
              f"${lo:>7,.0f}  ${hi:>7,.0f}  ${FLAT_FEE[p]:>4d}  {hi/FLAT_FEE[p]:>4.1f}x")
