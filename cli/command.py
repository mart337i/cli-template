import sys
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

def execute_command() -> None:
    """Parse and execute the appropriate command."""
    if len(sys.argv) < 2:
        print(f"Error: No command provided.\n")
        Help().run([])
        sys.exit(1)

    command_name, *args = sys.argv[1:]
    command_cls = commands.get(command_name)

    if not command_cls:
        print(f"Error: Unknown command '{command_name}'.\n")
        Help().run([])
        sys.exit(1)

    command = command_cls()
    if '--help' in args or not args:
        print(command.help())
    else:
        command.run(args)

if __name__ == "__main__":
    execute_command()
