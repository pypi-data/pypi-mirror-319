import shutil
from colorama import Fore, Style
import textwrap
import getpass

def wrap_and_center(text: str, width: int) -> str:
    wrapped_lines = textwrap.wrap(text, width=width)
    centered_lines = []
    for line in wrapped_lines:
        left_padding = (width - len(line)) // 2
        centered_line = f"{' ' * left_padding}{line}"
        centered_lines.append(centered_line)
    return "\n".join(centered_lines)

def show_banner():
    """🎨 Display CLI banner"""
    username = getpass.getuser()
    terminal_width = shutil.get_terminal_size(fallback=(80, 24)).columns
    banner_line = "=" * terminal_width
    banner_text = "🚀 Welcome FastAPI Starter Project CLI 🚀"
    centered_banner_text = wrap_and_center(banner_text, terminal_width)
    
    banner = f"""
{Fore.CYAN}{banner_line}
{Fore.YELLOW}{centered_banner_text}{Fore.CYAN}
{banner_line}
{Style.RESET_ALL}
👋 Hello, {Fore.GREEN}{username}{Style.RESET_ALL}! Welcome to FastAPI Generator CLI.

{Fore.BLUE}🌟 Create modern FastAPI projects with ease!{Style.RESET_ALL}
"""
    print(banner)