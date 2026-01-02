import unittest
from monitor import WalletMonitor

class MockClient:
    def __init__(self):
        self.state = {"assetPositions": []}

    def get_user_state(self, address):
        return self.state

class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = WalletMonitor("dummy_address")
        # Replace real client with mock
        self.monitor.client = MockClient()
        self.monitor.webhook_url = "" # disable real network call

    def test_open_position(self):
        # Initial empty state
        self.monitor.update_positions({"assetPositions": []}, alert=False)

        # New state with 1 position
        new_state = {
            "assetPositions": [
                {"position": {"coin": "BTC", "szi": "1.5", "entryPx": "50000"}}
            ]
        }

        # We expect a notification (mocked by print in notifications.py, but here we just check logic doesn't crash)
        # Ideally we'd mock send_discord_alert too to verify calls.
        self.monitor.update_positions(new_state, alert=True)

        self.assertIn("BTC", self.monitor.last_positions)
        self.assertEqual(self.monitor.last_positions["BTC"]["szi"], "1.5")

    def test_close_position(self):
        # Initial state with position
        initial = {
            "assetPositions": [
                {"position": {"coin": "ETH", "szi": "10", "entryPx": "3000"}}
            ]
        }
        self.monitor.update_positions(initial, alert=False)

        # New state empty
        self.monitor.update_positions({"assetPositions": []}, alert=True)

        self.assertNotIn("ETH", self.monitor.last_positions)

    def test_change_size(self):
        # Initial
        initial = {
            "assetPositions": [
                {"position": {"coin": "SOL", "szi": "100", "entryPx": "20"}}
            ]
        }
        self.monitor.update_positions(initial, alert=False)

        # Increase size
        new_state = {
             "assetPositions": [
                {"position": {"coin": "SOL", "szi": "150", "entryPx": "20"}}
            ]
        }
        self.monitor.update_positions(new_state, alert=True)
        self.assertEqual(self.monitor.last_positions["SOL"]["szi"], "150")

if __name__ == "__main__":
    unittest.main()
