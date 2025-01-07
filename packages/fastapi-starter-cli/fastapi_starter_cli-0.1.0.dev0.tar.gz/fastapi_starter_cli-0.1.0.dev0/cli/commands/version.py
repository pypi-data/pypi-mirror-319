import typer
from cli.commands.base import BaseCommand

app = typer.Typer(help="🔍 Version Information Commands")
command = BaseCommand()

@app.command(name="version")
def show_version():
    """📌 Shows CLI version information"""
    try:
        command._print_header("🚀 FastAPI Starter CLI Information")
        command._print_info(f"📦 Version: {command.config.VERSION}")
        command._print_info(f"📄 License: {command.config.LICENSE}")
    except Exception as e:
        command._handle_error(e)

if __name__ == "__main__":
    app()