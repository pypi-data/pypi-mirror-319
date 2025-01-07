import os
from typing import Optional, Tuple
from cli.core.config import CLIConfig
from cli.utils.database_type import DatabaseType
from cli.core.exceptions import CLIException

class RequirementsService:
    """📦 Service for managing project requirements"""
    
    def __init__(self):
        self.config = CLIConfig()

    def create_requirements(self, path: str, db_type: Optional[DatabaseType] = None) -> Tuple[bool, str]:
        """📝 Generates requirements.txt file"""
        try:
            if not os.path.exists(path):
                raise CLIException(f"❌ Path '{path}' does not exist")
            
            requirements = self.config.BASE_PACKAGES.copy()
            
            if db_type:
                db_packages = self.config.DB_PACKAGES.get(db_type.value, [])
                requirements.extend(db_packages)
            
            req_path = os.path.join(path, "requirements.txt")
            with open(req_path, "w") as f:
                f.write("\n".join(requirements))
            
            return True, "✅ Requirements.txt created successfully"
        except Exception as e:
            return False, f"💥 Error creating requirements.txt: {str(e)}"
        
    def add_optional_package(self, path: str, package_type: str) -> Tuple[bool, str]:
        """📝 Adds optional package to requirements.txt"""
        try:
            if not os.path.exists(path):
                raise CLIException(f"❌ Path '{path}' does not exist")
            
            req_path = os.path.join(path, "requirements.txt")
            packages = self.config.OPTIONAL_PACKAGES.get(package_type, [])
            
            with open(req_path, "a") as f:
                f.write("\n# Optional packages\n")
                for package in packages:
                    if package in self.config.EXTRA_INDEX_URL:
                        f.write(f"--extra-index-url {self.config.EXTRA_INDEX_URL[package]}\n")
                    f.write(f"{package}\n")
            
            return True, f"✅ Added {package_type} packages to requirements.txt"
        except Exception as e:
            return False, f"💥 Error adding {package_type} packages: {str(e)}"