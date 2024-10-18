import logging
from pathlib import Path

fp = Path(".").absolute() / "pychess_cli" / "loggers" / "game.log"
print(fp)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("{asctime}, {levelname}, {message}", style="{")

file_handler = logging.FileHandler(filename=fp, mode="w", encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
