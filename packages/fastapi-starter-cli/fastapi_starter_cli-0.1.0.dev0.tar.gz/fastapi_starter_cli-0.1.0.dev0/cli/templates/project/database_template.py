from dataclasses import dataclass
from cli.utils.database_type import DatabaseType

@dataclass
class DatabaseTemplate:
    """🛢️ Database connection templates"""
    
    @staticmethod
    def get_template(db_type: DatabaseType) -> str:
        templates = {
            DatabaseType.POSTGRESQL: """from sqlmodel import SQLModel, create_engine, Session
from src.config.settings import settings
from src.model.entity import *

postgres_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
""",
            DatabaseType.MYSQL: """from sqlmodel import SQLModel, create_engine, Session
from src.config.settings import settings
from src.model.entity import *

maria_db_url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(maria_db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
""",
            DatabaseType.MARIADB: """from sqlmodel import SQLModel, create_engine, Session
from src.config.settings import settings
from src.model.entity import *

maria_db_url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(maria_db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
""",
            DatabaseType.SQLSERVER: """from sqlmodel import SQLModel, create_engine, Session
from src.config.settings import settings
from src.model.entity import *

sqlserver_url = f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(sqlserver_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
""",
            DatabaseType.ORACLE: """from sqlmodel import SQLModel, create_engine, Session
from src.config.settings import settings
from src.model.entity import *

oracle_url = f"oracle+cx_oracle://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/?service_name={settings.DB_NAME}"

engine = create_engine(oracle_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
"""
        }
        return templates.get(db_type, "")