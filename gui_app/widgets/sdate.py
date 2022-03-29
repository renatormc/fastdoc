from typing import Any, Optional
from gui_app.widgets.validation_error import ValidationError

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from datetime import datetime
from custom_types import ValidatorType
from gui_app.widgets.label_error import LabelError


class SDate:

    def __init__(self, name: str, required=False, label="", placeholder="", validators: list[ValidatorType] = [], stretch=0) -> None:
        self.required = required
        self.placeholder = placeholder
        self._name = name
        self._label = label or self.name
        self.validators = validators
        self._stretch = stretch
        super(SDate, self).__init__()
        self._led: Optional[QLineEdit] = None
        self._lbl_error: Optional[LabelError] = None

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def led(self) -> QLineEdit:
        if not self._led:
            raise Exception("get_widget must be executed once before")
        return self._led

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

    def get_context(self) -> Any:
        return datetime.strptime(self.led.displayText(), "%d/%m/%Y")

    def get_widget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        l.addWidget(QLabel(self.label))
        self._led = QLineEdit()
        self.led.setPlaceholderText(self.placeholder)
        l.addWidget(self.led)
        self._lbl_error = LabelError()
        l.addWidget(self._lbl_error)
        return w

    def validate(self):
        try:
            value = datetime.strptime(self.led.displayText(), "%d/%m/%Y")
        except:
            raise ValidationError('Data inválida')
        for v in self.validators:
            v(value)


    def show_error(self, message: str) -> None:
        self.lbl_error.setText(message)

    def serialize(self) -> Any:
        return self.led.displayText()

    def load(self, value: Any) -> None:
        self.led.setText(value)
