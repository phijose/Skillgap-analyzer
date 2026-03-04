import streamlit as st
from sqlalchemy import event
from src.models.normalize_model import make_normalized_data
from src.models.structure_model import make_structured_data
from src.schema.schema import RawData, StructuredData

event.listen(RawData, 'after_insert', make_structured_data)
event.listen(StructuredData, 'after_insert', make_normalized_data)

analysis = st.Page("analysis_page.py", title="Job Analyzer", icon="🤹")
scrapper = st.Page("scrap_page.py", title="Job Scrapper", icon="⛏️")
resume_sr = st.Page("resume_score.py", title="Resume Analyzer", icon="🧑‍🏫")

ui = st.navigation([resume_sr, analysis, scrapper])
ui.run()
