# WSB Prediction Analyzer

Fetches the past 3 months of r/wallstreetbets posts, uses **Claude AI** to
extract forward-looking predictions (war, AI, Fed rates, crypto, etc.),
then cross-references them against real **stock market data** to measure
how accurate WSB predictions actually are.

---

## Quick Start

### 1. Install dependencies
```bash
cd reddit_wsb_analysis
pip install -r requirements.txt
```

### 2. Configure credentials
```bash
cp .env.example .env
```

Edit `.env` and fill in:

| Variable | Where to get it |
|---|---|
| `REDDIT_CLIENT_ID` | https://www.reddit.com/prefs/apps → create a "script" app |
| `REDDIT_CLIENT_SECRET` | Same app page |
| `REDDIT_USER_AGENT` | Any descriptive string, e.g. `WSBAnalyzer/1.0 by yourname` |
| `ANTHROPIC_API_KEY` | https://console.anthropic.com |

### 3. Run
```bash
python main.py
```

---

## Options

```
python main.py --help

--days N          Days to look back (default: 90)
--posts N         Max posts to fetch (default: 500)
--comments N      Max comments per post (default: 200)
--no-charts       Skip PNG chart generation
--no-save         Skip CSV/JSON output files
--load-cache PATH Load previously extracted predictions (skip Reddit/Claude)
--save-posts PATH Save raw posts to JSON for later reuse
--verbose         Debug logging
```

---

## How It Works

```
Reddit API (PRAW)
    └─ r/wallstreetbets posts + top comments (past 90 days)
           │
           ▼
Claude claude-haiku-4-5 (fast, cheap)
    └─ Extracts structured predictions:
       { direction, tickers, topic, time_horizon, confidence }
           │
           ▼
yfinance
    └─ Downloads historical prices for each ticker/topic proxy
    └─ Measures % change over predicted time horizon
           │
           ▼
Accuracy Scorer
    └─ bullish + price rose  ≥ 3%  → CORRECT
    └─ bullish + price rose  0–3%  → PARTIAL
    └─ bullish + price fell       → INCORRECT
    └─ (mirror logic for bearish)
           │
           ▼
Rich terminal report + PNG charts + CSV export
```

---

## Output

- **Terminal**: Colour-coded tables showing overall accuracy, accuracy by topic
  (war / AI / Fed rates / crypto / etc.), and the most/least accurate predictions.
- **`wsb_analysis_output/`**:
  - `predictions_<ts>.csv` — full prediction dataset with outcomes
  - `stats_<ts>.json` — aggregated statistics
  - `outcome_pie.png` — correct / partial / incorrect / inconclusive breakdown
  - `accuracy_by_topic.png` — bar chart by topic
  - `price_change_distribution.png` — histogram of price moves

---

## Topics Tracked

| Topic | What it covers |
|---|---|
| `war` | Ukraine/Russia, China/Taiwan, defense stocks (LMT, RTX, NOC…) |
| `ai` | NVDA, MSFT, GOOGL, AMD, AI ETFs, LLM companies |
| `fed_rates` | Fed decisions, CPI/PCE, bond ETFs (TLT), gold |
| `tech` | QQQ, AAPL, AMZN, META, TSLA |
| `energy` | Oil, XOM, CVX, USO |
| `crypto` | BTC, ETH, COIN, MSTR |
| `market` | SPY, VIX, broad market calls/crashes |
