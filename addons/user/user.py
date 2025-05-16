from clix.cli.command import Command

class User(Command):
    """Configure the current user"""
    def run(self, args: list[str]) -> None:
        """Run the command with the given arguments."""
        print("HI")

    def help(self) -> str:
        """Return help information for the command."""
        return self.__doc__ or "No help available."
