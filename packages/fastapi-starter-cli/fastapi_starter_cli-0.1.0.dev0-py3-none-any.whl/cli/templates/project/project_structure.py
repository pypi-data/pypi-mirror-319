from dataclasses import dataclass, field
from typing import List

@dataclass
class ProjectStructure:
    """Define la estructura base de un proyecto FastAPI"""
    
    DIRECTORIES: List[str] = field(default_factory=lambda: [
        "src",
        "src/controller",
        "src/config",
        "src/db",
        "src/dto",
        "src/service",
        "src/model",
        "src/model/entity",
        "src/model/enum",
        "src/repository",
        "test",
    ])
    
    INIT_FILES: List[str] = field(default_factory=lambda: [
        "src/__init__.py",
        "src/controller/__init__.py",
        "src/config/__init__.py",
        "src/db/__init__.py",
        "src/dto/__init__.py",
        "src/service/__init__.py",
        "src/model/__init__.py",
        "src/model/entity/__init__.py",
        "src/model/enum/__init__.py",
        "src/repository/__init__.py",
        "src/main.py",
    ])