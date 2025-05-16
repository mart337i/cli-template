import sys
import os
from pkgutil import extend_path
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
__path__ = extend_path(__path__, __name__)

from . import cli