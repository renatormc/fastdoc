import argparse
import shutil
import os
from pathlib import Path
import subprocess

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True, help='Command to be used')

p_prepare = subparsers.add_parser("prepare")
p_prepare.add_argument("direction", choices=("up", "down"), help="Direction up or down")

p_dist = subparsers.add_parser("dist")

args = parser.parse_args()

if args.command == "prepare":
    if args.direction == "up":
        shutil.rmtree(app_dir / "fastdoc/models_example")
        shutil.copytree(app_dir / "models", app_dir / "fastdoc/models_example")
    elif args.direction == "down":
        shutil.rmtree(app_dir / "models")
        shutil.copytree(app_dir / "fastdoc/models_example", app_dir / "models")
elif args.command == "dist":
    path_to = app_dir / "dist"
    itens = ['models', 'fastdoc', 'main.py', 'requirements.txt']
    try:
        shutil.rmtree(path_to)
    except FileNotFoundError:
        pass
    shutil.copytree(app_dir / "dist_start", path_to)
    for item in itens:
        path = app_dir / item
        if path.is_dir():
            shutil.copytree(path, path_to / item)
        else:
            shutil.copy(path, path_to / item)
   
    path_from = "D:\\portable\\python\\Python3.10.0"
    shutil.copytree(path_from, path_to / "Python")

    python = app_dir / "dist/Python/python.exe"
    subprocess.run([str(python), '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(app_dir / "requirements.txt")])