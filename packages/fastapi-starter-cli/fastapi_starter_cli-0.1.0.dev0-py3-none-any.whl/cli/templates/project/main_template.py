from dataclasses import dataclass

@dataclass
class MainTemplate:
    """📄 Template for FastAPI main application"""
    
    @staticmethod
    def get_template(project_name: str = "FastAPI", version: str = "0.1.0") -> str:
        return f"""from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="{project_name} API",
    description="API for {project_name}",
    version="{version}",
    debug=True,
    lifespan=lifespan
)
"""