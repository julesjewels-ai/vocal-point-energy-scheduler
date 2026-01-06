from playwright.sync_api import sync_playwright, expect

def verify_ux():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app
        page.goto("http://localhost:8000")

        # 1. Verify aria-live attribute on status
        status = page.locator("#status")
        expect(status).to_have_attribute("aria-live", "polite")
        expect(status).to_have_attribute("aria-atomic", "true")
        expect(status).to_have_attribute("role", "status")
        print("✅ aria-live attributes verified")

        # 2. Verify focus styles
        # Focus on settings button
        settings_btn = page.locator(".settings-btn")
        settings_btn.focus()
        page.screenshot(path="verification/focus_settings.png")

        # Focus on record button
        record_btn = page.locator("#recordBtn")
        record_btn.focus()
        page.screenshot(path="verification/focus_record.png")

        print("✅ Screenshots captured")
        browser.close()

if __name__ == "__main__":
    verify_ux()
