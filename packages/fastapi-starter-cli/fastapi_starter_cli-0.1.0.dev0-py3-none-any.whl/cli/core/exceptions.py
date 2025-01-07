import typer
from colorama import Fore, Style

class CLIException(Exception):
    """🚨 Base exception for CLI errors"""
    def __init__(self, message: str):
        self.message = f"{Fore.RED}{message}{Style.RESET_ALL}"
        super().__init__(self.message)
        typer.echo(self.message, err=True)

class ProjectCreationError(CLIException):
    """❌ Error creating project"""
    pass

class DatabaseConfigError(CLIException):
    """❌ Error configuring database"""
    pass