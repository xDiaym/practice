import functools
from collections.abc import Sequence

import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout

from src.widgets.labeled_combobox import LabeledCombobox


class ComboGroup(QWidget):
    combo_activated = Signal(str, str)

    def __init__(self, labels: Sequence[str], df: pd.DataFrame) -> None:
        super().__init__()
        self._layout = QHBoxLayout()
        for label in labels:
            combobox = LabeledCombobox(label, df)
            signal = functools.partial(self.combo_activated.emit, label)
            combobox.activated.connect(signal)
            self._layout.addWidget(combobox)
        self.setLayout(self._layout)
