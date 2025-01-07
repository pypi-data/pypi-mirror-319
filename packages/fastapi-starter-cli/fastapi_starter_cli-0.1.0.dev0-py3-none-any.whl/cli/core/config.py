from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class CLIConfig:
    """⚙️ CLI Configuration"""
    VERSION: str = "0.1.0-dev"
    LICENSE: str = "MIT"
    
    BASE_PACKAGES: List[str] = field(default_factory=lambda: [
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "python-dotenv",
        "pydantic-settings"
    ])
    
    DB_PACKAGES: Dict[str, List[str]] = field(default_factory=lambda: {
        "postgresql": ["psycopg2-binary"],
        "mysql": ["PyMySQL"],
        "mariadb": ["PyMySQL"],
        "sqlserver": ["pyodbc"],
        "oracle": ["cx_Oracle"]
    })
    
    OPTIONAL_PACKAGES: Dict[str, List[str]] = field(default_factory=lambda: {
        "migrations": ["alembic"],
        "repository": ["base-repository"]
    })
    
    EXTRA_INDEX_URL: Dict[str, str] = field(default_factory=lambda: {
        "base-repository": "https://test.pypi.org/simple/"
    })
    