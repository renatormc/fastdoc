import os
import sys
from pathlib import Path
import json
import tempfile
import shutil
from typing import Optional

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
main_script_dir = app_dir.parent
models_folder = app_dir.parent / "models"
models_example_folder = app_dir / "models_example"
# local_folder = app_dir.parent / ".local"
debug=False
# try:
#     local_folder.mkdir()
# except FileExistsError:
#     pass
workdir: Path = Path(".").absolute()
verbose = False
SECRET_KEY="!@#QWEsddda"

local_data_path = main_script_dir / "local_data.json"
try:
    with local_data_path.open("r", encoding="utf-8") as f:
        local_data = json.load(f)
except FileNotFoundError:
    local_data = {}

DATABASE_URI = f"sqlite:///{main_script_dir / 'db.db'}"

TEMPFOLDER = Path(tempfile.gettempdir(), "fastdoc")
if not TEMPFOLDER.exists():
    TEMPFOLDER.mkdir()

SELF_CONTAINED: bool = "extras\\Python\\python.exe" in sys.executable or "extras\\Python\\pythonw.exe" in sys.executable

vscode_exe: Optional[Path] = None

if SELF_CONTAINED:
    pass
else:
    aux = shutil.which("code")
    vscode_exe = Path(aux) if aux else None

def find_file_manager():
    if os.name == "nt":
        return shutil.which("explorer")
    candidates = ['nautilus', 'dolphin', 'nemo', 'nautilus']
    for c in candidates:
        aux = shutil.which(c)
        if aux:
            return aux
      

file_manager = find_file_manager()


APP_USER_FOLDER = Path.home() / ".fastdoc"
if not APP_USER_FOLDER.exists():
    APP_USER_FOLDER.mkdir()
PREFERENCES_PATH = APP_USER_FOLDER / "preferences.json"

