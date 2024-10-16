import sys
import shlex

def base_cli(commands, args):
    # Combine the remaining args into a single command string
    command_input = ' '.join(args[1:])  # Skip the '--shell' argument itself
    
    if not command_input:
        print("No command entered. Please provide a command.")
        return

    # Parse the command input
    parsed_args = shlex.split(command_input)

    command = parsed_args[0]

    if command in commands:
        # Create an instance of the command and run it
        o = commands[command]()
        o.run(parsed_args)
    else:
        print(f"Unknown command: {command}. Type 'help' for a list of available commands.")