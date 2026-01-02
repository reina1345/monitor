from notifications import send_discord_alert

def test_notification():
    # Test with no URL (should print to console)
    print("Testing mock notification...")
    send_discord_alert("", "Test message from HyperTracker clone")

if __name__ == "__main__":
    test_notification()
