import os, json
from pathlib import Path
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from src.utils import save_json

load_dotenv(dotenv_path=Path().cwd().joinpath(".env"))

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

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

parser = JsonOutputParser(pydantic_object=NormaliseJob)

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
{uncleaned_text}

{format_instructions}
""",
    input_variables=["uncleaned_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | llm | parser

def clean_extracted_data(record, chain):
    text_to_process = json.dumps(record, indent=2)
    normalised_data = chain.invoke({"uncleaned_text", text_to_process})
    try:
        save_json(normalised_data, "normalised_data")
        print(normalised_data)
        normalised_data.append(normalised_data)
        print(f"  [✓] Processed: {normalised_data.get('title')}")
    except Exception as e:
        print(f"  [!] Failed to process a record: {e}")


if __name__ == "__main__":
    record = {
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
        "soft_skills": [],
    }
    clean_extracted_data(record, chain)