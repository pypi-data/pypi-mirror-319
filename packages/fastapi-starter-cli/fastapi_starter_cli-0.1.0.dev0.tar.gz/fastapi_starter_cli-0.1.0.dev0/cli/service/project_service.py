import os
from typing import Optional
from cli.core.exceptions import ProjectCreationError
from cli.service.interface.base_service import IProjectService
from cli.templates.project.project_structure import ProjectStructure
from cli.templates.project.main_template import MainTemplate

class ProjectService(IProjectService):
    """🚀 Service for FastAPI project management"""
    
    def __init__(self):
        self.structure = ProjectStructure()
        
    def get_current_path(self) -> str:
        """📂 Gets the current working directory"""
        return os.getcwd()
        
    def create_project(self, base_path: str, name: str) -> Optional[str]:
        """📂 Creates a new FastAPI project"""
        if not base_path or not name:
            raise ProjectCreationError("🚫 Base path and project name are required")

        try:
            project_path = os.path.join(base_path, name)
            
            if not os.path.exists(base_path):
                raise ProjectCreationError(f"❌ Base path '{base_path}' does not exist")

            if os.path.exists(project_path):
                raise ProjectCreationError(f"⚠️ Project '{name}' already exists")

            os.makedirs(project_path)
            return project_path

        except ProjectCreationError:
            raise
        except Exception as e:
            raise ProjectCreationError(f"💥 Error creating project: {str(e)}")

    def create_structure(self, base_path: str) -> bool:
        """🏗️ Creates the FastAPI project structure"""
        if not base_path:
            raise ProjectCreationError("🚫 Base path is required")

        try:
            if not os.path.exists(base_path):
                raise ProjectCreationError(f"❌ Path '{base_path}' does not exist")

            for directory in self.structure.DIRECTORIES:
                dir_path = os.path.join(base_path, directory)
                os.makedirs(dir_path, exist_ok=True)

            for file in self.structure.INIT_FILES:
                file_path = os.path.join(base_path, file)
                with open(file_path, "a") as f:
                    f.write("")

            return True

        except ProjectCreationError:
            raise
        except Exception as e:
            raise ProjectCreationError(f"💥 Error creating structure: {str(e)}")
        
        
    def create_main_file(self, project_path: str, project_name: str) -> bool:
        """📝 Creates main.py FastAPI application file"""
        try:
            main_path = os.path.join(project_path, "src", "main.py")
            
            if os.path.exists(main_path):
                content = MainTemplate.get_template(project_name)
                with open(main_path, "w") as f:
                    f.write(content)
                return True
                
            content = MainTemplate.get_template(project_name)
            with open(main_path, "w") as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            raise ProjectCreationError(f"💥 Error creating main.py: {str(e)}")