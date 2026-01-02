"use client";
import { useState, useEffect } from 'react';
import WalletSummary from '../components/WalletSummary';
import PositionsTable from '../components/PositionsTable';

// Default wallet from requirements
const DEFAULT_WALLET = "0x5b5d51203a0f9079f8aeb098a6523a13f298c060";
const API_BASE = "http://localhost:8000/api";

export default function Home() {
  const [address, setAddress] = useState(DEFAULT_WALLET);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [monitoring, setMonitoring] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/wallet/${address}`);
      const json = await res.json();
      setData(json.state);
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      setLoading(false);
    }
  };

  const toggleMonitor = async () => {
      if (monitoring) {
          await fetch(`${API_BASE}/stop/${address}`, { method: 'POST' });
          setMonitoring(false);
      } else {
          await fetch(`${API_BASE}/monitor/${address}`, { method: 'POST' });
          setMonitoring(true);
      }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, [address]);

  // Calculate total PnL from positions if not provided in summary (or use marginSummary)
  // The API returns assetPositions which has unrealizedPnl for each.
  // We can sum them up or check if crossMarginSummary has it.
  // Based on curl output: marginSummary doesn't have total Unrealized PnL directly, but assetPositions do.

  const totalPnl = data?.assetPositions?.reduce((acc: number, pos: any) => acc + parseFloat(pos.position.unrealizedPnl), 0).toString() || "0";

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8 font-sans">
      <header className="mb-8 flex flex-col md:flex-row justify-between items-center">
        <div>
            <h1 className="text-3xl font-bold text-blue-400">HyperTracker Clone</h1>
            <p className="text-gray-400 mt-2">Mirror Trading & Wallet Watcher</p>
        </div>
        <div className="mt-4 md:mt-0 flex gap-2">
            <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                className="bg-gray-800 border border-gray-700 rounded px-4 py-2 w-64 md:w-96 focus:outline-none focus:border-blue-500"
                placeholder="Enter Wallet Address"
            />
             <button
                onClick={fetchData}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition"
            >
                Refresh
            </button>
            <button
                onClick={toggleMonitor}
                className={`${monitoring ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'} text-white font-bold py-2 px-4 rounded transition`}
            >
                {monitoring ? "Stop Monitor" : "Start Monitor"}
            </button>
        </div>
      </header>

      {loading && !data && <p className="text-center text-gray-500">Loading wallet data...</p>}

      {data && (
        <main>
          <WalletSummary
            accountValue={data.marginSummary.accountValue}
            totalPnl={totalPnl}
            marginUsed={data.marginSummary.totalMarginUsed}
          />

          <PositionsTable positions={data.assetPositions.map((p: any) => p.position)} />

          <div className="mt-8 text-xs text-gray-500 text-center">
            Data provided by Hyperliquid Info API. Replicating CoinMarketMan experience.
          </div>
        </main>
      )}
    </div>
  );
}
