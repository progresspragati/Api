from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 🔹 Load .env
load_dotenv(dotenv_path=".env")

EMAIL = os.getenv("AIRALO_EMAIL")
PASSWORD = os.getenv("AIRALO_PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("❌ Missing credentials in .env file")

LOGIN_URL = "https://app.partners.airalo.com/sign-in"
BASE_URL = "https://app.partners.airalo.com/api-orders"


def wait_for_page_ready(page):
    """
    Reliable wait (instead of networkidle)
    """
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(5000)
    page.wait_for_selector("[data-testid='trailButtonWrapper']", timeout=60000)


def count_orders(page):
    """
    Adjust selector if needed
    """
    page.wait_for_timeout(4000)

    rows = page.locator("tbody tr")
    count = rows.count()

    order_dates = []
    for i in range(count):
        try:
            row = rows.nth(i)
            date_text = row.locator("td").nth(1).inner_text()
            order_dates.append(date_text)
        except:
            pass

    return count, order_dates

def get_airalo_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 🔹 STEP 1: LOGIN
        page.goto(LOGIN_URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(5000)

        # Fill email
        try:
            page.get_by_role("textbox", name="Email").fill(EMAIL)
        except:
            page.fill("input[type='email']", EMAIL)

        # Fill password
        try:
            page.get_by_role("textbox", name="Password").fill(PASSWORD)
        except:
            page.fill("input[type='password']", PASSWORD)

        # Click login
        try:
            page.get_by_role("button", name="Continue").click()
        except:
            page.locator("button[type='submit']").click()

        wait_for_page_ready(page)

        # 🔹 STEP 2: OPEN ORDERS PAGE
        page.goto(BASE_URL)
        wait_for_page_ready(page)

        # 🔹 STEP 3: SCREENSHOT
        screenshot_path = "orders_page.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print("📸 Screenshot saved")

        # 🔹 STEP 4: CLICK DATE DROPDOWN
        page.locator("[data-testid='trailDateRangePickerField']").click()
        page.wait_for_timeout(500)

       # 🔹 STEP 5: CLICK TODAY (directly, no dropdown)
        page.locator("[data-testid='trailChipGroupItem']", has_text="Today").click()

        today_count, today_orders = count_orders(page)
        today_date = datetime.today().strftime("%Y-%m-%d")

        print(f"\n📅 TODAY ({today_date})")
        print("Orders:", today_count if today_count != 1 else 0)

        # 🔹 STEP 6: CLICK YESTERDAY

        page.locator("[data-testid='trailDateRangePickerField']").click()
        page.wait_for_timeout(500)

        page.locator("[data-testid='trailChipGroupItem']", has_text="Yesterday").click()

        yesterday_count, yesterday_orders = count_orders(page)
        yesterday_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"\n📅 YESTERDAY ({yesterday_date})")
        print("Orders:", yesterday_count if yesterday_count != 1 else 0)

        browser.close()

        return {
            "today_date": today_date,
            "today_orders": today_count-1,
            "yesterday_date": yesterday_date,
            "yesterday_orders": yesterday_count-1,
            "screenshot": screenshot_path
        }

if __name__ == "__main__":
    data = get_airalo_data()

    print("\n📊 AIRALO REPORT")
    print(f"Today ({data['today_date']}): {data['today_orders']}")
    print(f"Yesterday ({data['yesterday_date']}): {data['yesterday_orders']}")
    print(f"Screenshot: {data['screenshot']}")