from cli import Command

class TEST(Command):
    """Greet the user with a friendly message."""
    def run(self, args: list[str]) -> None:
        name = args[0] if args else "world"
        print(f"Hello, {name}!")