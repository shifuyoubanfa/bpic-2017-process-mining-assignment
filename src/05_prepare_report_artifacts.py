"""Prepare report-only process model artifacts.

This script keeps final report preparation reproducible without rerunning the
heavy discovery notebooks. It converts the selected Heuristics Miner Petri net
to BPMN and creates a compact decision-aware BPMN-style overview figure.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
import pm4py


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_MODELS_DIR = PROJECT_ROOT / "results" / "process_models"
FIGURES_MODELS_DIR = PROJECT_ROOT / "figures" / "process_models"

HEURISTICS_PNML = RESULTS_MODELS_DIR / "heuristics_miner.pnml"
FINAL_BPMN = RESULTS_MODELS_DIR / "final_heuristics_miner.bpmn"


def _rounded_box(ax, xy, width, height, text, facecolor="#E8F1FA", fontsize=8):
    """Draw a BPMN-style activity block."""
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.03,rounding_size=0.06",
        linewidth=1.0,
        edgecolor="#1F4E79",
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        wrap=True,
    )


def _diamond(ax, center, size, text):
    """Draw a BPMN-style XOR gateway."""
    x, y = center
    points = [(x, y + size), (x + size, y), (x, y - size), (x - size, y)]
    ax.add_patch(
        Polygon(points, closed=True, linewidth=1.0, edgecolor="#8A5A00", facecolor="#FFF1CC")
    )
    ax.text(x, y, text, ha="center", va="center", fontsize=8, fontweight="bold")


def _arrow(ax, start, end, label=None, dy=0.0):
    """Draw a directed sequence-flow arrow."""
    ax.annotate(
        "",
        xy=(end[0], end[1] + dy),
        xytext=(start[0], start[1] + dy),
        arrowprops=dict(arrowstyle="->", lw=1.1, color="#333333"),
    )
    if label:
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2 + dy + 0.13,
            label,
            ha="center",
            va="bottom",
            fontsize=7,
        )


def export_final_heuristics_bpmn() -> None:
    """Convert the selected Heuristics Miner Petri net to BPMN and save figures."""
    if not HEURISTICS_PNML.exists():
        raise FileNotFoundError(f"Missing input model: {HEURISTICS_PNML}")

    RESULTS_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    net, initial_marking, final_marking = pm4py.read_pnml(str(HEURISTICS_PNML))
    bpmn_graph = pm4py.convert_to_bpmn(net, initial_marking, final_marking)
    pm4py.write_bpmn(bpmn_graph, str(FINAL_BPMN))

    for suffix in ("pdf", "png"):
        pm4py.save_vis_bpmn(
            bpmn_graph,
            str(FIGURES_MODELS_DIR / f"final_heuristics_bpmn.{suffix}"),
            rankdir="LR",
            graph_title="Final BPMN model derived from Heuristics Miner",
        )


def export_decision_aware_overview() -> None:
    """Create a compact report figure with the two mined decision blocks."""
    FIGURES_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(13, 5.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    # Main application and offer path.
    _rounded_box(ax, (0.25, 2.35), 1.35, 0.55, "Create\napplication")
    _rounded_box(ax, (1.95, 2.35), 1.35, 0.55, "Complete\napplication")
    _rounded_box(ax, (3.65, 2.35), 1.25, 0.55, "Create\noffer")
    _rounded_box(ax, (5.2, 2.35), 1.25, 0.55, "Send /\nreturn offer")
    _rounded_box(ax, (10.9, 2.35), 1.35, 0.55, "Close\ncase")

    _arrow(ax, (1.6, 2.63), (1.95, 2.63))
    _arrow(ax, (3.3, 2.63), (3.65, 2.63))
    _arrow(ax, (4.9, 2.63), (5.2, 2.63))

    # Decision gateway after validating.
    _rounded_box(ax, (6.8, 2.35), 1.15, 0.55, "Validate\napplication")
    _diamond(ax, (8.55, 2.63), 0.38, "X")
    _arrow(ax, (6.45, 2.63), (6.8, 2.63))
    _arrow(ax, (7.95, 2.63), (8.17, 2.63))

    _rounded_box(ax, (9.15, 3.65), 1.25, 0.5, "Accept /\npending", "#E8F6E8")
    _rounded_box(ax, (9.15, 2.35), 1.25, 0.5, "Return /\nrework")
    _rounded_box(ax, (9.15, 1.05), 1.25, 0.5, "Deny /\nincomplete", "#F9E5E5")
    _arrow(ax, (8.93, 2.86), (9.15, 3.9), "O_Accepted")
    _arrow(ax, (8.95, 2.63), (9.15, 2.63), "O_Returned")
    _arrow(ax, (8.93, 2.4), (9.15, 1.3), "A_Denied / A_Incomplete")
    _arrow(ax, (10.4, 3.9), (11.15, 2.9))
    _arrow(ax, (10.4, 2.63), (10.9, 2.63))
    _arrow(ax, (10.4, 1.3), (11.15, 2.35))

    # Second decision block related to returned offers.
    _diamond(ax, (6.05, 1.05), 0.35, "X")
    _arrow(ax, (5.85, 2.35), (5.95, 1.4), "O_Returned")
    _rounded_box(ax, (6.75, 0.4), 1.3, 0.5, "Revalidate /\ncall files")
    _rounded_box(ax, (6.75, 1.5), 1.3, 0.5, "Accept /\ndeny")
    _arrow(ax, (6.4, 1.05), (6.75, 0.65), "A_Incomplete")
    _arrow(ax, (6.4, 1.05), (6.75, 1.75), "O_Accepted / A_Denied")
    _arrow(ax, (8.05, 0.65), (8.55, 2.25))
    _arrow(ax, (8.05, 1.75), (8.55, 2.25))

    # Data-aware decision annotations.
    _rounded_box(
        ax,
        (0.35, 4.25),
        5.25,
        0.65,
        "Decision block for A_Validating: elapsed time, requested amount, previous activity,\n"
        "application/offer/workflow prefix counts, loan goal, and application type",
        "#F5F5F5",
        fontsize=7,
    )
    _rounded_box(
        ax,
        (6.05, 4.25),
        5.55,
        0.65,
        "Decision block for O_Returned: previous activity, repeated incomplete/returned behavior,\n"
        "prefix length, elapsed time, requested amount, and origin counts",
        "#F5F5F5",
        fontsize=7,
    )

    ax.text(
        0.25,
        0.08,
        "Compact decision-aware view based on mined BPIC-17 complete-event behavior. "
        "Decision blocks summarize the explanatory variables used in the report.",
        fontsize=8,
        color="#444444",
    )

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES_MODELS_DIR / f"final_decision_aware_bpmn.{suffix}", dpi=300)
    plt.close(fig)


def main() -> None:
    export_final_heuristics_bpmn()
    export_decision_aware_overview()
    print("Report artifacts created:")
    print(f"- {FINAL_BPMN.relative_to(PROJECT_ROOT)}")
    print("- figures/process_models/final_heuristics_bpmn.pdf/png")
    print("- figures/process_models/final_decision_aware_bpmn.pdf/png")


if __name__ == "__main__":
    main()
