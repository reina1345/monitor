interface WalletSummaryProps {
  accountValue: string;
  totalPnl: string;
  marginUsed: string;
}

export default function WalletSummary({ accountValue, totalPnl, marginUsed }: WalletSummaryProps) {
  // Simple formatter
  const formatMoney = (val: string) => {
    const num = parseFloat(val);
    return isNaN(num) ? "$0.00" : `$${num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  const pnlNum = parseFloat(totalPnl);
  const pnlColor = pnlNum >= 0 ? "text-green-500" : "text-red-500";

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div className="bg-gray-800 p-4 rounded-lg shadow-md">
        <h3 className="text-gray-400 text-sm">口座残高 (Account Value)</h3>
        <p className="text-2xl font-bold text-white">{formatMoney(accountValue)}</p>
      </div>
      <div className="bg-gray-800 p-4 rounded-lg shadow-md">
        <h3 className="text-gray-400 text-sm">含み損益 (Total PnL)</h3>
        <p className={`text-2xl font-bold ${pnlColor}`}>{formatMoney(totalPnl)}</p>
      </div>
      <div className="bg-gray-800 p-4 rounded-lg shadow-md">
        <h3 className="text-gray-400 text-sm">使用証拠金 (Margin Used)</h3>
        <p className="text-2xl font-bold text-white">{formatMoney(marginUsed)}</p>
      </div>
    </div>
  );
}
