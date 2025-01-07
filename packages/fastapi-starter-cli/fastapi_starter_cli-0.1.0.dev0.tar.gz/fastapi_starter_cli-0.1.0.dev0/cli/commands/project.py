import typer
from cli.commands.base import BaseCommand
from cli.core.exceptions import CLIException

app = typer.Typer(help="🚀 FastAPI Project Management Commands")
command = BaseCommand()

@app.command(name="create-project")
def create_project():
    """📦 Creates a new FastAPI project"""
    try:
        project_name = typer.prompt("📝 Enter project name")
        current_path = command.project_service.get_current_path()
        
        command._print_header(f"📂 Creating FastAPI Project: {project_name}")
        
        project_path = command.project_service.create_project(current_path, project_name)
        if not project_path:
            return
        
        command.project_service.create_structure(project_path)
        command._print_success("✅ Project structure created successfully")
        
        success, message = command.venv_service.create_venv(project_path)
        if not success:
            raise CLIException(message)
        command._print_success(message)
        
        if typer.confirm("🛢️ Do you want to configure a database?"):
            db_type = command.database_service.select_database()
            db_config = command.database_service.configure_database()
            
            success, message = command.requirements_service.create_requirements(project_path, db_type)
            if not success:
                raise CLIException(message)
            command._print_success(message)
            
            success, message = command.database_service.create_env_file(project_path)
            if not success:
                raise CLIException(message)
            command._print_success(message)
            
            success, message = command.database_service.create_settings_file(project_path)
            if not success:
                raise CLIException(message)
            command._print_success(message)
            
            success, message = command.database_service.create_database_file(project_path, db_type)
            if not success:
                raise CLIException(message)
            command._print_success(message)
            
            try:
                command.project_service.create_main_file(project_path, project_name)
                command._print_success("✅ Main application file created/updated successfully")
            except Exception as e:
                command._handle_error(e)
                
            if typer.confirm("\n🔄 Would you like to configure database migrations with Alembic?"):
                success, message = command.requirements_service.add_optional_package(project_path, "migrations")
                if not success:
                    raise CLIException(message)
                command._print_success(message)
                
            if typer.confirm("\n📦 Would you like to install Base Repository for automated CRUD operations?"):
                success, message = command.requirements_service.add_optional_package(project_path, "repository")
                if not success:
                    raise CLIException(message)
                command._print_success(message)
            
            command._print_info("\n🚀 Next steps:")
            command._print_info("Activate your virtual environment 🐍✨")
            command._print_info("Install the project's dependencies with pip 📦")
            command._print_info("1. venv\\Scripts\\activate")
            command._print_info("2. pip install -r requirements.txt\n")
        
        command._print_success("✨ Project created successfully!")
        
    except Exception as e:
        command._handle_error(e)

@app.command(name="init-project")
def init_project():
    """🏗️ Initialize FastAPI project in current directory"""
    try:
        current_path = command.project_service.get_current_path()
        
        command._print_header("🚀 Initializing FastAPI Project")
        
        command.project_service.create_structure(current_path)
        command._print_success("✅ Project structure created successfully")
        
        success, message = command.venv_service.create_venv(current_path)
        if not success:
            raise CLIException(message)
        command._print_success(message)
        
        if typer.confirm("🛢️ Do you want to configure a database?"):
            db_type = command.database_service.select_database()
            db_config = command.database_service.configure_database()
            
            success, message = command.requirements_service.create_requirements(current_path, db_type)
            if not success:
                raise CLIException(message)
            command._print_success(message)
            
            command._print_info("\n🚀 Next steps:")
            command._print_info("1. venv\\Scripts\\activate")
            command._print_info("2. pip install -r requirements.txt\n")
        
        command._print_success("✨ Project initialized successfully!")
        
    except Exception as e:
        command._handle_error(e)
