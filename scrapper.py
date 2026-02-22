from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
import json
import time
import random
import os


def build_url(location, query, radius, next_from):
    params = {"q": query, "l": location, "radius": radius, "start": next_from}
    return f"https://in.indeed.com/jobs?{urlencode(params)}"


def scrape_data(location_list, query, radius, pages_per_loc, filename):
    print(f"\n>>>> STARTING GLOBAL SEARCH FOR: {query} <<<<")
    all_jobs_for_this_query = []

    for loc in location_list:
        print(f"\n--- Moving to Location: {loc} ---")
        limit_count = pages_per_loc * 10

        for i in range(0, limit_count, 10):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                try:
                    encoded_url = build_url(loc, query, radius, i)
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
                                "header": page.locator(".jobsearch-HeaderContainer").all_inner_texts(),
                                "description": page.locator(".jobsearch-JobComponent-description").all_inner_texts()
                            }
                            all_jobs_for_this_query.append(job)
                            print(f"    [+] Total Collected: {len(all_jobs_for_this_query)}")

                        except Exception as e:
                            continue

                    save_data(all_jobs_for_this_query, filename)

                finally:
                    browser.close()

                wait_time = random.uniform(30, 60)
                print(f"  [Rest] Sleeping for {wait_time:.1f}s before next page...")
                time.sleep(wait_time)


def save_data(all_jobs, filename):
    directory = "data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{filename}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=4, ensure_ascii=False)
    print(f"Successfully saved to: {file_path}")


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
        scrape_data(locations, title, 100, 1, fname)
        long_wait = random.uniform(60, 120)
        print(f"\n>>> ROLE COMPLETED: {title}. Deep rest for {long_wait:.1f}s...")
        time.sleep(long_wait)