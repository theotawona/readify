from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "zahavi_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    session = Session(engine)
    yield session