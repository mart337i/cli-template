# CLI Tool Template

A simple and extensible template for building command-line interfaces (CLI) in Python. Lightweight, user-friendly, and easy to expand with new commands.

---

## Features

- **Dynamic Command Registration**: Subclass `Command` to automatically register new commands.
- **Addons Support**: Dynamically load commands from an `addons` directory.
- **Built-in Help**: Lists all available commands and their usage.
- **Extensible**: Add commands by subclassing `Command` and implementing the `run` method.
- **Namespace Package**: The `cli` package is a namespace package for easy extension.

---

## Usage

Run the CLI tool:

```bash
python cli_tool.py <command> [arguments]
```

### Example Commands

- **help**: Lists all commands.
  ```bash
  python cli_tool.py help
  ```

- **Custom Commands**: New commands appear in the help menu.

---

## Adding Commands

### Direct Commands

Subclass `Command` to define new commands. Example:

```python
class Greet(Command):
    """Greet the user."""
    def run(self, args: list[str]) -> None:
        name = args[0] if args else "world"
        print(f"Hello, {name}!")
```

Run it:
```bash
python cli_tool.py greet Alice
# Output: Hello, Alice!
```

### Addons Commands

Add commands dynamically from an `addons` directory. Example structure:

```
addons/
    my_command/
        __init__.py
        __manifest__.py
```

**`my_command/__init__.py`**:
```python
class MyCommand(Command):
    """My custom addon command."""
    def run(self, args: list[str]) -> None:
        print("Running my custom command!")
```

Commands are automatically discovered when `addons` is loaded.

---

## Configuration

By default, addons are loaded from the `addons` directory relative to the script. Override with:

```bash
python cli_tool.py --addons-path=/custom/path <command>
```

---

## Example Session

```bash
$ python cli_tool.py help
CLI Tool - Use 'cli_tool.py <command> --help' for command-specific help.

Available commands:
  help        Display the list of available commands.
  greet       Greet the user.
  mycommand   My custom addon command.

$ python cli_tool.py greet John
Hello, John!

$ python cli_tool.py mycommand
Running my custom command!

$ python cli_tool.py unknown
Error: Unknown command 'unknown'.
```

---

## Requirements

- Python 3.12 or later.

---

## License

Open source under the MIT License.

--- 

This version trims unnecessary details while keeping all key functionality and usage examples clear and concise. Let me know if you need further edits!