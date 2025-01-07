from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
from cli.utils.database_type import DatabaseType

class IProjectService(ABC):
    @abstractmethod
    def create_structure(self, base_path: str) -> bool: pass
    
    @abstractmethod
    def create_project(self, base_path: str, name: str) -> Optional[str]: pass

class IDatabaseService(ABC):
    @abstractmethod
    def select_database(self) -> DatabaseType: pass
    
    @abstractmethod
    def configure_database(self) -> Dict[str, str]: pass

class IVenvService(ABC):
    @abstractmethod
    def create_venv(self, path: str) -> Tuple[bool, str]: pass

class IRequirementsService(ABC):
    @abstractmethod
    def create_requirements(self, path: str, db_type: Optional[DatabaseType] = None) -> Tuple[bool, str]: pass