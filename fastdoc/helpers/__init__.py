import json
import subprocess
import os
from pathlib import Path
from typing import Literal, Optional, Union
from fastdoc.custom_types import ModelInfo, ModelMetaType
from report_writer.types import CaseObjectsType
import models
from fastdoc import config
from report_writer import Renderer
from pprint import pprint
from InquirerPy import inquirer
import importlib
import stringcase
import unidecode
import imp


def get_test_context(model):
    mod = getattr(models, model)
    return mod.test_data.context


def get_models_info(type: Optional[Literal['qt', 'web']] = None) -> list[ModelInfo]:
    mis: list[ModelInfo] = []
    for entry in config.models_folder.iterdir():
        if entry.is_dir() and (entry / "templates").exists():
            mi = ModelInfo(entry.name)
            if type is None or (type == "qt" and mi.meta['has_qt_form']) or (type == "web" and mi.meta['has_web_form']):
                mis.append(mi)
    return mis


def choose_model():
    choices = [mi.name for mi in get_models_info()]
    model = inquirer.select(
        message="Model:",
        choices=choices,
    ).execute()
    return model


def render_doc(model: str, context, file_: Union[Path, str, None] = None):
    path = Path(file_) if file_ is not None else config.app_dir / \
        "compilado.docx"
    md = getattr(models, model)
    r = Renderer(md)
    new_context, file_ = r.render(context, path)
    if config.verbose:
        pprint(new_context)


def open_doc(file_: Union[str, Path]) -> None:
    if os.name == "nt":
        subprocess.Popen(['start', str(file_)], shell=True)


def get_model_meta(model: str) -> dict:
    path = config.models_folder / model / "meta.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def update_model_meta(name: str, data: dict) -> None:
    mi = ModelInfo(name)
    mi.meta.update(data)  # type: ignore
    mi.save_meta()


def fix_imports():
    lines = []
    for mi in get_models_info():
        lines.append(f"from . import {mi.name}")
    text = "\n".join(lines)
    path = config.models_folder / "__init__.py"
    path.write_text(text, encoding="utf-8")
    imp.reload(models)


def get_objects_from_folder(folder: Path, image_extensions=['.jpg', '.png']) -> CaseObjectsType:
    obj = CaseObjectsType(folder=folder)
    obj.pics_not_classified = []
    for entry in folder.iterdir():
        if entry.is_file() and entry.suffix in image_extensions:
            obj.pics_not_classified.append(str(entry.absolute()))
    return obj


def read_workdir_data():
    path = config.workdir / "fastdoc.json"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}


def write_workdir_data(workdir: Union[Path, str], data: Union[dict, list]) -> None:
    workdir = Path(workdir)
    path = workdir / "fastdoc.json"
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))


def init_dir(model, workdir: Union[Path, str]) -> bool:
    workdir = Path(workdir)
    try:
        fmod = importlib.import_module(f"models.{model}.init_dir")
        fmod.init_dir(workdir)
        return True
    except ModuleNotFoundError:
        return False


def model_name_to_folder_name(name: str) -> str:
    return stringcase.snakecase(unidecode.unidecode(name))


def find_model_meta_by_folder(folder: Union[str, Path]) -> ModelMetaType:
    folder = Path(folder)
    with (folder / "meta.json").open("r", encoding="utf-8") as f:
        data: ModelMetaType = json.load(f)
    return data
