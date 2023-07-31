from bisect import bisect

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QLabel,
)
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.colors import Normalize
from matplotlib.figure import Figure

from src.widgets.combo_group import ComboGroup
from src.widgets.labeled_combobox import LabeledCombobox

HEAT_PERCEPTION = {
    -30: "Крайне холодно",
    -24: "Крайне холодно",
    -12: "Очень холодно",
    0: "Холодно",
    12: "Умеренно тепло",
    18: "Тепло",
    24: "Жарко",
    30: "Очень жарко",
}
_HP_VALUES = list(HEAT_PERCEPTION)
_HP_LABELS = list(HEAT_PERCEPTION.values())


def convert_labels(x: int) -> int:
    return bisect(_HP_VALUES, x)


def effective_temperature(t: np.ndarray, h: np.ndarray) -> np.ndarray:
    return t - 0.4 * (t - 10) * (1 - h / 100)


class HeatPerceptionPlot(QWidget):
    def __init__(self, t: pd.DataFrame, h: pd.DataFrame) -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        self._canvas = FigureCanvas(Figure())
        ax1, ax2 = self._canvas.figure.subplots(2, 1)
        self._canvas.figure.autofmt_xdate(rotation=70)

        eff = effective_temperature(t, h)

        ax1.plot(t, label="temperature")
        ax1.plot(eff, label="effective temperature")

        x = [convert_labels(x) for x in eff]
        colormap = plt.get_cmap("turbo")
        rescale = Normalize(np.min(_HP_VALUES), np.max(_HP_VALUES))

        ax2.bar(
            eff.index,
            x,
            width=25 / len(x),
            label="heat perception",
            color=colormap(rescale(eff)),
        )
        ax2.yaxis.tick_right()
        ax2.set_ylabel("Heat perception")
        ax2.set_yticks(ticks=np.arange(len(_HP_VALUES)), labels=_HP_LABELS)
        self._canvas.figure.legend()

        self._layout.addWidget(self._canvas)


class HeatPerceptionWidget(QWidget):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self._df = df
        self._temp, self._hum = self._df.columns[:2]

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._build_comboboxes())
        self._plot = HeatPerceptionPlot(
            self._df[self._temp], self._df[self._hum]
        )
        self._layout.addWidget(self._plot)
        self.setLayout(self._layout)

    def _build_comboboxes(self) -> QWidget:
        cg = ComboGroup(("Temperature", "Humidity"), self._df)
        cg.combo_activated.connect(self._on_combo_activated)
        return cg

    def _on_combo_activated(self, label: str, selected: str) -> None:
        if label == "Temperature":
            self._temp = selected
        elif label == "Humidity":
            self._hum = selected
        new_plot = HeatPerceptionPlot(self._df[self._temp], self._df[self._hum])
        self._layout.replaceWidget(self._plot, new_plot)
        self._plot = new_plot
