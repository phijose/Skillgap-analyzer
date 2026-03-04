from sqlmodel import select, Session
from src.schema.main import get_db_store
from src.schema.schema import NormalizedData
from src.utils.util import get_embedding_model, normalize_experience


def main():
    embedding_model = get_embedding_model()
    db_store = get_db_store()
    with Session(db_store.engine) as session:
        rows = session.exec(select(NormalizedData)).all()
        for row in rows:
            if row.embedding is None:
                text = f"{row.title} {' '.join(row.category)} {normalize_experience(row.yrs_of_exp)}"
                vector = embedding_model.embed_query(text)
                row.embedding = vector
        session.commit()


if __name__ == "__main__":
    main()
