import requests
import json
import logging

def send_discord_alert(webhook_url: str, message: str):
    if not webhook_url:
        logging.warning("No Discord webhook URL provided. Skipping notification.")
        print(f"[MOCK NOTIFICATION] {message}")
        return

    payload = {
        "content": message
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logging.info("Discord notification sent successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to send Discord notification: {e}")
