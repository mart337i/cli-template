__import__('os').environ['TZ'] = 'UTC'
import cli

if __name__ == "__main__":
    cli.cli_base.execute_command()
