import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


def aggregate(x: pd.Series, freq="12h"):
    sample = x.resample(freq)
    return sample.min(), sample.mean(), sample.max()


class MinMaxWidget(QWidget):
    def __init__(
        self, label: str, series: pd.Series, *, freq: str = "12h"
    ) -> None:
        super().__init__()

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        canvas = FigureCanvas(Figure())
        self._ax = canvas.figure.subplots()

        df_min, df_mean, df_max = aggregate(series, freq)

        self._ax.fill_between(df_mean.index, df_min, df_max, alpha=0.5)
        self._ax.plot(df_mean, c="orange")
        self._ax.set_ylabel(label)

        canvas.figure.autofmt_xdate(rotation=70)

        self._layout.addWidget(canvas)
