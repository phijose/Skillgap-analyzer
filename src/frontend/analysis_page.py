import streamlit as st
import yaml
from src.schema.main import get_db_store
from src.schema.schema import NormalizedData
from src.utils.util import normalize_experience

# --- CONFIG & STYLES ---
st.set_page_config(page_title="Job Analyzer", page_icon="🤹", layout="centered")
db_store = get_db_store()

def analyze_callback():
    if not st.session_state.job_title:
        st.error("Please enter a Job Title first!")
        return
    location = st.session_state.get('location')
    text = f"{st.session_state.get('job_title')} {normalize_experience(st.session_state.get('experience'))}"
    rows = db_store.getdata_by_similarity(NormalizedData, text, location)
    if rows:
        clean_data = [row.model_dump(exclude={"embedding"}) for row in rows]
        st.write(clean_data)
    else:
        st.warning("No matching data found.")


# --- UI HEADER ---
st.title("🤹 Job Analyzer")
st.caption("Identify the skills and market requirements.")

# --- INPUT SECTION ---
with st.container(border=True):
    st.text_input("Job Title", key="job_title", placeholder="e.g. AI Engineer")
    col1, col2 = st.columns(2)
    locations_list = [
        "All Locations", "Thiruvananthapuram, Kerala", "Kochi, Kerala", "Chennai, Tamil Nadu",
        "Bengaluru, Karnataka", "Hyderabad, Telangana"
    ]
    col1.selectbox("Location", options=locations_list, key="location")
    col2.text_input("Experience", key="experience", placeholder="e.g. 3-5 Years")

    lt_btn_col, _, _, btn_col = st.columns([1, 1, 1, 1])
    # lt_btn_col.button("Load Data", on_click=load_json_data, type="secondary", use_container_width=True)
    btn_col.button("Analyze", on_click=analyze_callback, type="primary", use_container_width=True)

# --- DATA DISPLAY ---
sample_object = {
    "title": "AI ENGINEER",
    "employer": "Wipro Limited",
    "location": "Bengaluru, Karnataka",
    "salary": "Not Specified",
    "category": [
        "MLOps",
        "Generative AI"
    ],
    "domain": "Technology Services and Consulting",
    "job_type": "Full-time",
    "responsibilities": [
        "Manage the technical scope of a project in line with requirements at all stages",
        "Gather information from various sources and interpret patterns and trends",
        "Develop record management process and policies",
        "Provide sales data, proposals, data insights, and account reviews to clients",
        "Identify areas to increase efficiency and automation of processes",
        "Set up and maintain automated data processes",
        "Analyze complex data sets and prepare reports for internal and external audiences",
        "Create data dashboards, graphs, and visualization to showcase business performance",
        "Mine and analyze large datasets and present insights to management"
    ],
    "tech_skills": [
        "AI",
        "Artificial Intelligence"
    ],
    "tools_and_platforms": [],
    "yrs_of_exp": "3-5 Years",
    "education": "Not Specified",
    "soft_skills": [],
    "certification": [],
    "deadline": "Not Specified"
}

st.divider()
st.subheader("📋 Job Specification")
with st.container(border=True):
    st.code(yaml.dump(sample_object, sort_keys=False), language="yaml")