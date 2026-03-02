"""
Market Analyzer — fetches historical price data via yfinance and scores
each WSB prediction as CORRECT, INCORRECT, or INCONCLUSIVE.
"""

import logging
from datetime import datetime, timezone, timedelta
from functools import lru_cache
from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf

try:
    from demo_data import MOCK_PRICES as _MOCK_PRICES
except ImportError:
    _MOCK_PRICES: dict = {}

logger = logging.getLogger(__name__)

# ── Topic → representative instruments ──────────────────────────────────────
TOPIC_PROXIES: dict[str, list[str]] = {
    "war":       ["LMT", "RTX", "NOC", "GD", "BA", "XAR", "ITA"],
    "ai":        ["NVDA", "MSFT", "GOOGL", "AMD", "SMCI", "PLTR", "AI"],
    "fed_rates": ["TLT", "IEF", "GLD", "SPY", "^TNX"],          # ^TNX = 10yr yield
    "tech":      ["QQQ", "AAPL", "MSFT", "AMZN", "META", "TSLA"],
    "energy":    ["XOM", "CVX", "XLE", "OIH", "USO"],
    "crypto":    ["BTC-USD", "ETH-USD", "COIN", "MSTR"],
    "market":    ["SPY", "QQQ", "DIA", "^VIX"],
    "other":     ["SPY"],
}

# ── Price change thresholds ──────────────────────────────────────────────────
# A move of > SIGNIFICANT_MOVE% in the predicted direction = CORRECT
SIGNIFICANT_MOVE_PCT = 3.0      # 3 % minimum "significant" move
STRONG_MOVE_PCT = 10.0          # 10 % = strong confirmation


