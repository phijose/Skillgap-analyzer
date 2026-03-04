import streamlit as st
from src.scrapper import IndeedScraper


def run_scraping():
    if not st.session_state.job_title or not st.session_state.locations:
        st.error("Please provide both a Job Title and at least one Location.")
        return
    role = st.session_state.job_title
    locations = st.session_state.locations
    with st.status("🚀 Initializing Scraper...", expanded=True) as status:
        st.write("Connecting to Indeed...")
        scraper = IndeedScraper()
        scraper.scrape_data(locations=locations,query=role)
        status.update(label="✅ Scraping Complete!", state="complete", expanded=False)
    st.success(f"Data saved to database for {st.session_state.job_title}")


# --- UI Setup ---
st.set_page_config("Job Scraper", page_icon="⛏️")
st.title("⛏️ Job Scraper")
st.caption("Automated background data collection from Indeed")

# Grouping inputs in a nice card-like container
with st.container(border=True):
    st.text_input("Job Title", key="job_title", placeholder="e.g. AI Engineer")
    locations_list = [
        "Thiruvananthapuram, Kerala", "Kochi, Kerala",
        "Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Hyderabad, Telangana"
    ]
    st.multiselect("Target Locations", options=locations_list, key="locations")
    _, btn_col = st.columns([4, 1])
    btn_col.button("Start Scraping", on_click=run_scraping, type="primary", use_container_width=True)