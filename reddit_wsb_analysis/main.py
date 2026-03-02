#!/usr/bin/env python3
"""
WSB Prediction Analyzer
=======================
Fetches r/wallstreetbets posts from the past N days, extracts forward-looking
predictions (war, AI, rates, crypto, …), checks each prediction against real
market data, and prints a detailed accuracy report.

Usage
-----
    # 1. Copy and fill in credentials
    cp .env.example .env

    # 2. Install dependencies
    pip install -r requirements.txt

    # 3. Run
    python main.py

    # Optional flags:
    python main.py --days 90 --posts 400 --no-charts
    python main.py --load-cache predictions.json   # skip re-fetching
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

# Local modules
from reddit_fetcher    import fetch_wsb_posts
from prediction_extractor import batch_extract_predictions, deduplicate_predictions
from market_analyzer   import score_all_predictions, compute_accuracy_stats
from reporter          import print_full_report, save_charts, save_data

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger   = logging.getLogger(__name__)
console  = Console()

# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyse r/wallstreetbets predictions vs real market outcomes"
    )
    p.add_argument(
        "--days", type=int, default=90,
        help="How many days back to fetch Reddit posts (default: 90)"
    )
    p.add_argument(
        "--posts", type=int, default=500,
        help="Max Reddit posts to fetch (default: 500)"
    )
    p.add_argument(
        "--comments", type=int, default=200,
        help="Max comments per post (default: 200)"
    )
    p.add_argument(
        "--no-charts", action="store_true",
        help="Skip generating PNG charts"
    )
    p.add_argument(
        "--no-save", action="store_true",
        help="Do not save CSV/JSON output files"
    )
    p.add_argument(
        "--load-cache", metavar="PATH",
        help="Load previously extracted predictions from a JSON file (skips fetch + extract)"
    )
    p.add_argument(
        "--save-posts", metavar="PATH",
        help="Save raw fetched posts to JSON file for later reuse"
    )
    p.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose (DEBUG) logging"
    )
    return p.parse_args()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_cache(path: str) -> list[dict]:
    with open(path) as fh:
        data = json.load(fh)
    console.print(f"[dim]Loaded {len(data)} predictions from cache: {path}[/dim]")
    return data


def _save_posts(posts: list[dict], path: str) -> None:
    with open(path, "w") as fh:
        json.dump(posts, fh, indent=2, default=str)
    console.print(f"[dim]Raw posts saved to {path}[/dim]")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    load_dotenv()          # load .env if present
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # ── Step 1: Fetch posts (or load from cache) ──────────────────────────────
    predictions: list[dict]

    if args.load_cache:
        predictions = _load_cache(args.load_cache)
    else:
        console.rule("[bold cyan]Step 1 — Fetching Reddit Posts")
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(
                    f"Fetching up to {args.posts} posts from r/wallstreetbets "
                    f"(past {args.days} days)…",
                    total=None,
                )
                posts = fetch_wsb_posts(
                    lookback_days=args.days,
                    max_posts=args.posts,
                    max_comments_per_post=args.comments,
                )
                progress.update(task, description=f"Fetched {len(posts)} posts. Done.")

        except EnvironmentError as exc:
            console.print(f"[bold red]Configuration error:[/bold red] {exc}")
            return 1

        if args.save_posts:
            _save_posts(posts, args.save_posts)

        # ── Step 2: Extract predictions using Claude ──────────────────────────
        console.rule("[bold cyan]Step 2 — Extracting Predictions via Claude AI")
        console.print(
            f"[dim]Analysing {len(posts)} posts with claude-haiku-4-5…[/dim]"
        )

        try:
            raw_predictions = batch_extract_predictions(posts)
        except EnvironmentError as exc:
            console.print(f"[bold red]Configuration error:[/bold red] {exc}")
            return 1

        predictions = deduplicate_predictions(raw_predictions)
        console.print(
            f"[green]Extracted {len(raw_predictions)} raw → {len(predictions)} unique predictions[/green]"
        )

    # ── Step 3: Score against market data ────────────────────────────────────
    console.rule("[bold cyan]Step 3 — Scoring Predictions Against Market Data")
    console.print("[dim]Downloading historical price data via yfinance…[/dim]")
    predictions = score_all_predictions(predictions)

    # ── Step 4: Compute stats ─────────────────────────────────────────────────
    stats = compute_accuracy_stats(predictions)

    if not stats:
        console.print("[yellow]No resolved predictions found. Try a longer lookback window.[/yellow]")
        return 0

    # ── Step 5: Report ────────────────────────────────────────────────────────
    console.rule("[bold cyan]Step 4 — Report")
    print_full_report(stats)

    # ── Step 6: Save artefacts ────────────────────────────────────────────────
    if not args.no_save:
        save_data(predictions, stats)

    if not args.no_charts:
        save_charts(predictions, stats)

    return 0


if __name__ == "__main__":
    sys.exit(main())
