# SIGNAL DESK — Multi-Agent Autonomous Financial Intelligence

Hackverse 2026 | PS-01 | VIT Chennai

## What it does
Signal Desk converts market signals, document evidence and investor risk profiles into an explainable recommendation. It demonstrates:
- 3 parallel specialist agents: Momentum, Volume, Sentiment
- RAG-style document retrieval with visible source attribution
- Personalized synthesis for Conservative / Balanced / Aggressive profiles
- Full reasoning trace and confidence scoring
- Portfolio/watchlist dashboard
- Graceful degraded-data fallback
- Session performance metrics

## Quick start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL (usually http://localhost:5173).

## Demo flow for judges
1. Select a stock.
2. Switch between Conservative and Aggressive profiles.
3. Click **Run AI Analysis**.
4. Open the reasoning trace.
5. Turn on **Simulate data outage** and rerun to show graceful fallback.
6. Compare recommendation and confidence across profiles.

> Demo data is synthetic/illustrative and not financial advice.
