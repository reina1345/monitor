import asyncio
import logging
from client import HyperliquidClient
from notifications import send_discord_alert

class WalletMonitor:
    def __init__(self, address: str, webhook_url: str = ""):
        self.address = address
        self.webhook_url = webhook_url
        self.client = HyperliquidClient()
        self.last_positions = {}  # Map coin -> position dict
        self.is_running = False

    async def start(self, interval: int = 10):
        self.is_running = True
        logging.info(f"Starting monitor for {self.address}")

        # Initial fetch to populate state without alerting
        initial_state = self.client.get_user_state(self.address)
        if initial_state:
            self.update_positions(initial_state, alert=False)

        while self.is_running:
            try:
                state = self.client.get_user_state(self.address)
                if state:
                    self.update_positions(state, alert=True)
            except Exception as e:
                logging.error(f"Error in monitor loop: {e}")

            await asyncio.sleep(interval)

    def stop(self):
        self.is_running = False

    def update_positions(self, state, alert=True):
        current_positions = {}
        if 'assetPositions' in state:
            for item in state['assetPositions']:
                pos = item['position']
                coin = pos['coin']
                current_positions[coin] = pos

        # Check for changes
        for coin, new_pos in current_positions.items():
            old_pos = self.last_positions.get(coin)

            if not old_pos:
                # New position opened
                if float(new_pos['szi']) != 0:
                    self.notify_open(coin, new_pos, alert)
            else:
                # Position exists, check for changes
                self.check_change(coin, old_pos, new_pos, alert)

        # Check for closed positions
        for coin, old_pos in self.last_positions.items():
            if coin not in current_positions:
                # Position completely disappeared (closed)
                self.notify_close(coin, old_pos, 0, alert)
            elif float(current_positions[coin]['szi']) == 0 and float(old_pos['szi']) != 0:
                 self.notify_close(coin, old_pos, 0, alert)


        self.last_positions = current_positions

    def check_change(self, coin, old_pos, new_pos, alert):
        old_size = float(old_pos['szi'])
        new_size = float(new_pos['szi'])

        if old_size == new_size:
            return

        msg = ""
        if (old_size > 0 and new_size > old_size) or (old_size < 0 and new_size < old_size):
             msg = f"📈 積増 {coin} ポジション\n新サイズ: {new_size}"
        elif (old_size > 0 and new_size < old_size) or (old_size < 0 and new_size > old_size):
             # Partial close or flip
             if new_size == 0:
                 self.notify_close(coin, old_pos, 0, alert)
                 return
             else:
                 msg = f"📉 縮小 {coin} ポジション\n新サイズ: {new_size}"

        if msg and alert:
             send_discord_alert(self.webhook_url, msg)

    def notify_open(self, coin, pos, alert):
        if not alert: return
        size = pos['szi']
        entry = pos['entryPx']
        side = "買い(LONG)" if float(size) > 0 else "売り(SHORT)"
        msg = f"🚀 新規 {side} {coin} \nサイズ: {size}\n取得価格: {entry}"
        send_discord_alert(self.webhook_url, msg)

    def notify_close(self, coin, pos, exit_px, alert):
        if not alert: return
        size = pos['szi']
        entry = pos['entryPx']
        side = "買い(LONG)" if float(size) > 0 else "売り(SHORT)"
        msg = f"💰 決済 {side} {coin}\nサイズ: {size}\n取得価格: {entry}"
        send_discord_alert(self.webhook_url, msg)
