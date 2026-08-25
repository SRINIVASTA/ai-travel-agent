import json
import os
import sys
from playwright.sync_api import sync_playwright

def run_automation():
    if not os.path.exists("payload.json"):
        print("Error: No payload file found. Run Step 1 in the app first.", file=sys.stderr)
        return

    with open("payload.json", "r") as f:
        data = json.load(f)

    print(f"Loaded payload for: {data['booking_type']}")
    
    with sync_playwright() as p:
        # Opens a real, visible browser window on your desktop
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        if data['booking_type'] == "IRCTC Train":
            print("Navigating to Official IRCTC Developer Portal...")
            page.goto("https://irctc.co.in")
            
            # Close initial popup alerts if they appear
            try:
                page.wait_for_selector("button:has-text('OK')", timeout=4000)
                page.click("button:has-text('OK')")
            except:
                pass
                
            # Automatically type the travel routing fields
            if data.get('source_city'):
                page.fill("p-autocomplete[id='origin'] input", data['source_city'])
                page.keyboard.press("Enter")
                
            if data.get('destination_city'):
                page.fill("p-autocomplete[id='destination'] input", data['destination_city'])
                page.keyboard.press("Enter")
                
            if data.get('travel_date'):
                page.fill("p-calendar[id='jDate'] input", data['travel_date'])
                page.keyboard.press("Enter")
                
            print("\n🚨 [HUMAN CHECKPOINT]")
            print("Route details typed! Solve the CAPTCHA and log in to continue.")
            page.pause()  # Prevents the window from closing instantly

        elif data['booking_type'] == "TTD Seva":
            print("Navigating to TTD Instructions Gateway...")
            page.goto("https://ap.gov.in")
            
            print("\n💡 TTD uses intense security wait-rooms.")
            print(f"Your passenger details are ready to inject once you pass the login wall: {data['passengers']}")
            page.pause()

if __name__ == "__main__":
    run_automation()
