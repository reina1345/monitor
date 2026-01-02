from client import HyperliquidClient
import json

def test_fetch_data():
    client = HyperliquidClient()
    address = "0x5b5d51203a0f9079f8aeb098a6523a13f298c060"

    print(f"Fetching state for {address}...")
    state = client.get_user_state(address)

    if state:
        print("State fetched successfully.")
        print("Positions:")
        for pos in state.get('assetPositions', []):
            p = pos['position']
            print(f"- {p['coin']}: Size {p['szi']}, Entry {p['entryPx']}")
    else:
        print("Failed to fetch state.")

if __name__ == "__main__":
    test_fetch_data()
