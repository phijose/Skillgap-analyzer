import json
import time
import random
import os
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright
from src.schema.main import get_db_store
from src.schema.schema import RawData
import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

class IndeedScraper:
    def __init__(self, base_url="https://in.indeed.com/jobs"):
        self.base_url = base_url
        self.data_dir = "data"
        self._ensure_dir()
        self.db_store = get_db_store()

    def _ensure_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def build_url(self, location, query, radius, start_index):
        params = {
            "q": query,
            "l": location,
            "radius": radius,
            "start": start_index
        }
        return f"{self.base_url}?{urlencode(params)}"

    def get_all_inner_text(self, page, selector):
        return "\n".join(page.locator(selector).all_inner_texts())

    def scrape_data(self, locations, query, radius=100, pages_per_loc=1):
        print(f"\n>>>> STARTING GLOBAL SEARCH FOR: {query} <<<<")
        all_jobs = []

        for loc in locations:
            print(f"\n--- Moving to Location: {loc} ---")
            limit_count = pages_per_loc * 10

            for i in range(0, limit_count, 10):
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=False)
                    context = browser.new_context()
                    page = context.new_page()

                    try:
                        encoded_url = self.build_url(loc, query, radius, i)
                        print(f"  [Page {i // 10 + 1}] Target: {loc} | Start: {i}")

                        page.goto(encoded_url, wait_until="load", timeout=60000)
                        time.sleep(random.uniform(5, 8))

                        # Check for "No jobs found" or Captcha
                        if "hcaptcha" in page.content().lower() or "cloudflare" in page.content().lower():
                            print("  [!] Blocked by Cloudflare. Cooling down...")
                            time.sleep(120)  # Extra long rest if blocked
                            continue

                        job_cards = page.locator(".job_seen_beacon")
                        count = job_cards.count()

                        if count == 0:
                            print(f"  [?] No more jobs found for {loc}. Moving to next location.")
                            break

                        for j in range(count):
                            try:
                                card = job_cards.nth(j)
                                card.scroll_into_view_if_needed(timeout=3000)
                                card.click()

                                time.sleep(random.uniform(12, 18))

                                page.wait_for_selector(".jobsearch-HeaderContainer", timeout=5000)

                                job = {
                                    "header": self.get_all_inner_text(page, ".jobsearch-HeaderContainer"),
                                    "description": self.get_all_inner_text(page, ".jobsearch-JobComponent-description"),
                                }
                                self.db_store.insert_data(RawData(**job))
                                print(f"    [+] Total Collected: {len(all_jobs)}")
                            except Exception as e:
                                continue
                    finally:
                        browser.close()
                    wait_time = random.uniform(30, 60)
                    print(f"  [Rest] Sleeping for {wait_time:.1f}s before next page...")
                    time.sleep(wait_time)
