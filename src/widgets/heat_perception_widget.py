from bisect import bisect

import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.colors import Normalize
from matplotlib.figure import Figure

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


class HeatPerceptionWidget(QWidget):
    def __init__(self, t: np.ndarray, h: np.ndarray) -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        canvas = FigureCanvas(Figure())
        ax1, ax2 = canvas.figure.subplots(2, 1)
        canvas.figure.autofmt_xdate(rotation=70)

        eff = effective_temperature(t, h)

        ax1.plot(t, label="temperature")
        ax1.plot(eff, label="effective temperature")
        ax1.set_ylabel(r"Temperature ($^\circ$C)")

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
        canvas.figure.legend()

        self._layout.addWidget(canvas)
