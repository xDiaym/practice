import pandas as pd

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

from src.widgets.combo_group import ComboGroup


class PTScatterPlot(QWidget):
    def __init__(self, p: pd.DataFrame, t: pd.DataFrame) -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        static_canvas = FigureCanvas(Figure())
        self._ax = static_canvas.figure.subplots()

        self._ax.set_title("PT diagram")

        smap = self._ax.scatter(p, t, 0.12, c=mdates.date2num(p.index))

        cb = static_canvas.figure.colorbar(smap, orientation="vertical")
        loc = mdates.AutoDateLocator()
        cb.ax.yaxis.set_major_locator(loc)
        cb.ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

        self._layout.addWidget(static_canvas)


class PTScatterWidget(QWidget):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self._df = df
        self._p, self._t = self._df.columns[:2]

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._build_comboboxes())
        self._plot = PTScatterPlot(self._df[self._p], self._df[self._t])
        self._layout.addWidget(self._plot)
        self.setLayout(self._layout)

    def _build_comboboxes(self) -> QWidget:
        cg = ComboGroup(("P", "T"), self._df)
        cg.combo_activated.connect(self._on_combo_activated)
        return cg

    def _on_combo_activated(self, label: str, selected: str) -> None:
        if label == "P":
            self._p = selected
        elif label == "T":
            self._t = selected
        new_plot = PTScatterPlot(self._df[self._p], self._df[self._t])
        self._layout.replaceWidget(self._plot, new_plot)
        self._plot = new_plot
