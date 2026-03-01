from langchain_core.output_parsers import JsonOutputParser
from sqlmodel import SQLModel


class BaseChainModel:
    def __init__(self, llm, output_model, prompt, output_table, exclude_data, db_store):
        self.llm = llm
        self.exclude_data = exclude_data
        self.output_model = output_model
        self.parser = JsonOutputParser(pydantic_object=output_model)
        self.output_table = output_table
        self.db_store = db_store
        self.prompt = prompt.partial(
            format_instructions=self.parser.get_format_instructions()
        )
        self.chain = self.prompt | llm | self.parser

    def invoke(self, record: SQLModel, copy_base=False):
        try:
            text_to_process = record.model_dump_json(exclude=self.exclude_data)
            processed_data = self.chain.invoke({"input_text" :text_to_process})
            if copy_base:
                merged = record.model_dump()
                merged.update(processed_data)
            else:
                merged = {**processed_data, "id": record.id}
            new_data = self.output_table(**merged)
            self.db_store.insert_data(new_data)
            print(f"record inserted to {self.output_model}")
        except Exception as e:
            print(e)

