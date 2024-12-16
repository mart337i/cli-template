# CLI Tool Template

This project provides a simple and extensible template for building command-line interfaces (CLI) in Python, using only standard libraries. It is designed to be lightweight, user-friendly, and easy to expand with new commands.

---

## Features

- **Dynamic Command Registration**: 
  Subclass the `Command` base class to automatically register new commands.
  
- **Built-in Help**: 
  Includes a `help` command to list all available commands and display usage information.

- **Extensible**: 
  Easily add new commands by defining a subclass of `Command` and implementing the `run` method.

- **Error Handling**: 
  Provides clear feedback for unknown or missing commands.

- **Pure Standard Library**: 
  Uses only Python 3.12 standard library modules, ensuring compatibility and simplicity.

---

## Installation

No installation is required! Just clone or download the repository and execute the script using Python 3.12 or later.

---

## Usage

Run the CLI tool with the desired command:

```bash
python cli_tool.py <command> [arguments]
```

### Built-in Commands

1. **help**: Lists all available commands and their descriptions.
   ```bash
   python cli_tool.py help
   ```
   
2. **Custom Commands**: Any additional commands you define will appear in the help menu automatically.

---

## Adding Commands

To add a new command:

1. Create a new class that subclasses `Command`.
2. Optionally, set a `name` attribute. If not set, the class name (in lowercase) is used as the command name.
3. Implement the `run(self, args: list[str])` method to define the command's behavior.
4. Add a docstring to describe the command. This will appear in the help menu.

### Example

Here’s an example of adding a `greet` command:

```python
class Greet(Command):
    """Greet the user with a friendly message."""
    def run(self, args: list[str]) -> None:
        name = args[0] if args else "world"
        print(f"Hello, {name}!")
```

With this command added, you can now run:

```bash
python cli_tool.py greet Alice
# Output: Hello, Alice!
```

---

## Code Structure

- **`Command` Base Class**: 
  The foundation for all commands. Implements dynamic registration and default behaviors.
  
- **`commands` Dictionary**: 
  Stores mappings of command names to their corresponding classes.
  
- **`execute_command` Function**: 
  Parses CLI arguments and invokes the appropriate command.

---

## Example Session

```bash
$ python cli_tool.py help
CLI Tool - Use 'cli_tool.py <command> --help' for command-specific help.

Available commands:
  help   Display the list of available commands.

$ python cli_tool.py greet John
Hello, John!

$ python cli_tool.py unknown
Error: Unknown command 'unknown'.

$ python cli_tool.py greet --help
Greet the user with a friendly message.
```

---

## Requirements

- Python 3.12 or later.

---

## License

This project is open source and available under the MIT License.
