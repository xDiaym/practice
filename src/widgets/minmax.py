import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

from src.widgets.combo_group import ComboGroup
from src.widgets.labeled_combobox import LabeledCombobox


def aggregate(x: pd.Series, freq="12h"):
    sample = x.resample(freq)
    return sample.min(), sample.mean(), sample.max()


class MinMaxPlot(QWidget):
    def __init__(self, series: pd.Series, *, freq: str = "12h") -> None:
        super().__init__()

        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        canvas = FigureCanvas(Figure())
        self._ax = canvas.figure.subplots()

        df_min, df_mean, df_max = aggregate(series, freq)

        self._ax.fill_between(df_mean.index, df_min, df_max, alpha=0.5)
        self._ax.plot(df_mean, c="orange")

        canvas.figure.autofmt_xdate(rotation=70)

        self._layout.addWidget(canvas)


class MinMaxWidget(QWidget):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self._df = df
        self._column = self._df.columns[0]

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._build_comboboxes())
        self._plot = MinMaxPlot(self._df[self._column])
        self._layout.addWidget(self._plot)
        self.setLayout(self._layout)

    def _build_comboboxes(self) -> QWidget:
        lc = LabeledCombobox("Column", self._df)
        lc.activated.connect(self._on_combo_activated)
        return lc

    def _on_combo_activated(self, selected: str) -> None:
        self._column = selected
        new_plot = MinMaxPlot(self._df[self._column])
        self._layout.replaceWidget(self._plot, new_plot)
        self._plot = new_plot
