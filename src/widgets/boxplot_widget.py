import numpy as np
import pandas as pd

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


class BoxplotWidget(QWidget):
    def __init__(self, df: pd.DataFrame, *, freq: str = "d") -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        gb = df.BME280_temp.groupby(pd.Grouper(freq=freq))
        Y = [np.array(gb.get_group(x)) for x in gb.groups]
        labels = [x.strftime("%d %b") for x in gb.groups]

        canvas = FigureCanvas(Figure())
        self._ax = canvas.figure.subplots()
        self._ax.boxplot(Y, labels=labels, showfliers=False)

        canvas.figure.autofmt_xdate(rotation=70)

        self._layout.addWidget(canvas)
