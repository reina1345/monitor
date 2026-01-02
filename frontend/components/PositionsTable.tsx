interface Position {
  coin: string;
  szi: string;
  entryPx: string;
  positionValue: string;
  unrealizedPnl: string;
  leverage: { type: string; value: number };
}

interface PositionsTableProps {
  positions: Position[];
}

export default function PositionsTable({ positions }: PositionsTableProps) {
  const formatMoney = (val: string) => {
    const num = parseFloat(val);
    return isNaN(num) ? "$0.00" : `$${num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 })}`;
  };

  const formatSize = (val: string) => {
      const num = parseFloat(val);
      return isNaN(num) ? "0" : num.toLocaleString();
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <div className="p-4 border-b border-gray-700">
            <h3 className="text-xl font-bold text-white">保有ポジション一覧</h3>
        </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-gray-300">
          <thead className="bg-gray-700 text-xs uppercase text-gray-400">
            <tr>
              <th className="px-6 py-3">通貨</th>
              <th className="px-6 py-3">売買</th>
              <th className="px-6 py-3">サイズ</th>
              <th className="px-6 py-3">取得単価</th>
              <th className="px-6 py-3">評価額</th>
              <th className="px-6 py-3">損益</th>
              <th className="px-6 py-3">レバレッジ</th>
            </tr>
          </thead>
          <tbody>
            {positions.length === 0 ? (
                <tr>
                    <td colSpan={7} className="px-6 py-4 text-center">保有ポジションはありません</td>
                </tr>
            ) : positions.map((pos) => {
              const size = parseFloat(pos.szi);
              const side = size > 0 ? "LONG" : "SHORT";
              const sideColor = size > 0 ? "text-green-500" : "text-red-500";
              const pnl = parseFloat(pos.unrealizedPnl);
              const pnlColor = pnl >= 0 ? "text-green-500" : "text-red-500";

              return (
                <tr key={pos.coin} className="border-b border-gray-700 hover:bg-gray-750">
                  <td className="px-6 py-4 font-medium text-white">{pos.coin}</td>
                  <td className={`px-6 py-4 font-bold ${sideColor}`}>{side}</td>
                  <td className="px-6 py-4">{formatSize(pos.szi)}</td>
                  <td className="px-6 py-4">{formatMoney(pos.entryPx)}</td>
                  <td className="px-6 py-4">{formatMoney(pos.positionValue)}</td>
                  <td className={`px-6 py-4 font-bold ${pnlColor}`}>{formatMoney(pos.unrealizedPnl)}</td>
                  <td className="px-6 py-4">{pos.leverage.value}x</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
