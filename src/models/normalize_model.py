from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from src.models.base_chain_model import BaseChainModel
from src.schema.main import get_db_store
from src.schema.schema import NormalizedData
from src.utils.util import get_llm
import streamlit as st

class NormaliseJob(BaseModel):
    tech_skills: List[str] = Field(
        description=(
            "Deduplicated and normalized core technical skills such as programming languages, "
            "frameworks, and technical domains. Use canonical names and proper casing."
        )
    )
    tools_and_platforms: List[str] = Field(
        description=(
            "Deduplicated and standardized software tools, cloud platforms, libraries, "
            "databases, DevOps tools, or development environments."
        )
    )
    soft_skills: List[str] = Field(
        description=(
            "Normalized interpersonal and behavioral skills such as communication, "
            "teamwork, leadership, problem-solving, adaptability."
        )
    )
    responsibilities: List[str] = Field(
        description=(
            "Cleaned and concise action-oriented job responsibilities written as short phrases. "
            "Remove duplicates and avoid vague statements."
        )
    )

llm = get_llm("gpt")

prompt = PromptTemplate(
    template="""
    Normalize and deduplicate the following structured JSON job data.
    
    Rules:
    - Remove duplicates (including semantic duplicates).
    - Use canonical industry names (e.g., AI → Artificial Intelligence).
    - Use proper casing.
    - Do not add new information.
    - Keep categories unchanged.
    - Output strictly in the required JSON format.
    
    Input:
    {input_text}
    
    {format_instructions}
    """,
    input_variables=["input_text"]
)

exclude_data = {"id"}

@st.cache_resource
def get_normalized_chain():
    db_store = get_db_store()
    return BaseChainModel(llm, NormaliseJob, prompt, NormalizedData, exclude_data, db_store)

def make_normalized_data(mapper, connection, target):
    norm_model = get_normalized_chain()
    norm_model.invoke(target, copy_base=True)