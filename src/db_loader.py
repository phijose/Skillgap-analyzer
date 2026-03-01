from sqlalchemy.exc import IntegrityError

from src.schema.main import get_db_store
import json
from pathlib import Path
from src.schema.schema import RawData

db_store = get_db_store()
for f in Path().cwd().joinpath("data").iterdir():
    if f.is_file() and "jobs" in f.name:
        with open(f, encoding='utf-8') as file:
            for item in json.load(file):
                try:
                    rd = RawData(
                        header="\n".join(item['header']),
                        content="\n".join(item['description'])
                    )
                    db_store.insert_data(rd)
                except IntegrityError as e:
                    print("duplicate item found")
                except Exception as e:
                    print(e)




