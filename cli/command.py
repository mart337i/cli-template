import logging
import os
import sys
from pathlib import Path

from cli.base_cli import base_cli
from cli.interactive_shell import interactive_cli

commands = {}

class Command:
    name = None
    def __init_subclass__(cls):
        cls.name = cls.name or cls.__name__.lower()
        commands[cls.name] = cls

    def help(self):
        """Displays help for the command."""
        return self.__doc__ or "No help available."

ODOO_HELP = """\
Odoo CLI, use '{odoo_cli} --help' for regular server options.

Available commands:
    {command_list}

Use '{odoo_cli} <command> --help' for individual command help."""

class Help(Command):
    """ Display the list of available commands """
    def run(self, args):
        padding = max([len(cmd) for cmd in commands]) + 2
        command_list = "\n    ".join([
            "    {}{}".format(name.ljust(padding), (command.__doc__ or "").strip())
            for name, command in sorted(commands.items())
        ])
        print(ODOO_HELP.format(  # pylint: disable=bad-builtin
            odoo_cli=Path(sys.argv[0]).name,
            command_list=command_list
        ))

def _exec_command():
    args = sys.argv[1:]
    command = args[0]

    if command in commands:
        o = commands[command]()
        if len(args) == 1 or '--help' in args:  
            print(o.run(args))
            return
        else:
            o.run(args)
    else:
        sys.exit(f"Unknown command '{command}'")