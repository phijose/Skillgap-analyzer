import json
import random
import time
from urllib.parse import urlencode
from seleniumbase import SB

# --- TOR ROTATION (Keep if you still want to try Tor) ---
from stem import Signal
from stem.control import Controller


def renew_tor_ip():
    """Requests a new Tor IP. Note: Indeed heavily blocks Tor exit nodes."""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("  [Tor] New Identity Requested")
            time.sleep(3)
    except Exception:
        print("  [Tor] Could not rotate (Is Tor running?)")


def build_url(location, query, radius, next_from):
    params = {"q": query, "l": location, "radius": radius, "start": next_from}
    return f"https://in.indeed.com/jobs?{urlencode(params)}"


def scrape_data(location, query, radius, limit, filename):
    print(f"\n>>> Starting SeleniumBase Scrape: {query}")
    all_job_list = []
    limit_count = limit * 10

    with SB(uc=True, test=True, locale_code="en") as sb:
        for i in range(0, limit_count, 10):
            # 1. New Identity (If using Tor)
            renew_tor_ip()

            # 2. Open Page with Reconnect (Essential for Cloudflare)
            url = build_url(location, query, radius, i)
            sb.uc_open_with_reconnect(url, reconnect_time=5)

            # 3. FIXED: Human Scrolling
            print("  Scrolling to load results...")
            for _ in range(3):
                sb.execute_script(f"window.scrollBy(0, {random.randint(400, 800)});")
                sb.sleep(1)

            # 4. Extract Job IDs
            job_links = sb.find_elements("a[data-jk]")
            job_ids = list(set([el.get_attribute("data-jk") for el in job_links]))

            for jk in job_ids:
                sb.sleep(random.uniform(5, 12))  # Look like you're reading

                job_url = f"https://in.indeed.com/viewjob?jk={jk}"
                sb.uc_open_with_reconnect(job_url, reconnect_time=4)

                if sb.is_element_visible("#jobDescriptionText"):
                    all_job_list.append({
                        "job_id": jk,
                        "title": sb.get_text("h1"),
                        "description": sb.get_text("#jobDescriptionText")
                    })
                    print(f"    Saved: {jk}")

        # 5. Save Progress
        with open(f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(all_job_list, f, indent=4)


if __name__ == "__main__":
    roles = [
        ("AI Engineer", "ai-jobs"),
        ("AI ML Engineer", "ai-ml-jobs")
    ]

    for title, fname in roles:
        scrape_data("Thiruvananthapuram, Kerala", title, 100, 2, fname)
        # Big wait between different job categories
        time.sleep(random.uniform(20, 45))