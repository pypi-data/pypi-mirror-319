import typer
from colorama import init, Fore, Style
from cli.commands.base import BaseCommand
from cli.commands.project import app as project_command
from cli.commands.version import app as version_command
from cli.utils.terminal import clear_screen
from cli.utils.banner import show_banner

init(autoreset=True)

app = typer.Typer(
    help="🚀 FastAPI Project Generator CLI",
    no_args_is_help=False
)

class MainCommand(BaseCommand):
    """🎮 Main CLI implementation"""
    
    def show_menu(self):
        """📋 Show main menu"""
        self._print_header("Available Commands")
        
        # Project Management Commands
        self._print_info(f"\n{Fore.YELLOW}🛠️  Project Management:{Style.RESET_ALL}")
        print(f"  • {Fore.GREEN}fastapi create-project{Style.RESET_ALL} - Create new FastAPI project")
        print(f"  • {Fore.GREEN}fastapi init-project{Style.RESET_ALL}   - Initialize project in current directory")
        
        # System Commands
        self._print_info(f"\n{Fore.YELLOW}⚙️  System:{Style.RESET_ALL}")
        print(f"  • {Fore.GREEN}version{Style.RESET_ALL}            - Show CLI version")
        
        # Help Tip
        print(f"\n{Fore.BLUE}💡 Tip:{Style.RESET_ALL} Use --help with any command for more information\n")

app.add_typer(project_command, name="start")
app.add_typer(version_command, name="cli")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """🚀 Initialize CLI and show main menu"""
    try:
        main_command = MainCommand()
        clear_screen()
        show_banner()
        
        if ctx.invoked_subcommand is None:
            main_command.show_menu()
            
    except Exception as e:
        typer.echo(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}", err=True)

if __name__ == "__main__":
    app()