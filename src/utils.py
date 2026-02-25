import os
import json
from pathlib import Path

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