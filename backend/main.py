from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from client import HyperliquidClient
from monitor import WalletMonitor
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = HyperliquidClient()
active_monitors = {} # address -> Monitor instance

@app.get("/api/wallet/{address}")
def get_wallet(address: str):
    state = client.get_user_state(address)
    # Also get history if possible
    # history = client.get_user_fills(address)
    return {"state": state}

@app.post("/api/monitor/{address}")
async def start_monitor(address: str, background_tasks: BackgroundTasks):
    if address in active_monitors:
        return {"status": "already monitoring", "address": address}

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "")
    monitor = WalletMonitor(address, webhook_url)
    active_monitors[address] = monitor

    # Run in background
    background_tasks.add_task(monitor.start)

    return {"status": "started", "address": address}

@app.post("/api/stop/{address}")
def stop_monitor(address: str):
    if address in active_monitors:
        active_monitors[address].stop()
        del active_monitors[address]
        return {"status": "stopped", "address": address}
    return {"status": "not found", "address": address}

@app.get("/")
def read_root():
    return {"message": "HyperTracker Clone API"}
