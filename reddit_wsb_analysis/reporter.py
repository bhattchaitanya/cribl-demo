"""
Reporter — generates a rich terminal report and saves optional charts/CSV.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich import box
from rich.text import Text

logger = logging.getLogger(__name__)
console = Console()

# Output directory (created if absent)
OUTPUT_DIR = Path("wsb_analysis_output")


def _ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def _outcome_style(outcome: str) -> str:
    return {
        "correct":      "bold green",
        "partial":      "yellow",
        "incorrect":    "bold red",
        "inconclusive": "dim",
    }.get(outcome, "white")


def _direction_emoji(direction: str) -> str:
    return {"bullish": "▲ ", "bearish": "▼ ", "neutral": "→ ", "uncertain": "? "}.get(
        direction, ""
    )


# ── Section printers ─────────────────────────────────────────────────────────

def print_header(stats: dict) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = (
        f"[bold cyan]r/wallstreetbets Prediction Accuracy Report[/bold cyan]\n"
        f"[dim]Generated: {ts}[/dim]"
    )
    console.print(Panel(title, expand=False))
    console.print()


def print_summary(stats: dict) -> None:
    accuracy_pct = stats["overall_accuracy"] * 100
    colour = "green" if accuracy_pct >= 55 else ("yellow" if accuracy_pct >= 45 else "red")

    tbl = Table(title="Overall Summary", box=box.ROUNDED, show_header=False)
    tbl.add_column("Metric", style="bold")
    tbl.add_column("Value")

    tbl.add_row("Total predictions extracted",  str(stats["total_predictions"]))
    tbl.add_row("Resolved (horizon elapsed)",   str(stats["resolved_predictions"]))
    tbl.add_row("Inconclusive (too early)",     str(stats["inconclusive"]))
    tbl.add_row("Correct",                      f"[green]{stats['correct']}[/green]")
    tbl.add_row("Partial",                      f"[yellow]{stats['partial']}[/yellow]")
    tbl.add_row("Incorrect",                    f"[red]{stats['incorrect']}[/red]")
    tbl.add_row(
        "Overall accuracy (correct + 0.5×partial)",
        f"[{colour}]{accuracy_pct:.1f}%[/{colour}]",
    )
    console.print(tbl)
    console.print()


def print_topic_breakdown(stats: dict) -> None:
    tbl = Table(title="Accuracy by Topic", box=box.ROUNDED)
    tbl.add_column("Topic",     style="bold cyan")
    tbl.add_column("N",         justify="right")
    tbl.add_column("Correct",   justify="right", style="green")
    tbl.add_column("Partial",   justify="right", style="yellow")
    tbl.add_column("Incorrect", justify="right", style="red")
    tbl.add_column("Accuracy",  justify="right")

    for topic, ts in sorted(
        stats["topic_stats"].items(), key=lambda x: -x[1]["accuracy"]
    ):
        acc = ts["accuracy"] * 100
        colour = "green" if acc >= 55 else ("yellow" if acc >= 45 else "red")
        tbl.add_row(
            topic.replace("_", " ").title(),
            str(ts["n"]),
            str(ts["correct"]),
            str(ts["partial"]),
            str(ts["incorrect"]),
            f"[{colour}]{acc:.1f}%[/{colour}]",
        )

    console.print(tbl)
    console.print()


def print_direction_breakdown(stats: dict) -> None:
    tbl = Table(title="Accuracy by Direction", box=box.ROUNDED)
    tbl.add_column("Direction", style="bold")
    tbl.add_column("N",        justify="right")
    tbl.add_column("Correct",  justify="right", style="green")
    tbl.add_column("Partial",  justify="right", style="yellow")
    tbl.add_column("Accuracy", justify="right")

    for direction, ds in stats.get("direction_stats", {}).items():
        acc = ds["accuracy"] * 100
        colour = "green" if acc >= 55 else ("yellow" if acc >= 45 else "red")
        tbl.add_row(
            _direction_emoji(direction) + direction.title(),
            str(ds["n"]),
            str(ds["correct"]),
            str(ds["partial"]),
            f"[{colour}]{acc:.1f}%[/{colour}]",
        )

    console.print(tbl)
    console.print()


def print_top_predictions(stats: dict) -> None:
    # Most accurate predictions
    tbl_correct = Table(title="Top 5 Most Accurate Predictions", box=box.SIMPLE_HEAVY)
    tbl_correct.add_column("Post Date", style="dim")
    tbl_correct.add_column("Topic")
    tbl_correct.add_column("Direction")
    tbl_correct.add_column("Prediction", overflow="fold", max_width=50)
    tbl_correct.add_column("Move", justify="right", style="green")
    tbl_correct.add_column("URL", overflow="fold", max_width=30, style="blue")

    for p in stats.get("top_correct_predictions", []):
        tbl_correct.add_row(
            str(p.get("post_created_dt", ""))[:10],
            p.get("topic", ""),
            _direction_emoji(p.get("direction", "")) + p.get("direction", ""),
            p.get("prediction_text", ""),
            f"{p.get('avg_pct_change', 0):+.1f}%",
            p.get("post_url", ""),
        )

    console.print(tbl_correct)
    console.print()

    # Worst predictions
    tbl_wrong = Table(title="Top 5 Most Wrong Predictions", box=box.SIMPLE_HEAVY)
    tbl_wrong.add_column("Post Date", style="dim")
    tbl_wrong.add_column("Topic")
    tbl_wrong.add_column("Direction")
    tbl_wrong.add_column("Prediction", overflow="fold", max_width=50)
    tbl_wrong.add_column("Move",     justify="right", style="red")
    tbl_wrong.add_column("URL", overflow="fold", max_width=30, style="blue")

    for p in stats.get("top_wrong_predictions", []):
        tbl_wrong.add_row(
            str(p.get("post_created_dt", ""))[:10],
            p.get("topic", ""),
            _direction_emoji(p.get("direction", "")) + p.get("direction", ""),
            p.get("prediction_text", ""),
            f"{p.get('avg_pct_change', 0):+.1f}%",
            p.get("post_url", ""),
        )

    console.print(tbl_wrong)
    console.print()


def print_full_report(stats: dict) -> None:
    print_header(stats)
    print_summary(stats)
    print_topic_breakdown(stats)
    print_direction_breakdown(stats)
    print_top_predictions(stats)


# ── Charts ────────────────────────────────────────────────────────────────────

def save_charts(predictions: list[dict], stats: dict) -> None:
    """Save PNG charts to OUTPUT_DIR."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
    except ImportError:
        logger.warning("matplotlib/seaborn not available — skipping charts")
        return

    out = _ensure_output_dir()
    sns.set_theme(style="darkgrid")

    df = pd.DataFrame(predictions)
    resolved = df[df["outcome"].isin(["correct", "incorrect", "partial"])]

    # 1. Overall outcome pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    labels  = ["Correct", "Partial", "Incorrect", "Inconclusive"]
    values  = [
        stats["correct"], stats["partial"], stats["incorrect"], stats["inconclusive"]
    ]
    colours = ["#2ecc71", "#f39c12", "#e74c3c", "#95a5a6"]
    ax.pie(values, labels=labels, colors=colours, autopct="%1.1f%%", startangle=90)
    ax.set_title("WSB Prediction Outcomes (Past 3 Months)", fontsize=14, fontweight="bold")
    fig.savefig(out / "outcome_pie.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 2. Accuracy by topic bar chart
    if stats.get("topic_stats"):
        topics     = list(stats["topic_stats"].keys())
        accuracies = [stats["topic_stats"][t]["accuracy"] * 100 for t in topics]
        counts     = [stats["topic_stats"][t]["n"] for t in topics]

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(
            [t.replace("_", "\n").title() for t in topics],
            accuracies,
            color=[
                "#2ecc71" if a >= 55 else ("#f39c12" if a >= 45 else "#e74c3c")
                for a in accuracies
            ],
        )
        ax.axhline(50, color="white", linestyle="--", alpha=0.6, label="50% (random)")
        for bar, count in zip(bars, counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                f"n={count}",
                ha="center",
                va="bottom",
                fontsize=9,
                color="white",
            )
        ax.set_ylabel("Accuracy (%)")
        ax.set_title("WSB Prediction Accuracy by Topic", fontsize=13, fontweight="bold")
        ax.set_ylim(0, 100)
        ax.legend()
        fig.tight_layout()
        fig.savefig(out / "accuracy_by_topic.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # 3. Price change distribution
    if not resolved.empty and "avg_pct_change" in resolved.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        correct_chg   = resolved[resolved["outcome"] == "correct"]["avg_pct_change"].dropna()
        incorrect_chg = resolved[resolved["outcome"] == "incorrect"]["avg_pct_change"].dropna()

        bins = np.linspace(-60, 60, 40)
        ax.hist(correct_chg,   bins=bins, alpha=0.6, color="#2ecc71", label="Correct preds")
        ax.hist(incorrect_chg, bins=bins, alpha=0.6, color="#e74c3c", label="Incorrect preds")
        ax.axvline(0, color="white", linestyle="--", alpha=0.7)
        ax.set_xlabel("Avg price change (%)")
        ax.set_ylabel("# Predictions")
        ax.set_title("Price Change Distribution — Correct vs Incorrect Predictions", fontsize=12)
        ax.legend()
        fig.tight_layout()
        fig.savefig(out / "price_change_distribution.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    logger.info("Charts saved to %s/", out)
    console.print(f"[dim]Charts saved → {out}/[/dim]")


# ── CSV / JSON export ─────────────────────────────────────────────────────────

def save_data(predictions: list[dict], stats: dict) -> None:
    out = _ensure_output_dir()
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Full predictions CSV
    df = pd.DataFrame(predictions)
    csv_path = out / f"predictions_{ts}.csv"
    df.to_csv(csv_path, index=False)
    logger.info("Predictions CSV saved: %s", csv_path)

    # Summary JSON
    json_path = out / f"stats_{ts}.json"
    with open(json_path, "w") as fh:
        json.dump(stats, fh, indent=2, default=str)
    logger.info("Stats JSON saved: %s", json_path)

    console.print(f"[dim]Data saved → {csv_path}, {json_path}[/dim]")
