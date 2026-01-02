
from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app (backend must be running)
        page.goto("http://localhost:3000")

        # Wait for data to load
        page.wait_for_selector("text=Account Value")
        page.wait_for_selector("text=Open Positions")

        # Check if table has rows
        page.wait_for_selector("table")

        # Take screenshot
        page.screenshot(path="verification/dashboard.png", full_page=True)
        print("Screenshot taken at verification/dashboard.png")
        browser.close()

if __name__ == "__main__":
    verify_dashboard()
