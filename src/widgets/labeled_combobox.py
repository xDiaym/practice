import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QLabel


class LabeledCombobox(QWidget):
    activated = Signal(str)

    def __init__(self, label: str, items: pd.DataFrame) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        combo = QComboBox()
        combo.addItems(items)
        combo.textActivated.connect(self.activated)
        self._layout.addWidget(QLabel(label))
        self._layout.addWidget(combo)
        self.setLayout(self._layout)
