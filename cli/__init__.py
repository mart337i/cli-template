import pkgutil
import os.path

__path__ = [
    os.path.abspath(path)
    for path in pkgutil.extend_path(__path__, __name__)
]

from .cli_base.command import Command