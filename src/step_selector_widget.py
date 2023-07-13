from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QRadioButton


class StepSelectorWidget(QWidget):
    button_clicked = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self._group = QButtonGroup()
        # TODO: make more flexible
        for i, name in enumerate(("Как есть", "1h", "3h", "1d", "min/max 1d")):
            button = QRadioButton(name)
            self._layout.addWidget(button)
            self._group.addButton(button, i)
        self._group.idClicked.connect(self.button_clicked.emit)
        self._group.button(0).click()
        self.setLayout(self._layout)

    def _on_button_clicked(self, id_: int) -> None:
        self.button_clicked.emit(id_)
