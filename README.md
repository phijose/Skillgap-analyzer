```mermaid
graph TD
    %% Define Shapes
    User((User))
    IndeedScraper[Indeed Scraper]
    PostgreSQL[(PostgreSQL)]
    
    subgraph Processing_Layer [Processing Models]
        StructModel(Structurization Model)
        NormModel(Normalization Model)
        SumModel(Summarization Model)
    end

    Server([Server])
    UI[Streamlit UI]

    %% User Actions
    User -->|Scrap| LocJob[List of Location + Job Title]
    User <-->|Analyze| JobDetails[Job Title + Experience + Location]

    %% Scraper Flow
    LocJob --> IndeedScraper
    IndeedScraper -->|save data| PostgreSQL

    %% Database Internal Triggers (Models)
    PostgreSQL -->|on insert raw-data| StructModel
    StructModel -->|save| PostgreSQL

    PostgreSQL -->|on insert struct-raw| NormModel
    NormModel -->|save| PostgreSQL

    %% Data Output Flow
    PostgreSQL -->|data| SumModel
    SumModel -->|output| Server
    
    %% UI and Server interaction
    JobDetails <--> Server
    Server --> PostgreSQL
    UI -.-> User
