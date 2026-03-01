import os
import json
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.schema.schema import RawData, StructuredData

load_dotenv(Path.cwd().joinpath(".env"))

BASE_DIR = Path(__file__).resolve().parent.parent

def save_json(data, filename, directory="data"):
    directory = BASE_DIR / directory
    os.makedirs(directory, exist_ok=True)
    file_path = directory / f"{filename}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Successfully saved to: {file_path}")

def load_json(filename, directory="data"):
    directory = BASE_DIR / directory
    file_path = directory / f"{filename}.json"
    if not file_path.exists():
        print(f"Error: {file_path} not found.")
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def initial_trigger(db_store):
    raw_data = db_store.select_all_unprocessed(RawData, StructuredData)
    from src.models.structure_model import get_structured_chain
    struct_chain = get_structured_chain()
    for data in raw_data:
        struct_chain.invoke(data)


def get_llm(model="llama"):
    model="gpt"
    if model == "gpt":
        return ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    else:
        return OllamaLLM(model="llama3", temperature=0)