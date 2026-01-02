# HyperTracker Clone (日本語版)

CoinMarketManのHyperTrackerにインスパイアされた、Hyperliquidのミラートレード支援・ウォレット監視ツールです。

## 機能

- **リアルタイムダッシュボード**: 口座資産、使用証拠金、保有ポジションを監視します。
- **ポジション追跡**: 各ポジションの詳細（サイズ、取得単価、損益、レバレッジ）を表示します。
- **Discord通知**: バックグラウンド監視システムにより、以下のイベントを通知します：
  - 新規ポジション構築
  - ポジション決済
  - ポジションサイズの増減
- **HIP-3 対応**: APIから返されるすべての資産（HIP-3トークン含む）を自動的に表示します。

## プロジェクト構成

- `backend/`: Python FastAPI アプリケーション（データ取得・監視用）
- `frontend/`: Next.js アプリケーション（ユーザーインターフェース）

## 前提条件

- Python 3.9以上
- Node.js 18以上
- Discord Webhook URL（通知用）

## セットアップと実行

### 1. バックエンド (Backend)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt

# .env ファイルを作成して Discord Webhook を設定 (任意)
echo "DISCORD_WEBHOOK_URL=your_webhook_url_here" > .env

# サーバー起動
uvicorn main:app --reload
```

APIサーバーは `http://localhost:8000` で起動します。

### 2. フロントエンド (Frontend)

```bash
cd frontend
npm install
npm run dev
```

フロントエンドは `http://localhost:3000` でアクセスできます。

## 使い方

1. `http://localhost:3000` をブラウザで開きます。
2. デフォルトで特定のウォレットが表示されています。入力欄から任意のHyperliquidアドレスに変更して追跡できます。
3. **更新 (Refresh)** ボタンをクリックすると手動でデータを更新できます（10秒ごとの自動更新もあり）。
4. **監視開始 (Start Monitor)** ボタンをクリックするとバックグラウンド監視を開始します。対象ウォレットに動きがあるとDiscordに通知が飛びます。

## 技術スタック

- **Frontend**: Next.js, Tailwind CSS, TypeScript
- **Backend**: Python, FastAPI, Requests
- **API**: Hyperliquid Info API (`clearinghouseState`)
