import requests
import json

class HyperliquidClient:
    BASE_URL = "https://api.hyperliquid.xyz/info"

    def get_user_state(self, address: str):
        """
        Fetches the clearinghouse state (positions, margin, etc.) for a user.
        """
        payload = {
            "type": "clearinghouseState",
            "user": address
        }
        try:
            response = requests.post(self.BASE_URL, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching user state: {e}")
            return None

    def get_user_fills(self, address: str):
        """
        Fetches the trade history (fills) for a user.
        """
        payload = {
            "type": "userFills",
            "user": address
        }
        try:
            response = requests.post(self.BASE_URL, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching user fills: {e}")
            return None
