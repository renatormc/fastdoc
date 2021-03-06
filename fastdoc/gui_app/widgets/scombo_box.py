from typing import Any, Optional
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from fastdoc.custom_types import ConverterType, FormError
from fastdoc.gui_app.widgets.helpers import apply_converter
from fastdoc.gui_app.widgets.label_error import LabelError
from fastdoc.gui_app.widgets.helpers import get_list


class SComboBox:

    def __init__(self, name: str, label="", choices: list[str]|str=[], stretch=0, default="", converter: Optional[ConverterType] = None):
        self._name = name
        self.choices = choices
        self._label = label or self.name
        self._stretch = stretch
        self.default = default
        self.converter = converter
        super(SComboBox, self).__init__()
        self._combo: Optional[QComboBox] = None
        self._lbl_error: Optional[LabelError] = None
        self._model_name: Optional[str] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def combo(self) -> QComboBox:
        if self._combo is None:
            raise Exception("get_widget must be executed once before")
        return self._combo

    @property
    def lbl_error(self) -> LabelError:
        if not self._lbl_error:
            raise Exception("get_widget must be executed once before")
        return self._lbl_error

    @property
    def name(self) -> str:
        return self._name

    @property
    def label(self) -> str:
        return self._label

    def set_model_name(self, model_name: str) -> None:
        self._model_name = model_name

    def get_model_name(self) -> str:
        if self._model_name is None:
            raise Exception("Model name was not set")
        return self._model_name

    def get_context(self) -> Any:
        data = self.combo.currentData()
        if self.converter is not None:
            data = apply_converter(data, self.converter)
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        l.addWidget(QLabel(self.label))
        self._combo = QComboBox()
        for item in get_list(self.choices, self.get_model_name()):
            self.combo.addItem(item["key"], item["data"])
        l.addWidget(self.combo)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w


    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        return self.get_context()

    def load(self, value: Any) -> None:
        self.combo.setCurrentText(value)

    def clear_content(self)-> None:
        if self.default != "":
            self.combo.setCurrentText(self.default)
