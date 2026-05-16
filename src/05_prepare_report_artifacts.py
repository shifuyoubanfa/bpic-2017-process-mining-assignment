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


def export_final_heuristics_report_figure() -> None:
    """Create a readable final BPMN-style overview for the report body."""
    FIGURES_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7.0, 2.35))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.1)
    ax.axis("off")

    def box(x, y, text, w=1.55, h=0.48, fc="#EAF2FA"):
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            linewidth=0.9,
            edgecolor="#1F4E79",
            facecolor=fc,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.0)

    def gate(x, y, label="X"):
        size = 0.22
        pts = [(x, y + size), (x + size, y), (x, y - size), (x - size, y)]
        ax.add_patch(
            Polygon(pts, closed=True, linewidth=0.8, edgecolor="#8A5A00", facecolor="#FFF1CC")
        )
        ax.text(x, y, label, ha="center", va="center", fontsize=6.2, fontweight="bold")

    def arrow(start, end, label=None):
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops=dict(arrowstyle="->", lw=0.85, color="#333333"),
        )
        if label:
            ax.text(
                (start[0] + end[0]) / 2,
                (start[1] + end[1]) / 2 + 0.12,
                label,
                ha="center",
                va="bottom",
                fontsize=5.7,
            )

    ax.add_patch(plt.Circle((0.55, 2.1), 0.13, color="#47A447", fill=False, linewidth=1.0))
    box(1.05, 1.86, "Create\napplication")
    box(3.0, 1.86, "Complete\napplication")
    box(4.95, 1.86, "Create /\nsend offer")
    box(6.9, 1.86, "Validate\napplication")
    gate(8.8, 2.1)
    box(9.6, 2.95, "Accept /\nactivate", fc="#E8F6E8")
    box(9.6, 1.86, "Return /\nrework")
    box(9.6, 0.77, "Deny /\nincomplete", fc="#F9E5E5")
    box(12.0, 1.86, "Close\ncase", w=1.25)
    ax.add_patch(plt.Circle((13.55, 2.1), 0.13, color="#C95D2E", fill=False, linewidth=1.0))

    arrow((0.68, 2.1), (1.05, 2.1))
    arrow((2.6, 2.1), (3.0, 2.1))
    arrow((4.55, 2.1), (4.95, 2.1))
    arrow((6.5, 2.1), (6.9, 2.1))
    arrow((8.45, 2.1), (8.58, 2.1))
    arrow((8.99, 2.27), (9.6, 3.19))
    arrow((9.03, 2.1), (9.6, 2.1))
    arrow((8.99, 1.93), (9.6, 1.01))
    arrow((11.15, 3.19), (12.0, 2.25))
    arrow((11.15, 2.1), (12.0, 2.1))
    arrow((11.15, 1.01), (12.0, 1.95))
    arrow((13.25, 2.1), (13.42, 2.1))
    arrow((10.35, 1.86), (7.7, 1.28))
    arrow((7.55, 1.28), (7.55, 1.86))

    fig.tight_layout(pad=0.2)
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES_MODELS_DIR / f"final_heuristics_bpmn_report.{suffix}", dpi=300)
    plt.close(fig)


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


def export_decision_aware_report_figure() -> None:
    """Create a clean one-column decision-aware BPMN-style figure for the report body."""
    FIGURES_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(3.45, 3.55))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def box(x, y, w, h, text, fc="#E8F1FA", fs=5.9):
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            linewidth=0.85,
            edgecolor="#1F4E79",
            facecolor=fc,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)

    def gateway(x, y, text):
        size = 0.32
        pts = [(x, y + size), (x + size, y), (x, y - size), (x - size, y)]
        ax.add_patch(
            Polygon(pts, closed=True, linewidth=0.85, edgecolor="#8A5A00", facecolor="#FFF1CC")
        )
        ax.text(x, y, text, ha="center", va="center", fontsize=5.8, fontweight="bold")

    def arr(start, end, label=None, fs=4.8):
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops=dict(arrowstyle="->", lw=0.85, color="#333333"),
        )
        if label:
            ax.text(
                (start[0] + end[0]) / 2,
                (start[1] + end[1]) / 2 + 0.18,
                label,
                ha="center",
                va="bottom",
                fontsize=fs,
            )

    box(0.45, 8.85, 2.25, 0.48, "Application")
    box(3.85, 8.85, 2.25, 0.48, "Offer")
    box(7.15, 8.85, 2.35, 0.48, "A_Validating")
    arr((2.7, 9.09), (3.85, 9.09))
    arr((6.1, 9.09), (7.15, 9.09))

    gateway(5.0, 7.45, "D1")
    arr((8.1, 8.85), (5.28, 7.72))
    box(0.45, 6.15, 2.25, 0.52, "O_Returned", "#EEF5FF")
    box(3.7, 6.15, 2.6, 0.52, "Accept /\npending", "#E8F6E8")
    box(7.2, 6.15, 2.35, 0.52, "Deny /\nincomplete", "#F9E5E5")
    arr((4.75, 7.25), (1.6, 6.67))
    arr((5.0, 7.13), (5.0, 6.67))
    arr((5.25, 7.25), (8.35, 6.67))

    gateway(5.0, 4.72, "D2")
    arr((1.6, 6.15), (4.72, 4.98), "returned path")
    box(0.45, 3.45, 2.45, 0.52, "Incomplete /\ncall files", "#EEF5FF")
    box(3.75, 3.45, 2.5, 0.52, "Revalidate", "#EEF5FF")
    box(7.25, 3.45, 2.3, 0.52, "Accept /\ndeny", "#E8F6E8")
    arr((4.74, 4.48), (1.68, 3.97))
    arr((5.0, 4.36), (5.0, 3.97))
    arr((5.26, 4.48), (8.4, 3.97))

    box(0.85, 1.55, 2.3, 0.52, "Continue")
    box(6.9, 1.55, 2.3, 0.52, "Close case")
    arr((1.68, 3.45), (1.95, 2.07))
    arr((8.4, 3.45), (8.05, 2.07))
    arr((3.15, 1.81), (6.9, 1.81))

    fig.tight_layout(pad=0.3)
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES_MODELS_DIR / f"final_decision_aware_bpmn_report.{suffix}", dpi=300)
    plt.close(fig)


def main() -> None:
    export_final_heuristics_bpmn()
    export_final_heuristics_report_figure()
    export_decision_aware_overview()
    export_decision_aware_report_figure()
    print("Report artifacts created:")
    print(f"- {FINAL_BPMN.relative_to(PROJECT_ROOT)}")
    print("- figures/process_models/final_heuristics_bpmn.pdf/png")
    print("- figures/process_models/final_heuristics_bpmn_report.pdf/png")
    print("- figures/process_models/final_decision_aware_bpmn.pdf/png")
    print("- figures/process_models/final_decision_aware_bpmn_report.pdf/png")


if __name__ == "__main__":
    main()
