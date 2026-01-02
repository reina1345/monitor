# HyperTracker Clone

A mirror trading support tool and wallet tracker for Hyperliquid, inspired by CoinMarketMan's HyperTracker.

## Features

- **Real-time Dashboard**: Monitor account value, margin usage, and open positions.
- **Position Tracking**: View detailed metrics for each position (Size, Entry Price, PnL, Leverage).
- **Discord Notifications**: Background monitoring system that alerts you on:
  - New positions opened.
  - Positions closed.
  - Position size increased or decreased.
- **HIP-3 Support**: Automatically displays any asset returned by the Hyperliquid API, including new HIP-3 assets.

## Project Structure

- `backend/`: Python FastAPI application for data fetching and monitoring.
- `frontend/`: Next.js application for the user interface.

## Prerequisites

- Python 3.9+
- Node.js 18+
- A Discord Webhook URL (for notifications)

## Setup & Running

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file for Discord Webhook (Optional)
echo "DISCORD_WEBHOOK_URL=your_webhook_url_here" > .env

# Run the server
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Usage

1. Open `http://localhost:3000`.
2. The default wallet is pre-filled. You can change it to track any Hyperliquid address.
3. Click **Refresh** to update data manually (it also auto-refreshes every 10 seconds).
4. Click **Start Monitor** to enable background tracking. If the wallet makes a trade, the backend will detect the change and send a Discord notification (if configured).

## Tech Stack

- **Frontend**: Next.js, Tailwind CSS, TypeScript
- **Backend**: Python, FastAPI, Requests
- **API**: Hyperliquid Info API (`clearinghouseState`)
