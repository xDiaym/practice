from enum import IntEnum, auto

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QRadioButton


class Step(IntEnum):
    AS_IS = auto(value=0)
    ONE_H = auto()
    THREE_H = auto()
    ONE_D = auto()

    def __str__(self) -> str:
        match self:
            case Step.AS_IS:
                return "Как есть"
            case Step.ONE_H:
                return "1h"
            case Step.THREE_H:
                return "3h"
            case Step.ONE_D:
                return "1d"
            case _:
                assert False, "Invalid enum state"


class StepSelectorWidget(QWidget):
    button_clicked = Signal(Step)

    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self._group = QButtonGroup()
        # TODO: make more flexible
        for step in Step:
            button = QRadioButton(str(step))
            self._layout.addWidget(button)
            self._group.addButton(button, step.value)
        self._group.idClicked.connect(
            lambda id_: self.button_clicked.emit(Step(id_))
        )
        self._group.button(min(Step)).click()
        self.setLayout(self._layout)

    def _on_button_clicked(self, id_: int) -> None:
        self.button_clicked.emit(Step(id_))
