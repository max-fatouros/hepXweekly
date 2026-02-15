from pathlib import Path

path = Path(__file__)
while not Path.is_dir(path / 'hep_ex_weekly' ):
    path = path.parent

PROJECT_ROOT = path

UTIL_DIR = Path(__file__).parent

LOG_DIR = PROJECT_ROOT / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)