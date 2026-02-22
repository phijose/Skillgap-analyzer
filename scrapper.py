from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
import json
import time
import random


def build_url(location, query, radius, next_from):
    params = {"q": query, "l": location, "radius": radius, "start": next_from}
    return f"https://in.indeed.com/jobs?{urlencode(params)}"


def scrape_data(location, query, radius, limit, filename):
    limit_count = limit * 10
    all_jobs_for_this_query = []  # Store everything here to avoid overwriting

    for i in range(0, limit_count, 10):
        # LAUNCH browser inside the loop so it survives the IP change
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            try:
                encoded_url = build_url(location, query, radius, i)
                print(f"\n--- Scraping {query} | Start: {i} ---")
                page.goto(encoded_url, wait_until="domcontentloaded", timeout=60000)

                # Give Indeed a moment to verify you aren't a bot
                time.sleep(random.uniform(5, 8))

                job_cards = page.locator(".job_seen_beacon")
                count = job_cards.count()

                for j in range(count):
                    try:
                        card = job_cards.nth(j)
                        card.scroll_into_view_if_needed(timeout=3000)
                        card.click()

                        # Human-like reading time
                        time.sleep(random.uniform(12, 18))

                        page.wait_for_selector(".jobsearch-HeaderContainer", timeout=5000)

                        job = {
                            "header": page.locator(".jobsearch-HeaderContainer").all_inner_texts(),
                            "description": page.locator(".jobsearch-JobComponent-description").all_inner_texts()
                        }
                        all_jobs_for_this_query.append(job)
                        print(f"  [+] Saved job {len(all_jobs_for_this_query)}")

                    except Exception as e:
                        print(f"  [!] Skipping job {j}: {e}")
                        continue

                # Save progress after every page so you don't lose data if it crashes
                with open(f"{filename}.json", "w", encoding="utf-8") as f:
                    json.dump(all_jobs_for_this_query, f, indent=4)

            finally:
                browser.close()  # Close browser BEFORE changing IP

            print(f"\n[PAUSE] Finished page {i // 10 + 1}.")
            input(">>> Toggle Airplane Mode on your phone, then press Enter to continue...")


if __name__ == "__main__":
    roles = [
        ("AI Engineer", "ai-jobs"),
        ("AI ML Engineer", "ai-ml-jobs"),
        ("ML Engineer", "ml-jobs")
    ]
    locations = [
        "Thiruvananthapuram, Kerala",
        "Kochi, Kerala",
        "Chennai, Tamil Nadu",
        "Bengaluru, Karnataka",
        "Hyderabad, Telangana"
    ]

    for title, fname in roles:
        scrape_data("Thiruvananthapuram, Kerala", title, 100, 5, fname)
        print(f"--- Completed role: {title} ---")
        input(">>> HUGE IP CHANGE: Toggle Airplane Mode and press Enter for the next role...")