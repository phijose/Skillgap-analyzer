from sqlalchemy import event, exists
from sqlmodel import SQLModel, Session, select
import streamlit as st
from src.schema.schema import RawData, StructuredData, NormalizedData, PredictedData
from src.utils.util import get_embedding_model


class DBStore:
    def __init__(self):
        self.conn = st.connection('sql')
        self.engine = self.conn.engine
        self.__init_db()

    def getdata_by_similarity(self, entity, query_text, location, limit=10):
        embedding_model = get_embedding_model()
        query_vector = embedding_model.embed_query(query_text)
        with Session(self.engine) as session:
            stmt = select(entity)
            if location != "All Locations":
                stmt = stmt.where(entity.location == location)
            stmt = (
                stmt
                .order_by(entity.embedding.l2_distance(query_vector))
                .limit(limit)
            )
            return session.exec(stmt).all()

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