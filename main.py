import sys
import logging

from cli.command import execute_command 

def main():
    """
    Entry point for the Odoo CLI application.
    Run in shell argument mode or interactive mode based on the input.
    """
    execute_command()


if __name__ == "__main__":
    main()


