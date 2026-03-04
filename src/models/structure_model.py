from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from src.models.base_chain_model import BaseChainModel
from src.schema.main import get_db_store
from src.schema.schema import StructuredData
from src.utils.util import get_llm
import streamlit as st

class JobStructure(BaseModel):
    title: str = Field(description="The formal job title")
    employer: str = Field(description="The name of the employer or company")
    location: str = Field(description="The city and state of the office")
    salary: str = Field(description="The annual salary pay range (e.g., 5-10 LPA, 12 LPA). If not found, use 'Not Specified'")
    category: List[str] = Field(description="Select all applicable labels from: [MLOps, Generative AI, Computer Vision, NLP, Traditional ML, Data Engineering, Software Engineering, AI Agents, Healthcare, Finance, Research]")
    domain: str = Field(description="Industry: e.g., 'Healthcare', 'FinTech', 'IT Services'")
    job_type: str = Field(description="Employment type: Remote, In-person, Hybrid, or Not Specified")
    responsibilities: List[str] = Field(description="List of key duties, daily tasks, or what the person will actually do in this role (e.g., 'Develop ML models', 'Mentor junior devs')")
    tech_skills: List[str] = Field(description="List of specific tools, languages (Python, SQL), and frameworks (React, PyTorch)")
    tools_and_platforms: List[str] = Field(description="Cloud or specific software (AWS, CAD, CAE, Docker)")
    yrs_of_exp: str = Field(description="Required experience range, e.g., '2-4 years' or 'Entry Level'. Use 'Not Specified' if missing.")
    education: str = Field(description="Minimum degree required (e.g., B.Tech, MS, PhD, or 'Not Specified')")
    soft_skills: List[str] = Field(description="List of soft skills like 'Teamwork', 'Agile', 'Public Speaking'")
    certification: List[str] = Field(description="List of required certifications (e.g., AWS Certified, PMP). Return empty list [] if none.")
    deadline: str = Field(description="Application deadline date if mentioned, else 'Not Specified'")

llm = get_llm()

prompt = PromptTemplate(
    template="""
    You are a professional HR Data Analyst. 
    Your task is to extract structured information from the job description below.
    
    IMPORTANT: Return ONLY the JSON object. Do not include any introductory text, 
    explanations, or markdown code blocks (like ```json).
    
    Guidelines:
    - For 'responsibilities', extract the core actions.
    - If a section is missing, use 'Not Specified' for strings or [] for lists.
    - Remove duplicate responsibilities.
    - Do not copy company description into responsibilities.
    - Extract only role-specific tasks.
    
    {format_instructions}
    
    Raw Job Text: 
    {input_text}
    """,
    input_variables=["input_text"]
)

exclude_data = {"id", "content_hash"}

@st.cache_resource
def get_structured_chain():
    db_store = get_db_store()
    return BaseChainModel(llm, JobStructure, prompt, StructuredData, exclude_data, db_store)

def make_structured_data(mapper, connection, target):
    struct_model = get_structured_chain()
    struct_model.invoke(target)