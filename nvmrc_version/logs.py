import logging

from rich.logging import RichHandler
from rich.console import Console

FORMAT = "%(message)s"

logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(console=Console(stderr=True), rich_tracebacks=True, markup=True)])

log = logging.getLogger("rich")
