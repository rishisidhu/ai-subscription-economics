"""
Charts for the Medium post on AI subscription economics.
All figures and their sources live in chart_data.py (auditable).
Style: clean editorial, consistent palette.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import chart_data as D

INK, MUTED, GRID = "#1a1a1a", "#6b6b6b", "#e6e6e6"
ACCENT, COOL, FILL = "#c0392b", "#2c3e50", "#f4d7d2"
GOLD = "#c79a1e"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.8,
    "axes.titlesize": 14, "axes.titleweight": "bold", "figure.dpi": 150,
})

def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

def money(v, _):
    return f"${int(v):,}"

# ===========================================================================
# CHART A (CENTERPIECE) — flat price vs API-equivalent value a heavy user extracts
# ===========================================================================
def chart_subsidy():
    fig, ax = plt.subplots(figsize=(9, 5.4))
    style(ax)

    tiers = [t[0] for t in D.SUBSIDY]
    flat  = [t[1] for t in D.SUBSIDY]
    low   = [t[2] for t in D.SUBSIDY]
    high  = [t[3] for t in D.SUBSIDY]

    x = np.arange(len(tiers))
    w = 0.38

    # flat price paid
    ax.bar(x - w/2, flat, w, color=COOL, zorder=5, label="Flat price paid")

    # API-equivalent value extracted (range bar: low to high)
    heights = [h - l for l, h in zip(low, high)]
    ax.bar(x + w/2, high, w, color=FILL, zorder=4,
           label="API-equivalent value a heavy user can extract")
    ax.bar(x + w/2, low, w, color=ACCENT, zorder=5)

    # annotate the extract bars with the range
    for xi, l, h in zip(x, low, high):
        ax.annotate(f"${l:,}–\n${h:,}", (xi + w/2, h), xytext=(0, 6),
                    textcoords="offset points", ha="center", va="bottom",
                    color=ACCENT, fontsize=9.5, fontweight="bold")
    for xi, f in zip(x, flat):
        ax.annotate(f"${f}", (xi - w/2, f), xytext=(0, 6),
                    textcoords="offset points", ha="center", va="bottom",
                    color=COOL, fontsize=10, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(tiers, fontsize=11, color=INK)
    ax.set_ylabel("Dollars per month")
    ax.yaxis.set_major_formatter(FuncFormatter(money))
    ax.set_ylim(0, 1750)
    ax.set_title("What you pay vs what a heavy user can pull out", pad=30)
    ax.legend(loc="upper left", frameon=False, fontsize=10,
              bbox_to_anchor=(0, 1.10))

    fig.text(0.5, 0.005,
             "Anthropic tiers, June 2026. Flat fee vs the API-rate value a heavy user can consume "
             "before throttling. Sources: finout.io, productcompass.pm, lowcode.agency.",
             ha="center", color=MUTED, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig("charts/chartA_subsidy.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)

# ===========================================================================
# CHART B — single-subscriber crossover (computed)
# ===========================================================================
def chart_crossover():
    c = D.CROSSOVER
    cost_per_task = (c["in_tokens_per_task"]*c["in_rate_per_token"]
                     + c["out_tokens_per_task"]*c["out_rate_per_token"])
    REV = c["flat_revenue"]
    breakeven = REV / cost_per_task

    tasks = np.linspace(0, 3000, 200)
    cost = tasks * cost_per_task

    fig, ax = plt.subplots(figsize=(9, 5.2))
    style(ax)
    ax.axhline(REV, color=COOL, linewidth=2.4, zorder=5)
    ax.annotate(f"flat revenue  ${int(REV)}/mo", xy=(120, REV),
                xytext=(120, REV + 2.5), color=COOL, fontsize=10.5)
    ax.plot(tasks, cost, color=ACCENT, linewidth=2.6, zorder=6)
    ax.annotate("cost to serve\n(computed from API rates)",
                xy=(2650, cost[-1]*0.88), color=ACCENT, fontsize=10.5,
                ha="right", va="center")
    mask = tasks >= breakeven
    ax.fill_between(tasks[mask], REV, cost[mask], color=FILL, zorder=2)
    ax.axvline(breakeven, color=MUTED, linewidth=1, linestyle=(0, (4, 4)), zorder=4)
    ax.annotate(f"break-even\n≈ {int(round(breakeven, -1)):,} interactions/mo",
                xy=(breakeven, 33), xytext=(breakeven - 90, 38),
                ha="right", color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.annotate("provider profits", xy=(breakeven*0.42, 6.5), color=COOL,
                fontsize=10.5, ha="center")
    ax.annotate("provider loses money", xy=(breakeven + (3000-breakeven)/2, 6.5),
                color=ACCENT, fontsize=10.5, ha="center")
    ax.annotate("agents live\nout here →", xy=(2750, 19), color=ACCENT,
                fontsize=10, ha="center", style="italic")
    ax.set_xlim(0, 3000); ax.set_ylim(0, 46)
    ax.set_xlabel("Model interactions per month  (chat messages, or agent steps)")
    ax.set_ylabel("Dollars per month")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${int(v)}"))
    ax.set_title("Where a flat subscriber turns unprofitable", pad=14)
    fig.text(0.5, 0.005,
             "Computed from published Claude Sonnet 4.6 API rates ($3/$15 per 1M tokens, June 2026) "
             "at ~1,500 in / ~700 out tokens per interaction.",
             ha="center", color=MUTED, fontsize=9)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig("charts/chartB_crossover.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return cost_per_task, breakeven

# ===========================================================================
# CHART C — cheaper tokens, bigger bills (sourced magnitudes, indexed)
# ===========================================================================
def chart_divergence():
    fig, ax1 = plt.subplots(figsize=(9, 5.2))
    style(ax1)
    x = np.linspace(0, 24, 100)
    price = 100 * (1/D.DIVERGENCE["token_price_drop_factor"]) ** (x / 24)
    spend = 100 * (D.DIVERGENCE["spend_growth_multiple"]) ** (x / 24)
    ax2 = ax1.twinx()
    ax1.plot(x, price, color=COOL, linewidth=2.6, zorder=5)
    ax2.plot(x, spend, color=ACCENT, linewidth=2.6, zorder=5)
    ax1.set_yscale("log")
    ax1.set_ylabel("Price per token  (indexed, log scale)", color=COOL)
    ax2.set_ylabel("Total spend  (indexed)", color=ACCENT)
    ax1.tick_params(axis="y", colors=COOL); ax2.tick_params(axis="y", colors=ACCENT)
    ax2.spines["top"].set_visible(False)
    ax1.set_xticks([0, 6, 12, 18, 24]); ax1.set_xticklabels(["2024","","2025","","2026"])
    ax1.annotate("price per token\n≈ 280x cheaper", xy=(24, price[-1]),
                 xytext=(15.5, price[-1]*6), color=COOL, fontsize=11, ha="left",
                 va="center", arrowprops=dict(arrowstyle="-", color=COOL, lw=0.8))
    ax2.annotate("total spend\n≈ 320% higher", xy=(21, spend[int(len(spend)*21/24)]),
                 xytext=(8.5, spend[-1]*0.74), color=ACCENT, fontsize=11, ha="left",
                 va="center", arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
    ax1.set_title("Cheaper tokens, bigger bills", pad=14)
    fig.text(0.5, 0.005,
             "Two years: price per token fell ~280x, total enterprise AI spend rose ~320%.  "
             "Sources: 2026 inference-cost analyses; Goldman Sachs Research.",
             ha="center", color=MUTED, fontsize=9)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig("charts/chartC_divergence.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)

# ===========================================================================
# CHART D — the pricing ladder (refreshed)
# ===========================================================================
def chart_ladder():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    style(ax)
    providers = list(D.FLAT_TIERS.keys())
    colors = [COOL, ACCENT, "#27708a"]
    xpos = list(range(len(providers)))
    for xi, p, c in zip(xpos, providers, colors):
        items = list(D.FLAT_TIERS[p].items())
        for label, price in items:
            ax.scatter([xi], [price], s=70, color=c, zorder=5)
            ax.annotate(f"{label}  ${price}", (xi, price), xytext=(12, 0),
                        textcoords="offset points", va="center", fontsize=9.5, color=INK)
        ys = [v for _, v in items]
        ax.plot([xi]*len(ys), ys, color=c, linewidth=1.2, alpha=0.4, zorder=3)
    ax.axhspan(18, 22, color="#fff3b0", alpha=0.6, zorder=1)
    ax.annotate("the $20 on-ramp, held steady", xy=(2.55, 20), fontsize=9.5,
                color="#8a6d00", va="center")
    ax.set_xlim(-0.4, 3.3); ax.set_ylim(-15, 230)
    ax.set_xticks(xpos); ax.set_xticklabels(providers, color=INK, fontsize=12)
    ax.set_ylabel("Monthly price (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${int(v)}" if v >= 0 else ""))
    ax.set_title("Same ladder, three providers", pad=14)
    fig.text(0.5, 0.005,
             r"Consumer plan tiers, June 2026. A held \$20 anchor, added mid-rungs, every ladder "
             r"ending at a metered API pool above \$200.  Sources: OpenAI, Anthropic, Google.",
             ha="center", color=MUTED, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig("charts/chartD_ladder.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    chart_subsidy()
    cpt, be = chart_crossover()
    chart_divergence()
    chart_ladder()
    print(f"crossover: cost/task ${cpt:.4f}, break-even {be:.0f} interactions/mo")
    print("charts written: A_subsidy, B_crossover, C_divergence, D_ladder")
