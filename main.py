__import__('os').environ['TZ'] = 'UTC'
import clix

if __name__ == "__main__":
    clix.cli_base.execute_command()
