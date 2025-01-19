import sys
import logging
from pathlib import Path
from typing import Dict, Type

# Dictionary to store commands
commands: Dict[str, Type["Command"]] = {}

class Command:
    """Base class for all commands."""
    name: str = ""

    def __init_subclass__(cls):
        cls.name = cls.name or cls.__name__.lower()
        commands[cls.name] = cls

    def run(self, args: list[str]) -> None:
        """Run the command with the given arguments."""
        print(self.help())

    def help(self) -> str:
        """Return help information for the command."""
        return self.__doc__ or "No help available."

CLI_HELP_TEMPLATE = """\
CLI Tool - Use '{cli_name} <command> --help' for command-specific help.

Available commands:
{command_list}
"""

class Help(Command):
    """Display the list of available commands."""
    def run(self, args: list[str]) -> None:
        cli_name = Path(sys.argv[0]).name
        padding = max(len(name) for name in commands) + 2
        command_list = "\n".join(
            f"  {name.ljust(padding)}{cmd_cls().help().strip()}"
            for name, cmd_cls in sorted(commands.items())
        )
        print(CLI_HELP_TEMPLATE.format(cli_name=cli_name, command_list=command_list))


def initialize_sys_path(addons_path: str):
    """Initialize the system path for addon discovery."""
    sys.path.append(addons_path)

def get_modules(addons_path: str) -> list[str]:
    """Discover addon modules in the specified path."""
    modules = []
    for path in Path(addons_path).iterdir():
        if path.is_dir() and (path / '__init__.py').exists():
            modules.append(path.name)
    return modules

def get_module_path(module: str, addons_path: str) -> str:
    """Return the filesystem path of a module."""
    return str(Path(addons_path) / module)

def load_addon_commands(addons_path: str):
    """
    Discover and load Python modules from the specified addons directory.

    Args:
        addons_path (str): The path to the addons directory.
    """
    addons_path = Path(addons_path)  # Ensure it's a Path object

    if not addons_path.is_dir():
        raise ValueError(f"Invalid addons directory: {addons_path}")

    # Add the addons path to sys.path to allow dynamic imports
    sys.path.append(str(addons_path))

    # Iterate over each module directory in the addons path
    for module_dir in addons_path.iterdir():
        if module_dir.is_dir() and (module_dir / '__init__.py').exists():
            # Check if a CLI-specific directory exists inside the module
            cli_dir = module_dir / "cli"
            if cli_dir.is_dir():
                try:
                    # Dynamically import the CLI module
                    cli_module = f"{module_dir.name}.cli"
                    __import__(cli_module)
                    logging.info(f"Successfully loaded CLI module: {cli_module}")
                except Exception as e:
                    logging.error(f"Failed to load CLI module from {module_dir}: {e}")
            else:
                logging.warning(f"No CLI directory found in {module_dir}")
        else:
            logging.warning(f"Skipping non-module directory: {module_dir}")
def execute_command():
    args = sys.argv[1:]

    base_dir = Path(__file__).resolve().parents[2]
    default_path = base_dir / "addons"
    addons_path = default_path

    if len(args) > 1 and args[0].startswith('--addons-path='):
        addons_path = args[0].split('=', 1)[1]
        args = args[1:]

    load_addon_commands(addons_path)

    # Default command
    command = "help"

    # Subcommand discovery
    if args and not args[0].startswith("-"):
        command = args[0]
        args = args[1:]

    if command in commands:
        command_instance = commands[command]()
        command_instance.run(args)
    else:
        sys.exit(f"Unknown command '{command}'")
