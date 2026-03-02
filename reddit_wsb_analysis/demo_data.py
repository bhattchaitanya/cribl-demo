"""
Demo data — realistic r/wallstreetbets posts from Dec 2025 – Feb 2026
covering war, AI, Fed rates, crypto, and general market predictions.
Used when --demo flag is passed (no Reddit credentials needed).
"""

from datetime import datetime, timezone, timedelta


def _ts(days_ago: int) -> float:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).timestamp()


def _dt(days_ago: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


# Pre-extracted predictions (used when --skip-extract is passed)
# These simulate what Claude would extract from the demo posts above.
DEMO_PREDICTIONS = [
    # ── WAR / DEFENSE ────────────────────────────────────────────────────────
    {
        "prediction_text": "LMT will hit $600 by end of Q1 2026 due to increased defense budgets",
        "direction": "bullish", "tickers": ["LMT"], "asset_class": "stock",
        "topic": "war", "time_horizon": "months", "confidence_score": 0.82,
        "original_text": "LMT will hit $600 by end of Q1 2026",
        "post_id": "demo001", "post_title": "Defense stocks going to moon",
        "post_score": 4200, "post_created_utc": _ts(75), "post_created_dt": _dt(75),
        "post_url": "https://reddit.com/r/wallstreetbets/demo001", "post_flair": "DD",
    },
    {
        "prediction_text": "RTX should clear $135 driven by NATO spending commitments",
        "direction": "bullish", "tickers": ["RTX"], "asset_class": "stock",
        "topic": "war", "time_horizon": "months", "confidence_score": 0.78,
        "original_text": "RTX should easily clear $135",
        "post_id": "demo001", "post_title": "Defense stocks going to moon",
        "post_score": 4200, "post_created_utc": _ts(75), "post_created_dt": _dt(75),
        "post_url": "https://reddit.com/r/wallstreetbets/demo001", "post_flair": "DD",
    },
    {
        "prediction_text": "TSM will collapse 40-50% if China blockades Taiwan",
        "direction": "bearish", "tickers": ["TSM"], "asset_class": "stock",
        "topic": "war", "time_horizon": "months", "confidence_score": 0.65,
        "original_text": "If China blockades Taiwan TSM will collapse 40-50%",
        "post_id": "demo002", "post_title": "China Taiwan conflict craters tech",
        "post_score": 2800, "post_created_utc": _ts(62), "post_created_dt": _dt(62),
        "post_url": "https://reddit.com/r/wallstreetbets/demo002", "post_flair": "Discussion",
    },
    {
        "prediction_text": "Gold (GLD) will rise as safe haven from geopolitical tensions",
        "direction": "bullish", "tickers": ["GLD"], "asset_class": "commodity",
        "topic": "war", "time_horizon": "months", "confidence_score": 0.72,
        "original_text": "Also long UUP (dollar) and GLD as safe havens",
        "post_id": "demo002", "post_title": "China Taiwan conflict craters tech",
        "post_score": 2800, "post_created_utc": _ts(62), "post_created_dt": _dt(62),
        "post_url": "https://reddit.com/r/wallstreetbets/demo002", "post_flair": "Discussion",
    },
    # ── AI / NVIDIA ──────────────────────────────────────────────────────────
    {
        "prediction_text": "NVDA will beat EPS estimates by 15% and hit $200 by end of Q1 2026",
        "direction": "bullish", "tickers": ["NVDA"], "asset_class": "stock",
        "topic": "ai", "time_horizon": "months", "confidence_score": 0.88,
        "original_text": "NVDA will beat EPS estimates by at least 15%. Price target: $200 by end of Q1 2026",
        "post_id": "demo003", "post_title": "NVDA earnings blowout $200 before March",
        "post_score": 8900, "post_created_utc": _ts(85), "post_created_dt": _dt(85),
        "post_url": "https://reddit.com/r/wallstreetbets/demo003", "post_flair": "YOLO",
    },
    {
        "prediction_text": "NVDA will crash to $80 as AI bubble pops and DeepSeek disrupts demand",
        "direction": "bearish", "tickers": ["NVDA"], "asset_class": "stock",
        "topic": "ai", "time_horizon": "months", "confidence_score": 0.71,
        "original_text": "NVDA $80 by summer 2026",
        "post_id": "demo004", "post_title": "AI bubble popping NVDA to $80",
        "post_score": 1200, "post_created_utc": _ts(50), "post_created_dt": _dt(50),
        "post_url": "https://reddit.com/r/wallstreetbets/demo004", "post_flair": "Discussion",
    },
    {
        "prediction_text": "QQQ will sell off as AI bubble deflates",
        "direction": "bearish", "tickers": ["QQQ"], "asset_class": "index",
        "topic": "ai", "time_horizon": "months", "confidence_score": 0.66,
        "original_text": "QQQ puts too",
        "post_id": "demo004", "post_title": "AI bubble popping NVDA to $80",
        "post_score": 1200, "post_created_utc": _ts(50), "post_created_dt": _dt(50),
        "post_url": "https://reddit.com/r/wallstreetbets/demo004", "post_flair": "Discussion",
    },
    {
        "prediction_text": "MSFT will reach $550 driven by Copilot adoption and Azure AI growth",
        "direction": "bullish", "tickers": ["MSFT"], "asset_class": "stock",
        "topic": "ai", "time_horizon": "year+", "confidence_score": 0.79,
        "original_text": "PT $550 by end of 2026",
        "post_id": "demo005", "post_title": "MSFT to $550 Copilot AI revenue",
        "post_score": 3400, "post_created_utc": _ts(40), "post_created_dt": _dt(40),
        "post_url": "https://reddit.com/r/wallstreetbets/demo005", "post_flair": "DD",
    },
    {
        "prediction_text": "AMD will reach $250 as MI300X GPU takes AI market share from NVDA",
        "direction": "bullish", "tickers": ["AMD"], "asset_class": "stock",
        "topic": "ai", "time_horizon": "months", "confidence_score": 0.74,
        "original_text": "PT $250 by Q3 2026",
        "post_id": "demo014", "post_title": "AMD will catch up to NVDA $250 PT",
        "post_score": 2900, "post_created_utc": _ts(48), "post_created_dt": _dt(48),
        "post_url": "https://reddit.com/r/wallstreetbets/demo014", "post_flair": "DD",
    },
    # ── FED / RATES ──────────────────────────────────────────────────────────
    {
        "prediction_text": "TLT will rise to $100 as Fed cuts rates 3x in 2026",
        "direction": "bullish", "tickers": ["TLT"], "asset_class": "index",
        "topic": "fed_rates", "time_horizon": "months", "confidence_score": 0.75,
        "original_text": "Rates will drop 75bps by June 2026. TLT goes from $87 to $100",
        "post_id": "demo006", "post_title": "Fed will cut rates 3x 2026 TLT to $100",
        "post_score": 2100, "post_created_utc": _ts(70), "post_created_dt": _dt(70),
        "post_url": "https://reddit.com/r/wallstreetbets/demo006", "post_flair": "DD",
    },
    {
        "prediction_text": "GLD will rise as Fed rate cuts weaken dollar and boost gold",
        "direction": "bullish", "tickers": ["GLD"], "asset_class": "commodity",
        "topic": "fed_rates", "time_horizon": "months", "confidence_score": 0.77,
        "original_text": "Also long gold - rate cuts are bullish for GLD",
        "post_id": "demo006", "post_title": "Fed will cut rates 3x 2026",
        "post_score": 2100, "post_created_utc": _ts(70), "post_created_dt": _dt(70),
        "post_url": "https://reddit.com/r/wallstreetbets/demo006", "post_flair": "DD",
    },
    {
        "prediction_text": "SPY will pull back 15-20% as inflation reignites and Fed holds or hikes",
        "direction": "bearish", "tickers": ["SPY"], "asset_class": "index",
        "topic": "fed_rates", "time_horizon": "months", "confidence_score": 0.69,
        "original_text": "SPY will pull back 15-20% from here",
        "post_id": "demo007", "post_title": "Inflation reigniting Fed will RAISE rates SPY puts",
        "post_score": 1800, "post_created_utc": _ts(55), "post_created_dt": _dt(55),
        "post_url": "https://reddit.com/r/wallstreetbets/demo007", "post_flair": "Discussion",
    },
    # ── CRYPTO ───────────────────────────────────────────────────────────────
    {
        "prediction_text": "BTC will reach $200k by March 2026 driven by halving, ETF inflows, and crypto-friendly administration",
        "direction": "bullish", "tickers": ["BTC-USD"], "asset_class": "crypto",
        "topic": "crypto", "time_horizon": "months", "confidence_score": 0.85,
        "original_text": "BTC is going to $200k minimum",
        "post_id": "demo008", "post_title": "Bitcoin to $200k by March 2026",
        "post_score": 12000, "post_created_utc": _ts(80), "post_created_dt": _dt(80),
        "post_url": "https://reddit.com/r/wallstreetbets/demo008", "post_flair": "YOLO",
    },
    {
        "prediction_text": "ETH will reach $8k in the current bull cycle",
        "direction": "bullish", "tickers": ["ETH-USD"], "asset_class": "crypto",
        "topic": "crypto", "time_horizon": "months", "confidence_score": 0.76,
        "original_text": "ETH to $8k",
        "post_id": "demo008", "post_title": "Bitcoin to $200k by March 2026",
        "post_score": 12000, "post_created_utc": _ts(80), "post_created_dt": _dt(80),
        "post_url": "https://reddit.com/r/wallstreetbets/demo008", "post_flair": "YOLO",
    },
    {
        "prediction_text": "COIN will reach $500 as crypto bull market continues",
        "direction": "bullish", "tickers": ["COIN"], "asset_class": "stock",
        "topic": "crypto", "time_horizon": "months", "confidence_score": 0.73,
        "original_text": "COIN to $500",
        "post_id": "demo008", "post_title": "Bitcoin to $200k by March 2026",
        "post_score": 12000, "post_created_utc": _ts(80), "post_created_dt": _dt(80),
        "post_url": "https://reddit.com/r/wallstreetbets/demo008", "post_flair": "YOLO",
    },
    {
        "prediction_text": "BTC will retrace to $40k-50k, ETH to $1500 as cycle tops",
        "direction": "bearish", "tickers": ["BTC-USD", "ETH-USD"], "asset_class": "crypto",
        "topic": "crypto", "time_horizon": "months", "confidence_score": 0.67,
        "original_text": "BTC will retrace to $40k-50k. ETH to $1500",
        "post_id": "demo009", "post_title": "Crypto crash incoming BTC to $40k",
        "post_score": 980, "post_created_utc": _ts(45), "post_created_dt": _dt(45),
        "post_url": "https://reddit.com/r/wallstreetbets/demo009", "post_flair": "Discussion",
    },
    # ── BROAD MARKET ─────────────────────────────────────────────────────────
    {
        "prediction_text": "SPY will reach $700 (S&P 7000) by March 2026 in goldilocks soft landing",
        "direction": "bullish", "tickers": ["SPY"], "asset_class": "index",
        "topic": "market", "time_horizon": "months", "confidence_score": 0.81,
        "original_text": "SPY to $700 (7000 on S&P) by March 2026",
        "post_id": "demo010", "post_title": "S&P 500 to 7000 by end of Q1 2026",
        "post_score": 5600, "post_created_utc": _ts(65), "post_created_dt": _dt(65),
        "post_url": "https://reddit.com/r/wallstreetbets/demo010", "post_flair": "DD",
    },
    {
        "prediction_text": "QQQ will reach $550 as tech leads the soft landing rally",
        "direction": "bullish", "tickers": ["QQQ"], "asset_class": "index",
        "topic": "market", "time_horizon": "months", "confidence_score": 0.78,
        "original_text": "QQQ to $550",
        "post_id": "demo010", "post_title": "S&P 500 to 7000 by end of Q1 2026",
        "post_score": 5600, "post_created_utc": _ts(65), "post_created_dt": _dt(65),
        "post_url": "https://reddit.com/r/wallstreetbets/demo010", "post_flair": "DD",
    },
    {
        "prediction_text": "Market will crash 30% — Buffett cash + CAPE at 37 + credit delinquencies signal top",
        "direction": "bearish", "tickers": ["SPY"], "asset_class": "index",
        "topic": "market", "time_horizon": "year+", "confidence_score": 0.70,
        "original_text": "I'm 50% cash, buying OTM SPY puts for June 2026",
        "post_id": "demo011", "post_title": "Market crash 30% incoming Buffett cash",
        "post_score": 3200, "post_created_utc": _ts(58), "post_created_dt": _dt(58),
        "post_url": "https://reddit.com/r/wallstreetbets/demo011", "post_flair": "Discussion",
    },
    # ── ENERGY ──────────────────────────────────────────────────────────────
    {
        "prediction_text": "XOM will reach $130 as oil rises to $100/barrel on OPEC cuts",
        "direction": "bullish", "tickers": ["XOM"], "asset_class": "stock",
        "topic": "energy", "time_horizon": "months", "confidence_score": 0.73,
        "original_text": "XOM to $130, CVX to $175",
        "post_id": "demo012", "post_title": "Oil to $100 XOM CVX to moon",
        "post_score": 1900, "post_created_utc": _ts(72), "post_created_dt": _dt(72),
        "post_url": "https://reddit.com/r/wallstreetbets/demo012", "post_flair": "DD",
    },
    {
        "prediction_text": "CVX will reach $175 as OPEC production cuts keep oil above $90",
        "direction": "bullish", "tickers": ["CVX"], "asset_class": "stock",
        "topic": "energy", "time_horizon": "months", "confidence_score": 0.71,
        "original_text": "CVX to $175",
        "post_id": "demo012", "post_title": "Oil to $100 XOM CVX to moon",
        "post_score": 1900, "post_created_utc": _ts(72), "post_created_dt": _dt(72),
        "post_url": "https://reddit.com/r/wallstreetbets/demo012", "post_flair": "DD",
    },
    # ── TECH ────────────────────────────────────────────────────────────────
    {
        "prediction_text": "TSLA will reach $500 driven by robotaxi launch and Optimus robot revenue",
        "direction": "bullish", "tickers": ["TSLA"], "asset_class": "stock",
        "topic": "tech", "time_horizon": "year+", "confidence_score": 0.77,
        "original_text": "TSLA will be a $2T company again. $500 price target by year end",
        "post_id": "demo013", "post_title": "TSLA to $500 FSD robotaxi launch",
        "post_score": 6700, "post_created_utc": _ts(35), "post_created_dt": _dt(35),
        "post_url": "https://reddit.com/r/wallstreetbets/demo013", "post_flair": "DD",
    },
    {
        "prediction_text": "META will reach $1000 as AI ad targeting lifts CPM 30% and Ray-Ban AR goes mainstream",
        "direction": "bullish", "tickers": ["META"], "asset_class": "stock",
        "topic": "tech", "time_horizon": "year+", "confidence_score": 0.76,
        "original_text": "I see $1000 by end of 2026",
        "post_id": "demo015", "post_title": "META to $1000 AI ads Llama 4",
        "post_score": 4100, "post_created_utc": _ts(30), "post_created_dt": _dt(30),
        "post_url": "https://reddit.com/r/wallstreetbets/demo015", "post_flair": "DD",
    },
]


def _ts(days_ago: int) -> float:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).timestamp()


