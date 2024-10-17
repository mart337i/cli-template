import argparse
import subprocess
import os
import logging
from pathlib import Path
import sys
import paramiko  # To SSH into the source host and collect neutralize.sql

from ..command import Command

_logger = logging.getLogger(__name__)

class Neutralize(Command):
    """Dump, neutralize, and transfer a production database for testing."""

    def run(self, cmdargs):
        parser = argparse.ArgumentParser(
            prog=f'{Path(sys.argv[0]).name} {self.name}',
            description=self.__doc__,
        )
        
        # Define command line arguments
        parser.add_argument('-s', '--source-host', required=True, help="Remote source host for the production database")
        parser.add_argument('-t', '--target-host', required=True, help="Remote target host for the neutralized dump")
        parser.add_argument('-d', '--dbname', required=True, help="Database name on the source host")
        parser.add_argument('-u', '--dbuser', required=True, help="Database username on the source host")
        parser.add_argument('-f', '--dump-file', default='dump.sql', help="Local file path for the SQL dump")
        parser.add_argument('--source-db-port', default='5432', help="Postgres port on the source host")
        parser.add_argument('--target-db-port', default='5432', help="Postgres port on the target host")
        parser.add_argument('--module-paths', nargs='+', required=True, help="Paths to the module directories on the source host")

        if not cmdargs:
            sys.exit(parser.print_help())

        # Parse arguments
        args = parser.parse_args(args=cmdargs)
        
        dump_file = Path(args.dump_file).resolve()

        # Step 1: Dump the production database from the source host
        self.dump_database(
            source_host=args.source_host,
            dbname=args.dbname,
            dbuser=args.dbuser,
            dump_file=dump_file,
            dbport=args.source_db_port
        )

        # Step 2: Fetch and compile the neutralize.sql scripts from the source host
        compiled_neutralize_sql = self.compile_neutralization_sql(
            source_host=args.source_host,
            dbuser=args.dbuser,
            module_paths=args.module_paths
        )

        # Step 3: Apply the compiled neutralization to the dump file
        self.apply_neutralization(dump_file, compiled_neutralize_sql)

        # Step 4: Send the neutralized dump to the target host
        self.send_dump_to_target(
            target_host=args.target_host,
            dump_file=dump_file,
            dbport=args.target_db_port
        )

    def dump_database(self, source_host, dbname, dbuser, dump_file, dbport):
        """Dump the production database from the remote source host."""
        _logger.info(f"Dumping the production database '{dbname}' from '{source_host}' into '{dump_file}'.")

        dump_command = [
            "pg_dump",
            "-h", source_host,
            "-U", dbuser,
            "-d", dbname,
            "-p", dbport,
            "-F", "plain",
            "-f", str(dump_file)
        ]

        try:
            subprocess.run(dump_command, check=True)
            _logger.info("Database dump completed successfully.")
        except subprocess.CalledProcessError as e:
            _logger.error("Error occurred while dumping the database: %s", str(e))
            sys.exit(1)

    def compile_neutralization_sql(self, source_host, dbuser, module_paths):
        """Retrieve and compile all neutralize.sql files from module directories on the source host."""
        _logger.info(f"Fetching and compiling all neutralization SQL files from '{source_host}'.")

        neutralization_sql = []

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(source_host, username=dbuser)

        # Iterate through each module path and collect the neutralize.sql file
        for module_path in module_paths:
            remote_neutralize_path = f"{module_path}/neutralize.sql"

            _logger.info(f"Checking for neutralize.sql in {remote_neutralize_path}...")

            try:
                # Check if neutralize.sql exists in the directory
                stdin, stdout, stderr = ssh.exec_command(f"test -f {remote_neutralize_path} && echo 'Found'")
                result = stdout.read().decode().strip()

                if result == 'Found':
                    # If found, fetch its content
                    _logger.info(f"Found neutralize.sql in {module_path}. Fetching its content.")
                    sftp = ssh.open_sftp()
                    with sftp.file(remote_neutralize_path, 'r') as f:
                        sql_content = f.read()
                        neutralization_sql.append(sql_content)
                    sftp.close()
                else:
                    _logger.warning(f"neutralize.sql not found in {module_path}. Skipping.")

            except Exception as e:
                _logger.error(f"Error fetching neutralize.sql from {module_path}: {str(e)}")

        ssh.close()

        # Combine all neutralize.sql files into one script in memory
        compiled_sql = "\n-- Compiled Neutralization SQL --\n"
        compiled_sql += "\n".join(neutralization_sql)

        _logger.info(f"Compiled neutralization SQL with {len(neutralization_sql)} scripts.")
        return compiled_sql

    def apply_neutralization(self, dump_file, compiled_neutralize_sql):
        """Apply the compiled neutralization SQL to the database dump."""
        _logger.info(f"Applying the compiled neutralization SQL to the dump file '{dump_file}'.")

        with open(dump_file, 'a') as dump_file_handle:
            dump_file_handle.write(compiled_neutralize_sql)

        _logger.info(f"Neutralization SQL applied to {dump_file}.")

    def send_dump_to_target(self, target_host, dump_file, dbport):
        """Send the neutralized SQL dump to the target remote host."""
        _logger.info(f"Sending the neutralized dump to '{target_host}'.")

        remote_dump_path = f"{target_host}:{dump_file}"

        scp_command = ["scp", str(dump_file), remote_dump_path]

        try:
            subprocess.run(scp_command, check=True)
            _logger.info(f"Neutralized dump successfully sent to {target_host}.")
        except subprocess.CalledProcessError as e:
            _logger.error(f"Failed to send the neutralized dump: {e}")
            sys.exit(1)

