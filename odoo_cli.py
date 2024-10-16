# odoo_cli.py
import sys
import logging

from cli.command import _exec_command 

def main():
    """
    Entry point for the Odoo CLI application.
    Run in shell argument mode or interactive mode based on the input.
    """
    _exec_command()


if __name__ == "__main__":
    main()


