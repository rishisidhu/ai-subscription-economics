"""
Charts for the AI subscription economics article.
All figures live in chart_data.py, each annotated with its source.

Design: Messari/financial-dashboard style. Dark header band with title, subtitle
and unit; framed, gridded plot; teal for the "in control / what you pay" element,
coral for the "problem" element (the gap, the loss zone, the rising spend, the
held anchor). Consistent across all four so they read as one set.
No source line on the image (sources live in the repo and the article).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter, MultipleLocator
import chart_data as D

# ---- palette --------------------------------------------------------------
INK     = "#0f1419"
PANEL   = "#ffffff"
HEADER  = "#0d1b1e"
HEADERTX= "#ffffff"
SUB     = "#9fb8b4"     # subtitle text on dark header
UNIT    = "#5f7a76"     # unit label on dark header
GRID    = "#e2e6ea"
AXIS    = "#aab2bd"
TXT     = "#3d4651"
MUTE    = "#8b95a1"
TEAL    = "#0f8a7e"     # "in control" / what you pay
TEALD   = "#0a5f57"     # darker teal for teal text labels
CORAL   = "#e0654f"     # "the problem" / extract / loss / rise
CORALD  = "#b03f2c"     # darker coral for coral text labels
CORAL_F = "#f6d8d1"     # coral fill, light (loss zones)

def _pick(*names):
    avail = {f.name for f in fm.fontManager.ttflist}
    for n in names:
        if n in avail:
            return n
    return "DejaVu Sans"
DISPLAY = _pick("Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans")

plt.rcParams.update({
    "font.family": DISPLAY, "font.size": 13,
    "figure.dpi": 200, "savefig.dpi": 200,
    "text.parse_math": False,
})

# ---- shared scaffolding ---------------------------------------------------
def _frame(title, subtitle, unit, figsize=(9, 5.8),
           plot_rect=(0.10, 0.13, 0.86, 0.68)):
    """Build figure with a dark header band and a framed plot axis."""
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor(PANEL)
    hax = fig.add_axes([0, 0.88, 1, 0.12]); hax.axis("off")
    hax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=hax.transAxes,
                                color=HEADER, zorder=0))
    hax.text(0.018, 0.62, title.upper(), transform=hax.transAxes, ha="left",
             va="center", color=HEADERTX, fontsize=15, fontweight="bold",
             family=DISPLAY)
    hax.text(0.018, 0.24, subtitle, transform=hax.transAxes, ha="left",
             va="center", color=SUB, fontsize=10.5)
    if unit:
        hax.text(0.982, 0.5, unit, transform=hax.transAxes, ha="right",
                 va="center", color=UNIT, fontsize=9, fontweight="bold")
    ax = fig.add_axes(list(plot_rect)); ax.set_facecolor(PANEL)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(AXIS); ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(colors=TXT, length=0, labelsize=10.5)
    return fig, ax, hax

def _legend(ax, items, y=-0.17):
    """items: list of (color, label). Draws rectangle chips (font-independent)."""
    from matplotlib.patches import Rectangle
    x = 0.0
    chip_w, chip_h = 0.018, 0.030
    for color, label in items:
        ax.add_patch(Rectangle((x, y - chip_h/2), chip_w, chip_h,
                               transform=ax.transAxes, color=color,
                               clip_on=False, zorder=6))
        ax.text(x + chip_w + 0.008, y, label, color=TXT, transform=ax.transAxes,
                fontsize=10, va="center")
        x += chip_w + 0.008 + 0.0125 * len(label) + 0.03

def _save(fig, path):
    fig.savefig(path, bbox_inches="tight", facecolor=PANEL, pad_inches=0.25)
    plt.close(fig)

# ===========================================================================
# CHART A — the subsidy (paired bars: pay vs extract)
# ===========================================================================
def chart_subsidy():
    fig, ax, _ = _frame("What you pay vs what you can take",
                        "Flat monthly fee against the API-equivalent value a heavy user can pull through each plan",
                        "USD / MONTH")
    tiers = [t[0].split("\n")[0] for t in D.SUBSIDY]
    flat  = [t[1] for t in D.SUBSIDY]
    low   = [t[2] for t in D.SUBSIDY]
    high  = [t[3] for t in D.SUBSIDY]
    y = np.arange(len(tiers))[::-1]
    bh = 0.34
    ax.xaxis.grid(True, color=GRID, lw=1)

    for yi, f, l, h in zip(y, flat, low, high):
        ax.barh(yi + bh*0.55, f, height=bh, color=TEAL, zorder=4)
        ax.barh(yi - bh*0.55, h, height=bh, color=CORAL, zorder=3)
        ax.plot([l, l], [yi - bh*0.55 - bh/2, yi - bh*0.55 + bh/2],
                color="#ffffff", lw=1.6, zorder=5)
    for yi, f, l, h in zip(y, flat, low, high):
        ax.text(f + 14, yi + bh*0.55, f"${f}", va="center", ha="left",
                color=TEALD, fontsize=10.5, fontweight="bold", zorder=6)
        ax.text(h + 14, yi - bh*0.55, f"${l:,}–${h:,}", va="center", ha="left",
                color=CORALD, fontsize=10.5, fontweight="bold", zorder=6)

    ax.set_yticks(y); ax.set_yticklabels(tiers, fontsize=12.5, color=INK, fontweight="bold")
    ax.set_xlim(0, 2600); ax.xaxis.set_major_locator(MultipleLocator(500))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${int(v):,}"))
    ax.margins(y=0.18)
    _legend(ax, [(TEAL, "what you pay"),
                 (CORAL, "value a heavy user can extract (range)")])
    _save(fig, "charts/chartA_subsidy.png")

# ===========================================================================
# CHART B — single-subscriber crossover (computed)
# ===========================================================================
def chart_crossover():
    c = D.CROSSOVER
    # cost per interaction = cached context (0.1x) + fresh input + cache write (1.25x) + output
    cpt = (c["cached_tokens"]      * c["cache_read_rate_per_token"]
           + c["fresh_in_tokens"]  * c["in_rate_per_token"]
           + c["cache_write_tokens"] * c["cache_write_rate_per_token"]
           + c["out_tokens"]       * c["out_rate_per_token"])
    REV = c["flat_revenue"]
    be = REV / cpt
    x = np.linspace(0, 3000, 240)
    cost = x * cpt

    fig, ax, _ = _frame("Where a flat subscriber turns unprofitable",
                        "One agent interaction, priced at Sonnet rates with caching: cost rises with use, the $20 fee does not",
                        "USD / MONTH")
    ax.grid(True, color=GRID, lw=1)

    m = x >= be
    ax.fill_between(x[m], REV, cost[m], color=CORAL_F, zorder=1)
    ax.axhline(REV, color=TEAL, lw=2.4, zorder=4)
    ax.plot(x, cost, color=INK, lw=2.8, zorder=5)
    ax.axvline(be, color=MUTE, lw=1, ls=(0, (3, 3)), zorder=3)

    ax.annotate(f"break-even ≈ {int(round(be,-1)):,} interactions",
                xy=(be, REV), xytext=(be+50, 6.5), fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTE, lw=1))
    ax.text(50, REV+1.6, "flat revenue  $20", fontsize=11, color=TEALD)
    ax.text(1680, 30, "cost to serve", ha="center", fontsize=12, color=INK)
    ax.text(1450, 24, "every interaction past\nbreak-even loses money",
            fontsize=11, color=CORALD, ha="center")

    ax.set_xlim(0, 2000); ax.set_ylim(0, 46)
    ax.xaxis.set_major_locator(MultipleLocator(500))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${int(v)}"))
    ax.set_xlabel("Agent interactions per month (one resend-and-respond turn each)",
                  fontsize=10.5, color=TXT)
    _save(fig, "charts/chartB_crossover.png")
    return cpt, be

# ===========================================================================
# CHART C — cheaper tokens, bigger bills (real endpoints, two panels)
# ===========================================================================
def chart_divergence():
    d = D.DIVERGENCE
    fig = plt.figure(figsize=(9, 5.6)); fig.patch.set_facecolor(PANEL)
    hax = fig.add_axes([0, 0.88, 1, 0.12]); hax.axis("off")
    hax.add_patch(plt.Rectangle((0,0),1,1, transform=hax.transAxes, color=HEADER, zorder=0))
    hax.text(0.018, 0.62, "CHEAPER TOKENS, BIGGER BILLS", transform=hax.transAxes,
             ha="left", va="center", color=HEADERTX, fontsize=15, fontweight="bold", family=DISPLAY)
    hax.text(0.018, 0.24, "Unit price collapsed while total enterprise spending climbed",
             transform=hax.transAxes, ha="left", va="center", color=SUB, fontsize=10.5)

    axL = fig.add_axes([0.08, 0.18, 0.38, 0.60])
    axR = fig.add_axes([0.58, 0.18, 0.38, 0.60])
    for ax in (axL, axR):
        ax.set_facecolor(PANEL); ax.set_axisbelow(True)
        ax.grid(True, color=GRID, lw=1)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(AXIS); ax.spines["bottom"].set_color(AXIS)
        ax.tick_params(colors=TXT, length=0, labelsize=10.5)
        ax.set_xticks([0, 1]); ax.set_xlim(-0.35, 1.35)

    # left: price collapse (teal = the falling/"good" curve)
    axL.plot([0,1], [d["price_start"], d["price_end"]], color=TEAL, lw=3,
             marker="o", markersize=9, zorder=5)
    axL.set_xticklabels([d["price_start_label"], d["price_end_label"]], color=TXT)
    axL.annotate(f"${d['price_start']:.2f}", (0, d["price_start"]), xytext=(0,12),
                 textcoords="offset points", ha="center", fontsize=12, fontweight="bold", color=INK)
    axL.annotate(f"${d['price_end']:.2f}", (1, d["price_end"]), xytext=(0,16),
                 textcoords="offset points", ha="center", fontsize=12, fontweight="bold", color=INK)
    axL.set_ylim(-2, d["price_start"]*1.2)
    axL.text(0.78, 0.62, "≈ 280×\ncheaper", transform=axL.transAxes, ha="center",
             va="center", fontsize=13, color=MUTE, fontweight="bold")
    axL.set_title("Price per 1M tokens (GPT-3.5-class)", fontsize=11, color=TXT, pad=24)

    # right: spend rise (coral = the rising/"problem" curve)
    axR.plot([0,1], [d["spend_start"], d["spend_end"]], color=CORAL, lw=3,
             marker="o", markersize=9, zorder=5)
    axR.set_xticklabels([d["spend_start_label"], d["spend_end_label"]], color=TXT)
    axR.annotate(f"${d['spend_start']:.1f}B", (0, d["spend_start"]), xytext=(-4,16),
                 textcoords="offset points", ha="right", fontsize=12, fontweight="bold", color=INK)
    axR.annotate(f"${d['spend_end']:.0f}B", (1, d["spend_end"]), xytext=(0,12),
                 textcoords="offset points", ha="center", fontsize=12, fontweight="bold", color=INK)
    axR.set_ylim(0, d["spend_end"]*1.2)
    axR.text(0.22, 0.68, "≈ 3×\nhigher", transform=axR.transAxes, ha="center",
             va="center", fontsize=13, color=MUTE, fontweight="bold")
    axR.set_title("Total enterprise spend on generative AI", fontsize=11, color=TXT, pad=24)

    _save(fig, "charts/chartC_divergence.png")

# ===========================================================================
# CHART D — the pricing ladder, three providers
# ===========================================================================
def chart_ladder():
    fig, ax, _ = _frame("Same ladder, three providers",
                        "A held $20 on-ramp, mid-rungs added for price discrimination, a metered pool above",
                        "USD / MONTH")
    ax.yaxis.grid(True, color=GRID, lw=1)
    providers = list(D.FLAT_TIERS.keys())
    xpos = list(range(len(providers)))
    for xi, p in zip(xpos, providers):
        items = list(D.FLAT_TIERS[p].items())
        ys = [v for _, v in items]
        ax.plot([xi]*len(ys), ys, color="#cdd4db", lw=2.5, zorder=2)
        for label, price in items:
            ax.scatter([xi], [price], s=64, color=INK, zorder=5)
            ax.annotate(f"{label}  ${price}", (xi, price), xytext=(13, 7),
                        textcoords="offset points", va="center", fontsize=10.5, color=TXT)
    # anchor line: draw only across the dot columns, not through the right-side labels
    ax.plot([-0.4, len(providers)-1 + 0.02], [20, 20], color=CORAL, lw=2,
            alpha=0.85, zorder=1)
    ax.annotate("the $20 anchor, held for 3 years", xy=(len(providers)-1, 33),
                xytext=(0, 0), textcoords="offset points", fontsize=10.5,
                color=CORALD, ha="center", fontweight="bold")

    ax.set_xlim(-0.4, len(providers)-0.05); ax.set_ylim(-15, 235)
    ax.set_xticks(xpos); ax.set_xticklabels(providers, fontsize=12.5, color=INK, fontweight="bold")
    ax.set_yticks([0, 50, 100, 150, 200])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${int(v)}"))
    _save(fig, "charts/chartD_ladder.png")

if __name__ == "__main__":
    chart_subsidy()
    cpt, be = chart_crossover()
    chart_divergence()
    chart_ladder()
    print(f"crossover: cost/task ${cpt:.4f}, break-even {be:.0f} interactions/mo")
    print("charts written: A_subsidy, B_crossover, C_divergence, D_ladder")
