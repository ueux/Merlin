"""Allows `python -m merlin_engine ...` in addition to the console script."""

import sys

from .cli import main

sys.exit(main())
