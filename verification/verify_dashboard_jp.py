
from playwright.sync_api import sync_playwright

def verify_dashboard_jp():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app (backend must be running)
        page.goto("http://localhost:3000")

        # Wait for data to load
        page.wait_for_selector("text=口座残高")
        page.wait_for_selector("text=保有ポジション一覧")

        # Take screenshot
        page.screenshot(path="verification/dashboard_jp.png", full_page=True)
        print("Screenshot taken at verification/dashboard_jp.png")
        browser.close()

if __name__ == "__main__":
    verify_dashboard_jp()
