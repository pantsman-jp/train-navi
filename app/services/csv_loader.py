from csv import reader
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def get_data(fname):
    file_path = DATA_DIR / fname
    with open(file_path, mode="r", encoding="utf-8", newline="") as f:
        return [row for row in reader(f)]
