import typer
from colorama import Fore, Style
from cli.core.exceptions import CLIException
from cli.core.config import CLIConfig
from cli.service.project_service import ProjectService
from cli.service.database_service import DatabaseService
from cli.service.venv_service import VenvService
from cli.service.requirements_service import RequirementsService

class BaseCommand:
    """🎮 Base class for CLI commands"""

    def __init__(self):
        """Initialize services"""
        self.config = CLIConfig()
        self.project_service = ProjectService()
        self.database_service = DatabaseService()
        self.venv_service = VenvService()
        self.requirements_service = RequirementsService()

    def _print_header(self, title: str) -> None:
        """🎨 Print formatted header"""
        terminal_width = 80
        separator = f"{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}"
        print(f"\n{separator}")
        print(f"{Fore.YELLOW}{title.center(terminal_width)}{Style.RESET_ALL}")
        print(f"{separator}\n")

    def _print_success(self, message: str) -> None:
        """✅ Print success message"""
        typer.echo(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def _print_error(self, message: str) -> None:
        """❌ Print error message"""
        typer.echo(f"{Fore.RED}{message}{Style.RESET_ALL}", err=True)

    def _print_info(self, message: str) -> None:
        """ℹ️ Print info message"""
        typer.echo(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

    def _handle_error(self, error: Exception) -> None:
        """🛠️ Handle command errors"""
        if isinstance(error, CLIException):
            self._print_error(str(error))
        else:
            self._print_error(f"💥 Unexpected error: {str(error)}")