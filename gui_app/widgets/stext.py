from typing import Any, Optional
from gui_app.widgets.helpers import apply_converter
from gui_app.widgets.validation_error import ValidationError

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from custom_types import ConverterType, ValidatorType
from gui_app.widgets.label_error import LabelError


class SText:

    def __init__(
            self, name: str, required=False, label="",
            placeholder="", validators: list[ValidatorType] = [],
            stretch=0, default="", converter: Optional[ConverterType] = None) -> None:
        self.required = required
        self.placeholder = placeholder
        self._name = name
        self.validators = validators
        self._label = label or self.name
        self._stretch = stretch
        self.default = default
        self.converter = converter
        super(SText, self).__init__()
        self._w: Optional[QLineEdit] = None
        self._lbl_error: Optional[LabelError] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def w(self) -> QLineEdit:
        if not self._w:
            raise Exception("get_widget must be executed once before")
        return self._w

    @property
    def lbl_error(self) -> LabelError:
        if not self._lbl_error:
            raise Exception("get_widget must be executed once before")
        return self._lbl_error

    @property
    def label(self) -> str:
        return self._label

    @property
    def name(self) -> str:
        return self._name

    def get_context(self) -> Any:
        data = self.w.displayText().strip()
        if self.required and data == "":
            raise ValidationError('O valor não pode ser vazio')
        if self.converter is not None:
            data =  apply_converter(data, self.converter)
        for v in self.validators:
            v(data)
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        l.setSpacing(0)
        w.setLayout(l)
        l.addWidget(QLabel(self.label))
        self._w = QLineEdit()
        self._w.setPlaceholderText(self.placeholder)
        l.addWidget(self._w)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w

    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        return self.w.displayText()

    def load(self, value: Any) -> None:
        self.w.setText(value)

    def clear_content(self) -> None:
        self.w.setText(self.default)
