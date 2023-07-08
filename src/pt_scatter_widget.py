from pathlib import Path

import pandas as pd

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_json(path)
    df.date = pd.to_datetime(df.date, format="%Y-%m-%d %H:%M:%S")
    df.set_index("date", inplace=True)
    return df


class PTScatterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        df = load_dataset("../datasets/Hydra-L.json")
        df_mean = df.resample("5min").mean()

        static_canvas = FigureCanvas(Figure())
        self._ax = static_canvas.figure.subplots()

        self._ax.set_xlabel(r"Temperature ($^\circ$C)")
        self._ax.set_ylabel(r"Pressure (mm Hg)")
        self._ax.set_title("PT diagram for Mytishchi(HydraL)")

        smap = self._ax.scatter(
            df_mean.BME280_temp,
            df_mean.BME280_pressure,
            0.12,
            c=mdates.date2num(df_mean.index),
        )

        cb = static_canvas.figure.colorbar(smap, orientation="vertical")
        loc = mdates.AutoDateLocator()
        cb.ax.yaxis.set_major_locator(loc)
        cb.ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

        self._layout.addWidget(static_canvas)