@lru_cache(maxsize=512)
def _get_price_history(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Cached yfinance download."""
    try:
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        return df
    except Exception as exc:
        logger.warning("yfinance download failed for %s: %s", ticker, exc)
        return pd.DataFrame()


def _mock_pct_change(ticker: str, from_dt: datetime, to_dt: datetime) -> float | None:
    """Use pre-loaded mock prices when yfinance is unavailable."""
    prices = _MOCK_PRICES.get(ticker)
    if not prices:
        return None
    now = datetime.now(timezone.utc)
    from_days_ago = max(0, int((now - from_dt).days))
    to_days_ago   = max(0, int((now - to_dt).days))

    # Find closest available snapshots
    available = sorted(prices.keys())

    def closest(target):
        return min(available, key=lambda d: abs(d - target))

    p_start = prices[closest(from_days_ago)]
    p_end   = prices[closest(to_days_ago)]
    if p_start == 0:
        return None
    return (p_end - p_start) / p_start * 100.0


def _pct_change(ticker: str, from_dt: datetime, to_dt: datetime) -> float | None:
    """Return % price change for ticker between two dates. None on failure."""
    start = (from_dt - timedelta(days=5)).strftime("%Y-%m-%d")
    end = (to_dt + timedelta(days=5)).strftime("%Y-%m-%d")

    df = _get_price_history(ticker, start, end)
    if df.empty or "Close" not in df.columns:
        # Fall back to mock data
        return _mock_pct_change(ticker, from_dt, to_dt)

    close = df["Close"].dropna()
    if len(close) < 2:
        return _mock_pct_change(ticker, from_dt, to_dt)

    # Find the closest available trading day to from_dt and to_dt
    idx = close.index
    try:
        from_idx = idx.searchsorted(pd.Timestamp(from_dt.date()))
        to_idx   = idx.searchsorted(pd.Timestamp(to_dt.date()))
        from_idx = min(from_idx, len(close) - 1)
        to_idx   = min(to_idx,   len(close) - 1)

        price_start = float(close.iloc[from_idx])
        price_end   = float(close.iloc[to_idx])

        if price_start == 0:
            return None
        return (price_end - price_start) / price_start * 100.0
    except Exception as exc:
        logger.warning("Price calc error %s: %s", ticker, exc)
        return _mock_pct_change(ticker, from_dt, to_dt)


def _horizon_to_days(horizon: str) -> int:
    mapping = {"days": 5, "weeks": 21, "months": 60, "year+": 90}
    return mapping.get(horizon, 30)


def score_prediction(pred: dict, now: datetime | None = None) -> dict:
    """
    Evaluate whether a prediction came true by checking actual price data.

    Adds these fields to the prediction dict:
      outcome        : "correct" | "incorrect" | "partial" | "inconclusive"
      outcome_reason : human-readable explanation
      price_changes  : {ticker: pct_change, ...}
      avg_pct_change : float | None
      evaluation_dt  : ISO timestamp of end-of-horizon
    """
    if now is None:
        now = datetime.now(timezone.utc)

    post_dt = datetime.fromtimestamp(pred["post_created_utc"], tz=timezone.utc)
    horizon_days = _horizon_to_days(pred.get("time_horizon", "months"))
    eval_dt = post_dt + timedelta(days=horizon_days)

    # If the prediction horizon hasn't expired yet, mark inconclusive
    if eval_dt > now:
        pred["outcome"] = "inconclusive"
        pred["outcome_reason"] = f"Horizon ({pred.get('time_horizon')}) not yet elapsed"
        pred["price_changes"] = {}
        pred["avg_pct_change"] = None
        pred["evaluation_dt"] = eval_dt.isoformat()
        return pred

    # Resolve tickers to evaluate
    tickers = list(pred.get("tickers", []))
    topic   = pred.get("topic", "other")
    if not tickers:
        tickers = TOPIC_PROXIES.get(topic, TOPIC_PROXIES["other"])[:3]

    direction = pred.get("direction", "uncertain")

    price_changes: dict[str, float] = {}
    for ticker in tickers[:5]:   # cap at 5 tickers
        pct = _pct_change(ticker, post_dt, eval_dt)
        if pct is not None:
            price_changes[ticker] = round(pct, 2)

    pred["price_changes"] = price_changes
    pred["evaluation_dt"] = eval_dt.isoformat()

    if not price_changes:
        pred["outcome"] = "inconclusive"
        pred["outcome_reason"] = "No price data available for tickers"
        pred["avg_pct_change"] = None
        return pred

    avg_chg = float(np.mean(list(price_changes.values())))
    pred["avg_pct_change"] = round(avg_chg, 2)

    # Score against direction
    if direction == "bullish":
        if avg_chg >= STRONG_MOVE_PCT:
            pred["outcome"] = "correct"
            pred["outcome_reason"] = f"Assets rose {avg_chg:+.1f}% (strong bull move)"
        elif avg_chg >= SIGNIFICANT_MOVE_PCT:
            pred["outcome"] = "correct"
            pred["outcome_reason"] = f"Assets rose {avg_chg:+.1f}% (moderate bull move)"
        elif avg_chg >= 0:
            pred["outcome"] = "partial"
            pred["outcome_reason"] = f"Assets rose only {avg_chg:+.1f}% (weak move)"
        else:
            pred["outcome"] = "incorrect"
            pred["outcome_reason"] = f"Assets fell {avg_chg:+.1f}% (against bull prediction)"

    elif direction == "bearish":
        if avg_chg <= -STRONG_MOVE_PCT:
            pred["outcome"] = "correct"
            pred["outcome_reason"] = f"Assets fell {avg_chg:+.1f}% (strong bear move)"
        elif avg_chg <= -SIGNIFICANT_MOVE_PCT:
            pred["outcome"] = "correct"
            pred["outcome_reason"] = f"Assets fell {avg_chg:+.1f}% (moderate bear move)"
        elif avg_chg <= 0:
            pred["outcome"] = "partial"
            pred["outcome_reason"] = f"Assets fell only {avg_chg:+.1f}% (weak move)"
        else:
            pred["outcome"] = "incorrect"
            pred["outcome_reason"] = f"Assets rose {avg_chg:+.1f}% (against bear prediction)"

    else:
        # neutral / uncertain — just note the actual move
        pred["outcome"] = "inconclusive"
        pred["outcome_reason"] = f"No directional prediction; avg move was {avg_chg:+.1f}%"

    return pred


def score_all_predictions(predictions: list[dict]) -> list[dict]:
    """Score a list of predictions and return enriched list."""
    now = datetime.now(timezone.utc)
    total = len(predictions)
    for i, pred in enumerate(predictions):
        logger.info("Scoring prediction [%d/%d]", i + 1, total)
        score_prediction(pred, now=now)
    return predictions


def compute_accuracy_stats(predictions: list[dict]) -> dict[str, Any]:
    """
    Aggregate accuracy statistics from scored predictions.
    Returns a nested dict ready for reporting.
    """
    df = pd.DataFrame(predictions)
    if df.empty:
        return {}

    # Only look at directional (non-neutral) predictions that have resolved
    resolved = df[df["outcome"].isin(["correct", "incorrect", "partial"])]
    correct   = (resolved["outcome"] == "correct").sum()
    partial   = (resolved["outcome"] == "partial").sum()
    incorrect = (resolved["outcome"] == "incorrect").sum()
    n         = len(resolved)

    overall_accuracy = (correct + 0.5 * partial) / n if n > 0 else 0.0

    # Per-topic breakdown
    topic_stats: dict[str, dict] = {}
    for topic in df["topic"].unique():
        t_df = resolved[resolved["topic"] == topic]
        if t_df.empty:
            continue
        t_correct   = (t_df["outcome"] == "correct").sum()
        t_partial   = (t_df["outcome"] == "partial").sum()
        t_incorrect = (t_df["outcome"] == "incorrect").sum()
        t_n         = len(t_df)
        topic_stats[topic] = {
            "n":        t_n,
            "correct":  int(t_correct),
            "partial":  int(t_partial),
            "incorrect": int(t_incorrect),
            "accuracy": round((t_correct + 0.5 * t_partial) / t_n, 3) if t_n else 0,
        }

    # Per-direction breakdown
    dir_stats: dict[str, dict] = {}
    for direction in ["bullish", "bearish"]:
        d_df = resolved[resolved["direction"] == direction]
        if d_df.empty:
            continue
        d_n = len(d_df)
        d_correct = (d_df["outcome"] == "correct").sum()
        d_partial = (d_df["outcome"] == "partial").sum()
        dir_stats[direction] = {
            "n":       d_n,
            "correct": int(d_correct),
            "partial": int(d_partial),
            "accuracy": round((d_correct + 0.5 * d_partial) / d_n, 3) if d_n else 0,
        }

    # Best & worst predictions
    scored_df = resolved.copy()
    scored_df["abs_chg"] = pd.to_numeric(scored_df["avg_pct_change"], errors="coerce").abs()
    top_correct  = scored_df[scored_df["outcome"] == "correct"].nlargest(5, "abs_chg")
    top_wrong    = scored_df[scored_df["outcome"] == "incorrect"].nlargest(5, "abs_chg")

    return {
        "total_predictions": len(df),
        "resolved_predictions": n,
        "inconclusive": int((df["outcome"] == "inconclusive").sum()),
        "correct": int(correct),
        "partial": int(partial),
        "incorrect": int(incorrect),
        "overall_accuracy": round(overall_accuracy, 3),
        "topic_stats": topic_stats,
        "direction_stats": dir_stats,
        "top_correct_predictions": top_correct.to_dict("records"),
        "top_wrong_predictions":   top_wrong.to_dict("records"),
    }
