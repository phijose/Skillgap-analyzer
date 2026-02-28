from sqlmodel import SQLModel
import streamlit as st
from src.schema.schema import raw_data, structured_data, normalized_data

def get_conn():
    return st.connection('sql')

@st.cache_resource
def init_db():
    SQLModel.metadata.create_all(get_conn().engine)

if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True