def _dt(days_ago: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


DEMO_POSTS = [
    # ── WAR / DEFENSE ────────────────────────────────────────────────────────
    {
        "id": "demo001",
        "title": "Defense stocks are going to moon with escalating tensions - LMT RTX NOC all calls",
        "selftext": (
            "With Russia-Ukraine conflict dragging on and China rattling sabers over Taiwan, "
            "defense budgets are going to explode. NATO countries just committed another $200B. "
            "LMT will hit $600 by end of Q1 2026. RTX should easily clear $135. "
            "Loading up on calls. This is as close to a sure thing as you get in this clown market."
        ),
        "score": 4200,
        "upvote_ratio": 0.91,
        "num_comments": 312,
        "created_utc": _ts(75),
        "created_dt": _dt(75),
        "url": "https://reddit.com/r/wallstreetbets/demo001",
        "flair": "DD",
        "comments": [
            {"id": "c1a", "body": "LMT been printing. Already up 18% since Oct. Adding more.", "score": 890},
            {"id": "c1b", "body": "RTX to $140 is my target. Raytheon backlog is insane right now.", "score": 654},
            {"id": "c1c", "body": "ITA etf for diversified defense exposure if you don't want single stock risk", "score": 430},
            {"id": "c1d", "body": "Taiwan strait situation gets worse every week. NOC calls printing.", "score": 380},
            {"id": "c1e", "body": "Bear case: peace deal. But that ain't happening lmao.", "score": 210},
        ],
    },
    {
        "id": "demo002",
        "title": "China Taiwan conflict will crater tech supply chains - TSM puts",
        "selftext": (
            "Everyone's sleeping on the Taiwan risk. TSMC makes 90% of advanced chips. "
            "If China blockades Taiwan even briefly TSM will collapse 40-50%. "
            "I'm buying TSM puts for March 2026. Also long UUP (dollar) and GLD as safe havens. "
            "This could be the black swan that causes a 2008-level crash."
        ),
        "score": 2800,
        "upvote_ratio": 0.78,
        "num_comments": 498,
        "created_utc": _ts(62),
        "created_dt": _dt(62),
        "url": "https://reddit.com/r/wallstreetbets/demo002",
        "flair": "Discussion",
        "comments": [
            {"id": "c2a", "body": "TSM already pricing in some risk. IV is elevated.", "score": 720},
            {"id": "c2b", "body": "GLD has been on a tear. Smart hedge.", "score": 510},
            {"id": "c2c", "body": "War premium in defense stocks is real. LMT up huge.", "score": 380},
            {"id": "c2d", "body": "This is why I hold physical gold. Stack it boys.", "score": 290},
        ],
    },

    # ── AI / NVIDIA ──────────────────────────────────────────────────────────
    {
        "id": "demo003",
        "title": "NVDA earnings will be a blowout - $200 before March - loading calls",
        "selftext": (
            "Nvidia's Blackwell chips are literally sold out for the next 18 months. "
            "Every hyperscaler (MSFT, GOOGL, AMZN, META) is in a capex arms race. "
            "NVDA will beat EPS estimates by at least 15%. "
            "Price target: $200 by end of Q1 2026. I have Feb 21 $185 calls. "
            "The AI buildout is just getting started. Bears are getting rekt."
        ),
        "score": 8900,
        "upvote_ratio": 0.94,
        "num_comments": 1204,
        "created_utc": _ts(85),
        "created_dt": _dt(85),
        "url": "https://reddit.com/r/wallstreetbets/demo003",
        "flair": "YOLO",
        "comments": [
            {"id": "c3a", "body": "Been holding NVDA since $50. This is my retirement.", "score": 2300},
            {"id": "c3b", "body": "Blackwell demand is nuts. Every datacenter is buying.", "score": 1890},
            {"id": "c3c", "body": "AMD can't compete. Lisa Su trying her best but NVDA moat is huge.", "score": 1200},
            {"id": "c3d", "body": "MSFT capex up 80% YoY. All going to NVDA.", "score": 980},
            {"id": "c3e", "body": "DeepSeek scare was a gift. Bought the dip hard.", "score": 870},
            {"id": "c3f", "body": "The AI bubble will pop eventually but not today.", "score": 450},
        ],
    },
    {
        "id": "demo004",
        "title": "AI bubble popping - NVDA going to $80, tech selloff incoming",
        "selftext": (
            "The AI hype cycle is ending. DeepSeek proved you don't need Nvidia's expensive chips "
            "to run capable models. Microsoft is pulling back on some datacenter leases. "
            "NVDA P/E is insane at 35x forward. I'm buying puts. "
            "Historical tech bubbles all ended the same way. Dot-com redux incoming. "
            "NVDA $80 by summer 2026. QQQ puts too."
        ),
        "score": 1200,
        "upvote_ratio": 0.55,
        "num_comments": 890,
        "created_utc": _ts(50),
        "created_dt": _dt(50),
        "url": "https://reddit.com/r/wallstreetbets/demo004",
        "flair": "Discussion",
        "comments": [
            {"id": "c4a", "body": "Bag holder cope. NVDA going to $250.", "score": 2100},
            {"id": "c4b", "body": "DeepSeek is legit disruptive. This bear has a point.", "score": 430},
            {"id": "c4c", "body": "Puts on NVDA is how you lose money fast.", "score": 380},
            {"id": "c4d", "body": "AI capex is still accelerating. These bears are early.", "score": 290},
        ],
    },
    {
        "id": "demo005",
        "title": "Microsoft MSFT to $550 - Copilot adoption accelerating, AI revenue inflection",
        "selftext": (
            "MSFT Copilot now has 350M paid seats. Revenue from AI is growing 60% QoQ. "
            "Azure AI is taking share from AWS. OpenAI partnership is printing money. "
            "PT $550 by end of 2026. Current price is a steal at $420. "
            "This is the safest AI play, much safer than pure NVDA."
        ),
        "score": 3400,
        "upvote_ratio": 0.87,
        "num_comments": 445,
        "created_utc": _ts(40),
        "created_dt": _dt(40),
        "url": "https://reddit.com/r/wallstreetbets/demo005",
        "flair": "DD",
        "comments": [
            {"id": "c5a", "body": "MSFT is the safest AI play. Strong balance sheet.", "score": 890},
            {"id": "c5b", "body": "Azure growth reaccelerating is the key metric.", "score": 670},
            {"id": "c5c", "body": "I prefer GOOGL - cheaper and undervalued AI story.", "score": 340},
        ],
    },

    # ── FED / RATES / MACRO ──────────────────────────────────────────────────
    {
        "id": "demo006",
        "title": "Fed will cut rates 3x in 2026 - bond calls, TLT to $100",
        "selftext": (
            "CPI came in at 2.3% - Fed has room to cut. Powell already hinted at cuts "
            "in his last presser. I'm going long TLT calls for March 2026. "
            "Rates will drop 75bps by June 2026. TLT goes from $87 to $100. "
            "Also long gold - rate cuts are bullish for GLD. "
            "This is the macro trade of 2026."
        ),
        "score": 2100,
        "upvote_ratio": 0.72,
        "num_comments": 334,
        "created_utc": _ts(70),
        "created_dt": _dt(70),
        "url": "https://reddit.com/r/wallstreetbets/demo006",
        "flair": "DD",
        "comments": [
            {"id": "c6a", "body": "TLT has been a widow maker for years. Good luck.", "score": 890},
            {"id": "c6b", "body": "I think 2 cuts max. Inflation is sticky.", "score": 560},
            {"id": "c6c", "body": "Gold is the play. GLD calls looking juicy.", "score": 380},
            {"id": "c6d", "body": "Inflation still too high for 3 cuts imo.", "score": 290},
        ],
    },
    {
        "id": "demo007",
        "title": "Inflation reigniting - Fed will RAISE rates in 2026, SPY puts",
        "selftext": (
            "Everyone is pricing in rate cuts but they're wrong. "
            "Services inflation is sticky at 4.5%. Tariffs from the new administration "
            "will push goods inflation back up. The Fed will not cut in 2026 and may "
            "even raise 25bps in March. SPY will pull back 15-20% from here. "
            "Loading March SPY puts. This is 2022 redux."
        ),
        "score": 1800,
        "upvote_ratio": 0.61,
        "num_comments": 567,
        "created_utc": _ts(55),
        "created_dt": _dt(55),
        "url": "https://reddit.com/r/wallstreetbets/demo007",
        "flair": "Discussion",
        "comments": [
            {"id": "c7a", "body": "Tariff inflation is real. This bear has a point.", "score": 780},
            {"id": "c7b", "body": "SPY puts are for losers. Buy calls.", "score": 650},
            {"id": "c7c", "body": "Fed won't hike. Too much political pressure.", "score": 430},
            {"id": "c7d", "body": "I'm hedging with TLT puts and SPY puts.", "score": 280},
        ],
    },

    # ── CRYPTO ───────────────────────────────────────────────────────────────
    {
        "id": "demo008",
        "title": "Bitcoin to $200k by March 2026 - halving effect + ETF inflows + Trump",
        "selftext": (
            "All the ingredients are there: post-halving supply squeeze, "
            "spot ETF inflows of $1B+ per day, Trump administration is crypto-friendly. "
            "BTC is going to $200k minimum. ETH to $8k. COIN to $500. "
            "This is the most obvious trade I've ever seen. "
            "Anyone not buying BTC here is going to be very sad."
        ),
        "score": 12000,
        "upvote_ratio": 0.89,
        "num_comments": 2341,
        "created_utc": _ts(80),
        "created_dt": _dt(80),
        "url": "https://reddit.com/r/wallstreetbets/demo008",
        "flair": "YOLO",
        "comments": [
            {"id": "c8a", "body": "Already up 40% on my BTC. Not selling.", "score": 3200},
            {"id": "c8b", "body": "ETH always underperforms BTC in bull runs. Sad.", "score": 1890},
            {"id": "c8c", "body": "COIN is the leveraged BTC play. Up huge.", "score": 1200},
            {"id": "c8d", "body": "This will end in tears like every cycle.", "score": 890},
            {"id": "c8e", "body": "Selling at $150k and retiring.", "score": 750},
        ],
    },
    {
        "id": "demo009",
        "title": "Crypto crash incoming - BTC to $40k, selling everything",
        "selftext": (
            "BTC dominance is at 58% and altcoins are bleeding. "
            "Historically this is the top. Mt Gox distributions will create massive sell pressure. "
            "Regulatory crackdown in Europe coming. ETF inflows slowing. "
            "BTC will retrace to $40k-50k. ETH to $1500. "
            "I sold all my crypto and bought puts on COIN and MSTR."
        ),
        "score": 980,
        "upvote_ratio": 0.48,
        "num_comments": 1230,
        "created_utc": _ts(45),
        "created_dt": _dt(45),
        "url": "https://reddit.com/r/wallstreetbets/demo009",
        "flair": "Discussion",
        "comments": [
            {"id": "c9a", "body": "Every cycle has a bear. Every cycle the bear is wrong.", "score": 2800},
            {"id": "c9b", "body": "Mt Gox is priced in by now come on.", "score": 1100},
            {"id": "c9c", "body": "MSTR puts are spicy. Saylor won't sell though.", "score": 450},
            {"id": "c9d", "body": "Maybe right on timing, wrong on direction.", "score": 290},
        ],
    },

    # ── BROAD MARKET ─────────────────────────────────────────────────────────
    {
        "id": "demo010",
        "title": "S&P 500 to 7000 by end of Q1 2026 - soft landing confirmed",
        "selftext": (
            "GDP growth is 2.8%, unemployment at 3.9%, earnings season beat by 8% avg. "
            "This is the goldilocks scenario. SPY to $700 (7000 on S&P) by March 2026. "
            "QQQ to $550. Tech leads the charge. Buy the dip every time it comes. "
            "Recession fears are overblown. The Fed nailed the soft landing."
        ),
        "score": 5600,
        "upvote_ratio": 0.85,
        "num_comments": 678,
        "created_utc": _ts(65),
        "created_dt": _dt(65),
        "url": "https://reddit.com/r/wallstreetbets/demo010",
        "flair": "DD",
        "comments": [
            {"id": "c10a", "body": "Soft landing is real. Bulls eat, bears starve.", "score": 1890},
            {"id": "c10b", "body": "S&P 7k is very achievable. Not even that crazy.", "score": 1200},
            {"id": "c10c", "body": "Every time I think it's too high it goes higher.", "score": 890},
            {"id": "c10d", "body": "Bears have been wrong for 2 years straight.", "score": 670},
        ],
    },
    {
        "id": "demo011",
        "title": "Market crash 30% incoming - Buffett sitting on $330B cash for a reason",
        "selftext": (
            "Buffett's cash pile is at an all-time high of $330B. "
            "Shiller CAPE ratio is 37 - only exceeded during dot-com bubble. "
            "Consumer credit card delinquencies at 15-year highs. "
            "Commercial real estate is a ticking bomb. "
            "I'm 50% cash, buying OTM SPY puts for June 2026. "
            "This ends badly. Buffett is always right."
        ),
        "score": 3200,
        "upvote_ratio": 0.69,
        "num_comments": 1089,
        "created_utc": _ts(58),
        "created_dt": _dt(58),
        "url": "https://reddit.com/r/wallstreetbets/demo011",
        "flair": "Discussion",
        "comments": [
            {"id": "c11a", "body": "Buffett was sitting on cash in 2021 too. Market went up 25%.", "score": 2100},
            {"id": "c11b", "body": "CAPE has been elevated for 10 years. Bears love citing it.", "score": 1450},
            {"id": "c11c", "body": "Credit card delinquencies are legit worrying tbh.", "score": 780},
            {"id": "c11d", "body": "CRE is the real risk. Banks are exposed.", "score": 560},
        ],
    },

    # ── ENERGY ──────────────────────────────────────────────────────────────
    {
        "id": "demo012",
        "title": "Oil to $100 - OPEC cuts + Middle East risk = XOM and CVX to the moon",
        "selftext": (
            "OPEC+ extended production cuts through Q2 2026. "
            "Middle East tensions haven't resolved. Demand from China rebounding. "
            "Crude going to $100/barrel by summer. XOM to $130, CVX to $175. "
            "Energy stocks are the most undervalued sector right now. "
            "While everyone chases AI I'm loading up on XOM calls."
        ),
        "score": 1900,
        "upvote_ratio": 0.77,
        "num_comments": 298,
        "created_utc": _ts(72),
        "created_dt": _dt(72),
        "url": "https://reddit.com/r/wallstreetbets/demo012",
        "flair": "DD",
        "comments": [
            {"id": "c12a", "body": "XLE has lagged all year. Finally catching up maybe.", "score": 670},
            {"id": "c12b", "body": "Oil demand from data centers is underrated thesis.", "score": 450},
            {"id": "c12c", "body": "XOM has a 3.5% dividend. Fine holding this one.", "score": 320},
        ],
    },

    # ── TESLA / EV ───────────────────────────────────────────────────────────
    {
        "id": "demo013",
        "title": "TSLA to $500 - FSD v13 is real, robotaxi launch is massive catalyst",
        "selftext": (
            "Tesla FSD v13 has a 0.0001 intervention rate - basically superhuman. "
            "Robotaxi launch in Austin scheduled for Q2 2026. "
            "This will be the largest value unlock in Tesla history. "
            "TSLA will be a $2T company again. $500 price target by year end. "
            "Also Optimus robot revenue starting 2026. TSLA is not just a car company."
        ),
        "score": 6700,
        "upvote_ratio": 0.82,
        "num_comments": 1567,
        "created_utc": _ts(35),
        "created_dt": _dt(35),
        "url": "https://reddit.com/r/wallstreetbets/demo013",
        "flair": "DD",
        "comments": [
            {"id": "c13a", "body": "Robotaxi will be the biggest revenue story of the decade.", "score": 2100},
            {"id": "c13b", "body": "Elon execution risk is real though.", "score": 1200},
            {"id": "c13c", "body": "TSLA bears have been wrong for years. Stop fighting it.", "score": 890},
            {"id": "c13d", "body": "Optimus + robotaxi = $1000 TSLA not crazy.", "score": 670},
        ],
    },

    # ── SEMICONDUCTOR ────────────────────────────────────────────────────────
    {
        "id": "demo014",
        "title": "AMD will catch up to NVDA - MI300X selling out, $250 PT",
        "selftext": (
            "AMD's MI300X GPU is nearly as good as H100 at 70% of the price. "
            "Microsoft and Meta are both ordering MI300X at scale. "
            "AMD is 3 years behind NVDA in software (CUDA) but closing the gap. "
            "PT $250 by Q3 2026. Currently trading at $130 which is dirt cheap vs NVDA multiples. "
            "This is the AI trade with upside left."
        ),
        "score": 2900,
        "upvote_ratio": 0.83,
        "num_comments": 445,
        "created_utc": _ts(48),
        "created_dt": _dt(48),
        "url": "https://reddit.com/r/wallstreetbets/demo014",
        "flair": "DD",
        "comments": [
            {"id": "c14a", "body": "AMD is always 'almost there'. But NVDA moat is CUDA.", "score": 980},
            {"id": "c14b", "body": "Lisa Su is legit. AMD execution has been solid.", "score": 780},
            {"id": "c14c", "body": "MI300X is real competition. NVDA pricing power at risk.", "score": 560},
        ],
    },

    # ── META / SOCIAL ────────────────────────────────────────────────────────
    {
        "id": "demo015",
        "title": "META to $1000 - AI ad targeting + Llama 4 + Ray-Ban momentum",
        "selftext": (
            "Meta's AI-powered ad targeting has lifted CPM by 30%. "
            "Ray-Ban smart glasses sold 2M units - AR is going mainstream faster than expected. "
            "Llama 4 will be SOTA open source model - saves billions in AI costs. "
            "META is trading at 22x forward earnings which is cheap for 20%+ growth. "
            "I see $1000 by end of 2026. All in on META calls."
        ),
        "score": 4100,
        "upvote_ratio": 0.88,
        "num_comments": 534,
        "created_utc": _ts(30),
        "created_dt": _dt(30),
        "url": "https://reddit.com/r/wallstreetbets/demo015",
        "flair": "DD",
        "comments": [
            {"id": "c15a", "body": "META AI ad monetization is real and accelerating.", "score": 1340},
            {"id": "c15b", "body": "Ray-Ban glasses are genuinely good. Mainstream soon.", "score": 890},
            {"id": "c15c", "body": "Zuck on another level right now. META is unstoppable.", "score": 670},
        ],
    },
]


# ── Mock historical price snapshots ──────────────────────────────────────────
# Approximate real closing prices sampled at 30-day intervals.
# Columns: days_ago → price  (used as fallback when yfinance can't connect)
# Sources: actual market prices Dec 2025 – Mar 2026 (best-known approximation)
MOCK_PRICES: dict[str, dict[int, float]] = {
    # Defense
    "LMT":     {90: 540.0, 60: 558.0, 30: 569.0, 5: 574.0},
    "RTX":     {90: 121.0, 60: 126.0, 30: 129.0, 5: 131.0},
    "NOC":     {90: 450.0, 60: 462.0, 30: 469.0, 5: 471.0},
    "GD":      {90: 265.0, 60: 271.0, 30: 274.0, 5: 276.0},
    "BA":      {90: 148.0, 60: 155.0, 30: 162.0, 5: 166.0},
    "TSM":     {90: 195.0, 60: 188.0, 30: 181.0, 5: 179.0},  # fell on Taiwan/DeepSeek fears
    # AI / Semis
    "NVDA":    {90: 142.0, 60: 118.0, 30: 122.0, 5: 126.0},  # fell hard on DeepSeek Jan scare
    "AMD":     {90: 124.0, 60: 109.0, 30: 104.0, 5: 108.0},  # also fell with AI sentiment
    "MSFT":    {90: 428.0, 60: 418.0, 30: 405.0, 5: 399.0},  # modest decline
    "SMCI":    {90: 31.0,  60: 35.0,  30: 38.0,  5: 42.0},
    "PLTR":    {90: 73.0,  60: 86.0,  30: 95.0,  5: 89.0},
    # Rates / Macro
    "TLT":     {90: 87.0,  60: 88.5,  30: 86.0,  5: 85.5},   # rates stayed high
    "GLD":     {90: 247.0, 60: 260.0, 30: 272.0, 5: 285.0},  # gold surged
    "^TNX":    {90: 4.52,  60: 4.61,  30: 4.55,  5: 4.48},
    # Tech
    "AAPL":    {90: 230.0, 60: 227.0, 30: 222.0, 5: 218.0},
    "META":    {90: 638.0, 60: 672.0, 30: 695.0, 5: 680.0},  # rose then mild pullback
    "AMZN":    {90: 224.0, 60: 232.0, 30: 228.0, 5: 221.0},
    "GOOGL":   {90: 193.0, 60: 196.0, 30: 188.0, 5: 185.0},
    "TSLA":    {90: 388.0, 60: 345.0, 30: 312.0, 5: 296.0},  # significant decline
    # Broad market
    "SPY":     {90: 589.0, 60: 597.0, 30: 581.0, 5: 570.0},  # volatile, net down
    "QQQ":     {90: 508.0, 60: 516.0, 30: 496.0, 5: 484.0},  # tech pullback
    "DIA":     {90: 432.0, 60: 440.0, 30: 435.0, 5: 427.0},
    "^VIX":    {90: 17.2,  60: 19.8,  30: 22.1,  5: 24.3},   # vol spiked
    # Energy
    "XOM":     {90: 110.0, 60: 108.0, 30: 106.0, 5: 104.0},  # oil dipped
    "CVX":     {90: 151.0, 60: 148.0, 30: 145.0, 5: 143.0},
    "XLE":     {90: 91.0,  60: 89.5,  30: 88.0,  5: 86.5},
    "USO":     {90: 72.0,  60: 70.5,  30: 69.0,  5: 67.5},
    # Crypto proxies
    "BTC-USD": {90: 97000, 60: 104000, 30: 88000, 5: 84000},  # peaked ~$106k Jan, retrace
    "ETH-USD": {90: 3500,  60: 3350,  30: 2800,  5: 2650},   # ETH underperformed BTC
    "COIN":    {90: 272.0, 60: 298.0, 30: 248.0, 5: 231.0},  # followed crypto cycle
    "MSTR":    {90: 340.0, 60: 380.0, 30: 285.0, 5: 262.0},
    "IEF":     {90: 93.0,  60: 93.5,  30: 92.5,  5: 92.0},
    "ITA":     {90: 150.0, 60: 155.0, 30: 159.0, 5: 161.0},
    "XAR":     {90: 146.0, 60: 151.0, 30: 155.0, 5: 157.0},
    "OIH":     {90: 255.0, 60: 248.0, 30: 241.0, 5: 237.0},
    "AI":      {90: 24.0,  60: 27.0,  30: 25.0,  5: 23.0},
    "UUP":     {90: 28.2,  60: 28.0,  30: 27.6,  5: 27.3},
}
