import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """Configure a consistent logging format across the app.
    Replaces scattered print() statements used for pipeline progress.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )
