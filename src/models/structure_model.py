import json
import os
from typing import List
from pydantic import BaseModel, Field
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.utils import save_json

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

llm = OllamaLLM(model="llama3", temperature=0)

parser = JsonOutputParser(pydantic_object=JobStructure)

prompt = PromptTemplate(
    template="""You are a professional HR Data Analyst. 
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
    {raw_text}
    """,
    input_variables=["raw_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

def clean_extracted_data(record, chain):
    cleaned_results = []
    text_to_process = json.dumps(record, indent=2)
    try:
        structured_data = chain.invoke({"raw_text": text_to_process})
        save_json(structured_data, "structured_data")
        print(structured_data)
        cleaned_results.append(structured_data)
        print(f"  [✓] Processed: {structured_data.get('title')}")
    except Exception as e:
        print(f"  [!] Failed to process a record: {e}")

def test():
    print(prompt)
    # print(parser.get_format_instructions())

if __name__ == "__main__":
    record = {
        "header": [
            "AI ENGINEER\n- job post\nWipro Limited\n3.8\n3.8 out of 5 stars\nBengaluru, Karnataka\nYou must create an Indeed account before continuing to the company website to apply\nApply on company site"
        ],
        "description": [
            "Location\nBengaluru, Karnataka\n&nbsp;\nFull job description\nJob Description\n\n\n\n\nJob Title: AI ENGINEER\nCity: Bengaluru\nState/Province: Karnataka\nPosting Start Date: 1/12/26\nWipro Limited (NYSE: WIT, BSE: 507685, NSE: WIPRO) is a leading technology services and consulting company focused on building innovative solutions that address clients’ most complex digital transformation needs. Leveraging our holistic portfolio of capabilities in consulting, design, engineering, and operations, we help clients realize their boldest ambitions and build future-ready, sustainable businesses. With over 230,000 employees and business partners across 65 countries, we deliver on the promise of helping our customers, colleagues, and communities thrive in an ever-changing world. For additional information, visit us at www.wipro.com.\nJob Description:\nJob Description\n\nRole Purpose\n\nThe purpose of this role is to interpret data and turn into information (reports, dashboards, interactive visualizations etc) which can offer ways to improve a business, thus affecting business decisions.\n\n͏\n\nDo\n\n1. Managing the technical scope of the project in line with the requirements at all stages\n\na. Gather information from various sources (data warehouses, database, data integration and modelling) and interpret patterns and trends\n\nb. Develop record management process and policies\n\nc. Build and maintain relationships at all levels within the client base and understand their requirements.\n\nd. Providing sales data, proposals, data insights and account reviews to the client base\n\ne. Identify areas to increase efficiency and automation of processes\n\nf. Set up and maintain automated data processes\n\ng. Identify, evaluate and implement external services and tools to support data validation and cleansing.\n\nh. Produce and track key performance indicators\n\n\n2. Analyze the data sets and provide adequate information\n\na. Liaise with internal and external clients to fully understand data content\n\nb. Design and carry out surveys and analyze survey data as per the customer requirement\n\nc. Analyze and interpret complex data sets relating to customerÃ¢ÂÂs business and prepare reports for internal and external audiences using business analytics reporting tools\n\nd. Create data dashboards, graphs and visualization to showcase business performance and also provide sector and competitor benchmarking\n\ne. Mine and analyze large datasets, draw valid inferences and present them successfully to management using a reporting tool\n\nf. Develop predictive models and share insights with the clients as per their requirement\n\n͏\n\nDeliver\n\nNo\nPerformance Parameter\nMeasure\n\n\n1.\nAnalyses data sets and provide relevant information to the client\nNo. Of automation done, On-Time Delivery, CSAT score, Zero customer escalation, data accuracy\n\n\n\n\n͏\n͏\nMandatory Skills: AI : Artificial Intelligence .\n\n\nExperience: 3-5 Years .\n\n\nReinvent your world. We are building a modern Wipro. We are an end-to-end digital transformation partner with the boldest ambitions. To realize them, we need people inspired by reinvention. Of yourself, your career, and your skills. We want to see the constant evolution of our business and our industry. It has always been in our DNA - as the world around us changes, so do we. Join a business powered by purpose and a place that empowers you to design your own reinvention.\n\n&nbsp;",
            "Job Description\n\n\n\n\nJob Title: AI ENGINEER\nCity: Bengaluru\nState/Province: Karnataka\nPosting Start Date: 1/12/26\nWipro Limited (NYSE: WIT, BSE: 507685, NSE: WIPRO) is a leading technology services and consulting company focused on building innovative solutions that address clients’ most complex digital transformation needs. Leveraging our holistic portfolio of capabilities in consulting, design, engineering, and operations, we help clients realize their boldest ambitions and build future-ready, sustainable businesses. With over 230,000 employees and business partners across 65 countries, we deliver on the promise of helping our customers, colleagues, and communities thrive in an ever-changing world. For additional information, visit us at www.wipro.com.\nJob Description:\nJob Description\n\nRole Purpose\n\nThe purpose of this role is to interpret data and turn into information (reports, dashboards, interactive visualizations etc) which can offer ways to improve a business, thus affecting business decisions.\n\n͏\n\nDo\n\n1. Managing the technical scope of the project in line with the requirements at all stages\n\na. Gather information from various sources (data warehouses, database, data integration and modelling) and interpret patterns and trends\n\nb. Develop record management process and policies\n\nc. Build and maintain relationships at all levels within the client base and understand their requirements.\n\nd. Providing sales data, proposals, data insights and account reviews to the client base\n\ne. Identify areas to increase efficiency and automation of processes\n\nf. Set up and maintain automated data processes\n\ng. Identify, evaluate and implement external services and tools to support data validation and cleansing.\n\nh. Produce and track key performance indicators\n\n\n2. Analyze the data sets and provide adequate information\n\na. Liaise with internal and external clients to fully understand data content\n\nb. Design and carry out surveys and analyze survey data as per the customer requirement\n\nc. Analyze and interpret complex data sets relating to customerÃ¢ÂÂs business and prepare reports for internal and external audiences using business analytics reporting tools\n\nd. Create data dashboards, graphs and visualization to showcase business performance and also provide sector and competitor benchmarking\n\ne. Mine and analyze large datasets, draw valid inferences and present them successfully to management using a reporting tool\n\nf. Develop predictive models and share insights with the clients as per their requirement\n\n͏\n\nDeliver\n\nNo\nPerformance Parameter\nMeasure\n\n\n1.\nAnalyses data sets and provide relevant information to the client\nNo. Of automation done, On-Time Delivery, CSAT score, Zero customer escalation, data accuracy\n\n\n\n\n͏\n͏\nMandatory Skills: AI : Artificial Intelligence .\n\n\nExperience: 3-5 Years .\n\n\nReinvent your world. We are building a modern Wipro. We are an end-to-end digital transformation partner with the boldest ambitions. To realize them, we need people inspired by reinvention. Of yourself, your career, and your skills. We want to see the constant evolution of our business and our industry. It has always been in our DNA - as the world around us changes, so do we. Join a business powered by purpose and a place that empowers you to design your own reinvention."
        ]
    }
    clean_extracted_data(record, chain)
    # test()