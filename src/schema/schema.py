import uuid

from typing import List

from sqlalchemy import UniqueConstraint, Computed, func, text
from sqlmodel import SQLModel, Field, Column, JSON, Text

class RawData(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    header: str
    content: str
    content_hash: str = Field(
        sa_column=Column(
            Text,
            Computed(func.md5(text("header || content"))),
            unique=True,
            index=True
            )
        )

class StructuredData(SQLModel, table=True):
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

class NormalizedData(SQLModel, table=True):
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

class PredictedData(SQLModel, table=True):
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