import uuid

from typing import List
from sqlmodel import SQLModel, Field, Column, JSON

class raw_data(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    header: str
    content: str

class structured_data(SQLModel, table=True):
    id:uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    employer: str
    location: str
    salary: str
    category: List[str] = Field(default=[], sa_column=Column(JSON))
    domain: str
    job_type: str
    responsibilities: List[str] = Field(default=[], sa_column=Column(JSON))
    tech_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    tools_and_platforms: List[str] = Field(default=[], sa_column=Column(JSON))
    yrs_of_exp: str
    education: str
    soft_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    certification: List[str] = Field(default=[], sa_column=Column(JSON))
    deadline: str

class normalized_data(SQLModel, table=True):
    id:uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    employer: str
    location: str
    salary: str
    category: List[str] = Field(default=[], sa_column=Column(JSON))
    domain: str
    job_type: str
    responsibilities: List[str] = Field(default=[], sa_column=Column(JSON))
    tech_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    tools_and_platforms: List[str] = Field(default=[], sa_column=Column(JSON))
    yrs_of_exp: str
    education: str
    soft_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    certification: List[str] = Field(default=[], sa_column=Column(JSON))
    deadline: str

class predicted_data(SQLModel, table=True):
    id:uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    employers: List[str] = Field(default=[], sa_column=Column(JSON))
    locations: List[str] = Field(default=[], sa_column=Column(JSON))
    salary: str
    category: List[str] = Field(default=[], sa_column=Column(JSON))
    domain:  List[str] = Field(default=[], sa_column=Column(JSON))
    job_type: List[str] = Field(default=[], sa_column=Column(JSON))
    responsibilities: List[str] = Field(default=[], sa_column=Column(JSON))
    tech_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    tools_and_platforms: List[str] = Field(default=[], sa_column=Column(JSON))
    yrs_of_exp: str
    education: str
    soft_skills: List[str] = Field(default=[], sa_column=Column(JSON))
    certification: List[str] = Field(default=[], sa_column=Column(JSON))
    deadline: str