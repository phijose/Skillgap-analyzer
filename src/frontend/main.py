import streamlit as st
import yaml

def analyze_callback():
    st.balloons()
    pass

st.set_page_config("Skillgap Analyzer", page_icon="🤹")
st.title("SkillGap Analyzer")
st.text_input("Job Title", key="job_title")
left_col, right_col = st.columns(2)
left_col.text_input("Location", key="location")
right_col.text_input("Experiance", key="experiance")
right_col.container(horizontal_alignment="right").button("Analyze", on_click=analyze_callback)
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

st.markdown(f"""
### Job Specification
```yaml
{yaml.dump(sample_object, sort_keys=False)}
```
""")
