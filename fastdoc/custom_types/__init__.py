from typing import Any, Callable, Optional, TypedDict

from fastdoc import config
import json

FormError = dict[str, str]

ValidatorType = Callable[[Any], None]
ConverterType = Callable[[Any], Any]

class ModelMetaType(TypedDict):
    full_name: str
    has_qt_form: bool
    has_web_form: bool

default_meta: ModelMetaType = {
    'full_name': 'Sem nome',
    'has_qt_form': False, 
    'has_web_form': False
}


class ModelInfo:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.meta: ModelMetaType =  {
            'full_name': '',
            'has_qt_form': False,
            'has_web_form': False
        }
        self._load_meta()

    def _load_meta(self):
        path = config.models_folder / self.name / "meta.json"
        with path.open("r", encoding="utf-8") as f:
            self.meta = json.load(f)
        missing = False
        for key, value in default_meta.items():
            try:
                self.meta[key]
            except KeyError:
                missing = True
                self.meta[key] = value
        if missing:
            self.save_meta()


    def save_meta(self):
        path = config.models_folder / self.name / "meta.json"
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(self.meta, ensure_ascii=False, indent=4))

    
