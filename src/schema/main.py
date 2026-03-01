from sqlmodel import SQLModel, Session, select
import streamlit as st
from src.schema.schema import RawData, StructuredData, NormalizedData, PredictedData


class __DBStore:
    def __init__(self):
        self.conn = st.connection('sql')
        self.engine = self.conn.engine
        self.__init_db()

    def insert_data(self, new_data):
        with Session(self.engine) as session:
            session.add(new_data)
            session.commit()

    def select_data(self, entity, filters):
        with Session(self.engine) as session:
            statement = select(entity)
            for col, val in filters.items():
                statement = statement.where(getattr(entity, col) == val)
            return session.exec(statement).first()

    @st.cache_resource
    def __init_db(_self):
        SQLModel.metadata.create_all(_self.engine)

@st.cache_resource
def get_db_store():
    return __DBStore()