import numpy as np
import pandas as pd

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

from src.widgets.labeled_combobox import LabeledCombobox


class Boxplot(QWidget):
    def __init__(self, ser: pd.Series, freq: str) -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        gb = ser.groupby(pd.Grouper(freq=freq))
        Y = [np.array(gb.get_group(x)) for x in gb.groups]
        labels = [x.strftime("%d %b") for x in gb.groups]

        canvas = FigureCanvas(Figure())
        self._ax = canvas.figure.subplots()
        self._ax.boxplot(Y, labels=labels, showfliers=False)

        canvas.figure.autofmt_xdate(rotation=70)

        self._layout.addWidget(canvas)


class BoxplotWidget(QWidget):
    def __init__(self, df: pd.DataFrame, freq: str) -> None:
        super().__init__()
        self._df = df
        self._freq = freq
        self._column = self._df.columns[0]

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._build_comboboxes())
        self._plot = Boxplot(self._df[self._column], freq)
        self._layout.addWidget(self._plot)
        self.setLayout(self._layout)

    def _build_comboboxes(self) -> QWidget:
        lc = LabeledCombobox("Column", self._df)
        lc.activated.connect(self._on_combo_activated)
        return lc

    def _on_combo_activated(self, selected: str) -> None:
        self._column = selected
        new_plot = Boxplot(self._df[self._column], self._freq)
        self._layout.replaceWidget(self._plot, new_plot)
        self._plot = new_plot
