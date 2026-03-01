from sqlalchemy import event, exists
from sqlmodel import SQLModel, Session, select
import streamlit as st
from src.schema.schema import RawData, StructuredData, NormalizedData, PredictedData


class DBStore:
    def __init__(self):
        self.conn = st.connection('sql')
        self.engine = self.conn.engine
        self.__init_db()
        from src.models.normalize_model import make_normalized_data
        from src.models.structure_model import make_structured_data
        event.listen(RawData, 'after_insert', make_structured_data)
        event.listen(StructuredData, 'after_insert', make_normalized_data)

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

    def select_all_unprocessed(self, entity_b, entity_s):
        with Session(self.engine) as session:
            subquery = select(entity_s.id).where(entity_s.id == entity_b.id)
            stmt = select(entity_b).where(~exists(subquery))
            return session.exec(stmt).all()

    @st.cache_resource
    def __init_db(_self):
        SQLModel.metadata.create_all(_self.engine)

@st.cache_resource
def get_db_store():
    return DBStore()