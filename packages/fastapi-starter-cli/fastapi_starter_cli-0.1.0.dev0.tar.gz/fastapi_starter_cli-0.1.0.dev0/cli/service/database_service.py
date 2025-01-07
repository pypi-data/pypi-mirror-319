import os
import typer
from typing import Dict, Tuple
from colorama import Fore, Style
from cli.core.config import CLIConfig
from cli.core.exceptions import DatabaseConfigError
from cli.utils.database_type import DatabaseType
from cli.templates.config.settings_template import SettingsTemplate
from cli.templates.project.database_template import DatabaseTemplate
from cli.service.interface.base_service import IDatabaseService

class DatabaseService(IDatabaseService):
    """🛢️ Service for database configuration"""
    
    def __init__(self):
        self.config = CLIConfig()
        self.db_config: Dict[str, str] = {}
        self.templates = SettingsTemplate()
        
    def create_env_file(self, path: str) -> Tuple[bool, str]:
        """📝 Creates .env file with database configuration"""
        try:
            env_path = os.path.join(path, ".env")
            
            if os.path.exists(env_path):
                raise DatabaseConfigError("⚠️ .env file already exists")
            
            with open(env_path, "w") as env_file:
                for key, value in self.db_config.items():
                    env_file.write(f"{key}={value}\n")
            
            return True, "✅ .env file created successfully"
            
        except Exception as e:
            raise DatabaseConfigError(f"💥 Error creating .env file: {str(e)}")
        

    def select_database(self) -> DatabaseType:
        """🔍 Select database type"""
        try:
            options = [
                f"{Fore.GREEN}1){Style.RESET_ALL} 🐘 PostgreSQL",
                f"{Fore.GREEN}2){Style.RESET_ALL} 🐬 MySQL",
                f"{Fore.GREEN}3){Style.RESET_ALL} 🐋 MariaDB",
                f"{Fore.GREEN}4){Style.RESET_ALL} 🪟 SQL Server",
                f"{Fore.GREEN}5){Style.RESET_ALL} 🏛️  Oracle DB"
            ]
            
            print(f"\n{Fore.CYAN}🛢️ Select database type:{Style.RESET_ALL}")
            for option in options:
                print(option)
                
            while True:
                choice = typer.prompt("Enter option number", type=int)
                if 1 <= choice <= 5:
                    return list(DatabaseType)[choice-1]
                print(f"{Fore.RED}❌ Invalid option. Please select a number from 1 to 5{Style.RESET_ALL}")
        except Exception as e:
            raise DatabaseConfigError(f"💥 Error selecting database: {str(e)}")

    def configure_database(self) -> Dict[str, str]:
        """⚙️ Configure database connection"""
        try:
            print(f"\n{Fore.CYAN}⚙️ Database Configuration:{Style.RESET_ALL}")
            
            self.db_config = {
                "DB_USER": typer.prompt("👤 Database username"),
                "DB_PASSWORD": typer.prompt("🔑 Password", hide_input=True),
                "DB_HOST": typer.prompt("🌐 Host", default="localhost"),
                "DB_PORT": typer.prompt("🔌 Port"),
                "DB_NAME": typer.prompt("📝 Database name")
            }
            
            return self.db_config
        except Exception as e:
            raise DatabaseConfigError(f"💥 Error configuring database: {str(e)}")
        
    def create_database_file(self, project_path: str, db_type: DatabaseType) -> Tuple[bool, str]:
        """📝 Creates database.py with connection configuration"""
        try:
            db_dir = os.path.join(project_path, "src", "db")
            db_file = os.path.join(db_dir, "database.py")
            
            if os.path.exists(db_file):
                raise DatabaseConfigError("⚠️ database.py file already exists")
            
            template_content = DatabaseTemplate.get_template(db_type)
            with open(db_file, "w") as f:
                f.write(template_content)
            
            return True, "✅ Database configuration file created successfully"
            
        except Exception as e:
            raise DatabaseConfigError(f"💥 Error creating database.py: {str(e)}")
        
        
    def create_settings_file(self, project_path: str) -> Tuple[bool, str]:
        """📝 Creates settings.py with database configuration"""
        try:
            config_dir = os.path.join(project_path, "src", "config")
            settings_path = os.path.join(config_dir, "settings.py")
            
            if os.path.exists(settings_path):
                raise DatabaseConfigError("⚠️ settings.py file already exists")
            
            with open(settings_path, "w") as f:
                f.write(self.templates.PYDANTIC_SETTINGS)
            
            return True, "✅ Settings file created successfully"
            
        except Exception as e:
            raise DatabaseConfigError(f"💥 Error creating settings.py: {str(e)}")