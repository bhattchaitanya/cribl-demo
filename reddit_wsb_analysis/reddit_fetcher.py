"""
Reddit Fetcher — pulls posts and comments from r/wallstreetbets
using the PRAW library with official Reddit API credentials.
"""

import os
import time
import logging
from datetime import datetime, timezone, timedelta
from typing import Generator

import praw
from praw.models import MoreComments

logger = logging.getLogger(__name__)


def build_reddit_client() -> praw.Reddit:
    """Initialise a read-only Reddit client from environment variables."""
    client_id = os.environ.get("REDDIT_CLIENT_ID", "")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")
    user_agent = os.environ.get(
        "REDDIT_USER_AGENT", "WSBPredictionAnalyzer/1.0"
    )

    if not client_id or not client_secret:
        raise EnvironmentError(
            "REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET must be set.\n"
            "Copy .env.example to .env and fill in your Reddit app credentials.\n"
            "Create a free app at https://www.reddit.com/prefs/apps"
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        ratelimit_seconds=1,
    )


# ── Prediction-rich search queries ──────────────────────────────────────────
SEARCH_QUERIES = [
    "will moon",
    "will crash",
    "prediction 2026",
    "bull case bear case",
    "war stocks",
    "AI stocks prediction",
    "nvidia prediction",
    "China Taiwan war",
    "Russia Ukraine stocks",
    "interest rate prediction",
    "inflation prediction",
    "recession prediction",
    "market crash",
    "SPY calls puts prediction",
    "tech stocks 2026",
    "defense stocks war",
    "AI bubble",
    "Fed prediction",
]

# Topics we care about
TOPIC_KEYWORDS = {
    "war":         ["war", "ukraine", "russia", "china", "taiwan", "defense",
                    "military", "conflict", "nato", "invasion", "missile"],
    "ai":          ["ai", "artificial intelligence", "nvidia", "nvda", "openai",
                    "chatgpt", "llm", "gpu", "machine learning", "deepseek",
                    "grok", "gemini", "anthropic"],
    "fed_rates":   ["fed", "federal reserve", "interest rate", "rate cut",
                    "rate hike", "fomc", "powell", "inflation", "cpi", "pce"],
    "tech":        ["tech", "nasdaq", "qqq", "apple", "aapl", "microsoft",
                    "msft", "google", "googl", "meta", "amazon", "amzn"],
    "energy":      ["oil", "energy", "crude", "opec", "natural gas", "solar",
                    "xom", "chevron"],
    "crypto":      ["bitcoin", "btc", "ethereum", "eth", "crypto", "doge",
                    "solana", "coinbase", "coin"],
    "market":      ["spy", "s&p", "s&p500", "dow", "nasdaq", "market crash",
                    "bull run", "bear market", "correction", "recession"],
}


def _within_window(post, cutoff_ts: float) -> bool:
    return post.created_utc >= cutoff_ts


def fetch_wsb_posts(
    lookback_days: int = 90,
    max_posts: int = 500,
    max_comments_per_post: int = 200,
) -> list[dict]:
    """
    Return a list of dicts, each representing a post + its top comments.
    Fetches posts from the past `lookback_days` days.
    """
    reddit = build_reddit_client()
    subreddit = reddit.subreddit("wallstreetbets")
    cutoff = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).timestamp()

    posts_data: list[dict] = []
    seen_ids: set[str] = set()

    def _collect_post(post) -> dict | None:
        if post.id in seen_ids:
            return None
        if not _within_window(post, cutoff):
            return None

        seen_ids.add(post.id)
        created_dt = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)

        # Gather top comments
        try:
            post.comments.replace_more(limit=0)
            comments = [
                {
                    "id": c.id,
                    "body": c.body,
                    "score": c.score,
                    "created_utc": c.created_utc,
                }
                for c in post.comments.list()[:max_comments_per_post]
                if not isinstance(c, MoreComments) and len(c.body) > 20
            ]
        except Exception as exc:
            logger.warning("Could not fetch comments for %s: %s", post.id, exc)
            comments = []

        return {
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext or "",
            "score": post.score,
            "upvote_ratio": post.upvote_ratio,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "created_dt": created_dt.isoformat(),
            "url": f"https://reddit.com{post.permalink}",
            "flair": post.link_flair_text or "",
            "comments": comments,
        }

    # 1. Hot and top posts for broad coverage
    logger.info("Fetching hot posts from r/wallstreetbets…")
    for post in _rate_limited(subreddit.hot(limit=max_posts)):
        rec = _collect_post(post)
        if rec:
            posts_data.append(rec)

    logger.info("Fetching top posts (month) from r/wallstreetbets…")
    for post in _rate_limited(subreddit.top(time_filter="month", limit=min(max_posts, 250))):
        rec = _collect_post(post)
        if rec:
            posts_data.append(rec)

    logger.info("Fetching top posts (3 months) from r/wallstreetbets…")
    for post in _rate_limited(subreddit.top(time_filter="year", limit=min(max_posts, 250))):
        if not _within_window(post, cutoff):
            continue
        rec = _collect_post(post)
        if rec:
            posts_data.append(rec)

    # 2. Targeted searches for prediction-heavy content
    logger.info("Running targeted searches…")
    for query in SEARCH_QUERIES:
        try:
            for post in subreddit.search(
                query, sort="top", time_filter="month", limit=50
            ):
                rec = _collect_post(post)
                if rec:
                    posts_data.append(rec)
            time.sleep(0.5)   # gentle rate-limit
        except Exception as exc:
            logger.warning("Search '%s' failed: %s", query, exc)

    logger.info("Fetched %d unique posts total.", len(posts_data))
    return posts_data


def _rate_limited(generator: Generator, delay: float = 0.1):
    """Yield items from a generator with a small delay between each."""
    for item in generator:
        yield item
        time.sleep(delay)


def tag_topics(text: str) -> list[str]:
    """Return which topics appear in the text (case-insensitive)."""
    text_lower = text.lower()
    return [
        topic
        for topic, keywords in TOPIC_KEYWORDS.items()
        if any(kw in text_lower for kw in keywords)
    ]
