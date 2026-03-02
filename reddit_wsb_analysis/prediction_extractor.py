"""
Prediction Extractor — uses the Anthropic Claude API to parse raw WSB posts
and pull out structured, verifiable predictions with associated tickers,
time-horizons, and sentiment.
"""

import json
import logging
import os
import re
import time
from typing import Any

import anthropic

logger = logging.getLogger(__name__)

# ── Ticker pattern ───────────────────────────────────────────────────────────
_TICKER_RE = re.compile(r"\b([A-Z]{1,5})\b")

# Known non-ticker uppercased words to skip
_FALSE_POSITIVES = {
    "I", "A", "THE", "AND", "OR", "BUT", "NOT", "FOR", "IN", "ON", "AT",
    "TO", "IS", "IT", "IF", "BE", "BY", "OF", "US", "MY", "SO", "DO",
    "GO", "NO", "OK", "AI", "CEO", "CFO", "CTO", "IPO", "ETF", "SEC",
    "FED", "GDP", "CPI", "PCE", "ATH", "ATL", "DD", "OTM", "ITM", "IV",
    "EOD", "EOY", "YTD", "YOY", "IMO", "TBH", "WSB", "EPS", "PE",
    "QE", "QT", "YOLO", "FOMO", "HODL", "BTFD",
}

# ── Claude prompt ─────────────────────────────────────────────────────────────
_SYSTEM_PROMPT = """\
You are a financial analyst specialising in retail investor sentiment on Reddit's
r/wallstreetbets community. Your task is to read WSB posts/comments and extract
clear, verifiable predictions about future market movements, geopolitical events
and their financial impact.

Return ONLY a JSON array. Each element must have these fields:
{
  "prediction_text": "<concise summary of the prediction>",
  "direction": "bullish" | "bearish" | "neutral" | "uncertain",
  "tickers": ["<TICKER>", ...],          // stock tickers mentioned (empty list if none)
  "asset_class": "stock" | "index" | "crypto" | "commodity" | "macro",
  "topic": "war" | "ai" | "fed_rates" | "tech" | "energy" | "crypto" | "market" | "other",
  "time_horizon": "days" | "weeks" | "months" | "year+",
  "confidence_score": 0.0-1.0,          // how specific/confident the prediction is
  "original_text": "<verbatim key sentence(s)>"
}

Rules:
- Only extract PREDICTIONS (forward-looking statements), not commentary or analysis
- Ignore memes, jokes, and posts with no actual prediction content
- A prediction must be falsifiable (e.g. "NVDA will hit $200 by March" ✓, "this market is crazy" ✗)
- For tickers: only include real stock symbols, not abbreviations
- Return [] if the text contains no real predictions
"""


def _build_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. Add it to your .env file."
        )
    return anthropic.Anthropic(api_key=api_key)


def extract_predictions_from_text(
    text: str,
    client: anthropic.Anthropic,
    post_id: str = "",
) -> list[dict]:
    """
    Send a single text block (post + comments) to Claude and return
    a list of structured prediction dicts.
    """
    if not text.strip() or len(text) < 30:
        return []

    # Truncate very long texts to stay within token budget
    max_chars = 6000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n[...truncated]"

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",   # fast + cheap for bulk extraction
            max_tokens=1500,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": text}],
        )
        raw = response.content[0].text.strip()

        # Parse JSON safely
        # Sometimes Claude wraps the array in markdown code fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)

        predictions = json.loads(raw)
        if not isinstance(predictions, list):
            return []

        # Tag post_id for traceability
        for p in predictions:
            p["post_id"] = post_id

        return predictions

    except (json.JSONDecodeError, anthropic.APIError, anthropic.RateLimitError) as exc:
        logger.warning("Extraction failed for post %s: %s", post_id, exc)
        if isinstance(exc, anthropic.RateLimitError):
            time.sleep(30)
        return []


def batch_extract_predictions(
    posts: list[dict],
    batch_size: int = 10,
) -> list[dict]:
    """
    Run prediction extraction over all fetched posts and their comments.
    Returns a flat list of prediction dicts enriched with post metadata.
    """
    client = _build_client()
    all_predictions: list[dict] = []
    total = len(posts)

    for i, post in enumerate(posts):
        logger.info("Extracting predictions [%d/%d] post=%s", i + 1, total, post["id"])

        # Combine post title + body
        combined = f"TITLE: {post['title']}\n\nBODY: {post['selftext']}"

        # Append top-scored comments (up to 10 for context)
        top_comments = sorted(post.get("comments", []), key=lambda c: c["score"], reverse=True)[:10]
        if top_comments:
            combined += "\n\nTOP COMMENTS:\n" + "\n---\n".join(
                c["body"] for c in top_comments
            )

        predictions = extract_predictions_from_text(combined, client, post_id=post["id"])

        # Enrich each prediction with post metadata
        for pred in predictions:
            pred.update(
                {
                    "post_id": post["id"],
                    "post_title": post["title"],
                    "post_score": post["score"],
                    "post_created_utc": post["created_utc"],
                    "post_created_dt": post["created_dt"],
                    "post_url": post["url"],
                    "post_flair": post["flair"],
                }
            )
        all_predictions.extend(predictions)

        # Light throttle to stay within Claude rate limits
        if (i + 1) % batch_size == 0:
            time.sleep(2)

    logger.info("Extracted %d predictions from %d posts.", len(all_predictions), total)
    return all_predictions


def deduplicate_predictions(predictions: list[dict]) -> list[dict]:
    """
    Remove near-duplicate predictions (same direction + same ticker(s) + same topic
    posted within a short time window) to avoid double-counting.
    """
    seen: set[str] = set()
    unique: list[dict] = []
    for pred in predictions:
        key = (
            pred.get("direction", ""),
            tuple(sorted(pred.get("tickers", []))),
            pred.get("topic", ""),
            pred.get("asset_class", ""),
        )
        if key not in seen:
            seen.add(key)
            unique.append(pred)
    return unique
