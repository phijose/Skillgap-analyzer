from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
import json
import time
import random

def scrape_data(location, query, radius, limit, filename):
    limit = limit * 10
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i in range(0, limit, 10):
            encoded_url = build_url(location, query, radius, i)
            page.goto(encoded_url)
            job_cards = page.get_by_role("listitem").locator(".job_seen_beacon")
            count = job_cards.count()
            job_list = []
            for j in range(count):
                try:
                    job_cards.nth(j).scroll_into_view_if_needed(timeout=3000)
                    job_cards.nth(j).click()
                    time.sleep(random.uniform(6, 15))
                    page.wait_for_selector(".jobsearch-HeaderContainer", timeout=3000)
                    job = {
                        "header": page.locator(".jobsearch-HeaderContainer").all_inner_texts(),
                        "description": page.locator(".jobsearch-JobComponent-description").all_inner_texts()
                    }
                    job_list.append(job)
                except Exception as e:
                    print(f"Skipping job {j} due to error: {e}")
                    continue
            data = {
                "jobs": job_list,
                "count": len(job_list),
            }
            with open(f"{filename}.json", "w") as f:
                json.dump(data, f, indent=4)
    time.sleep(random.uniform(10, 20))


def extract_data(page):
    # everything has its time
    pass


def build_url(location, query, radius, next_from):
    params = {
        "q": query,
        "l": location,
        "radius": radius,
        "start": next_from
    }
    base_url = "https://in.indeed.com/jobs"
    return f"{base_url}?{urlencode(params)}"


if __name__ == "__main__":
    scrape_data("Thiruvananthapuram, Kerala", "AI Engineer", 100, 5, "ai-jobs")
    scrape_data("Thiruvananthapuram, Kerala", "AI ML Engineer", 100, 5, "ai-ml-jobs")
    scrape_data("Thiruvananthapuram, Kerala", "ML Engineer", 100, 5, "ml-jobs")
