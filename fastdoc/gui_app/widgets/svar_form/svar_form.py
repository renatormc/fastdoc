from typing import Any, Optional
from fastdoc.gui_app.widgets.scomposite import SComposite
from fastdoc.gui_app.widgets.svar_form.svar_form_item import SVarFormItem
from fastdoc.gui_app.widgets.types import ValidationError
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QComboBox, QHBoxLayout, QSpacerItem
from fastdoc.gui_app.colors import Colors
from .svar_form_item import SVarFormItem


class SVarForm:
    def __init__(self, name: str, choices: list[SVarFormItem], label="", stretch=0) -> None:
        self._name = name
        self._label = label or self.name
        self._stretch = stretch
        self.choices = [c.clone() for c in choices]
        self._current_item: Optional[SVarFormItem] = None
        self.map_choices: dict[str, SVarFormItem] = {}
        self._model_name: Optional[str] = None
        for item in self.choices:
            self.map_choices[item.choice_value] = item
        super(SVarForm, self).__init__()
        


    @property
    def current_item(self) -> SVarFormItem:
        if self._current_item is None:
            raise Exception("get_widget must be executed once before")
        return self._current_item

    @property
    def stretch(self) -> int:
        return self._stretch

    @property
    def label(self) -> str:
        return self._label

    @property
    def name(self) -> str:
        return self._name

    def set_model_name(self, model_name: str) -> None:
        self._model_name = model_name

    def get_model_name(self) -> str:
        if self._model_name is None:
            raise Exception("Model name was not set")
        return self._model_name

    def get_context(self) -> Any:
        data: dict = {
            'choice': self.current_item.choice_value,
            'data': None
        }
        data['data'], error = self.current_item.composite.get_context()
        if error:
            raise ValidationError("Há erros")
        return data

    def get_widget(self) -> QWidget:
        w = QWidget()
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.lay_main = QVBoxLayout()
        w.setLayout(self.lay_main)

        # self.lay_main.addWidget(QLabel(self.label))

        lay_horizontal = QHBoxLayout()
        lay_horizontal.addWidget(QLabel(self.label))
        self.cbx_choice = QComboBox()
        
        self.cbx_choice.addItems(list(self.map_choices.keys()))
        lay_horizontal.addWidget(self.cbx_choice)
        lay_horizontal.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.lay_main.addLayout(lay_horizontal)
       
        for item in self.choices:
            item.composite = SComposite(item.widgets, model_name=self.get_model_name())
            item.composite.setHidden(True)
            self.lay_main.addWidget(item.composite)
        self._current_item = self.choices[0]
        self.current_item.composite.setHidden(False)

        self.cbx_choice.currentTextChanged.connect(self.change_form)
        return w

    def change_form(self):
        if self._current_item is not None:
            self.current_item.composite.setHidden(True)
        choice = self.cbx_choice.currentText()
        if choice:
            self._current_item = self.map_choices[choice]
            self.current_item.composite.setHidden(False)


    def serialize(self) -> Any:
        return {
            'choice': self.current_item.choice_value,
            'data': self.current_item.composite.serialize()
        }
        
    def load(self, data: dict) -> None:
       pass

    def clear_content(self) -> None:
        for item in self.choices:
            item.composite.clear_content()

    def show_error(self, message: str) -> None:
        pass
