import sys
from pathlib import Path

import pandas as pd
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QMenuBar,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from src.widgets import (
    BoxplotWidget,
    DataRangeSelectorWidget,
    HeatPerceptionWidget,
    PTScatterPlot,
    StepSelectorWidget,
)
from src.widgets.minmax import MinMaxWidget
from src.widgets.pt_scatter import PTScatterWidget


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_json(path)
    df.date = pd.to_datetime(df.date, format="%Y-%m-%d %H:%M:%S")
    df.set_index("date", inplace=True)
    return df


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._main = QHBoxLayout()

        df = load_dataset("../datasets/Hydra-L.json")

        w, lay = QWidget(), QVBoxLayout()
        sel = StepSelectorWidget()
        sel.button_clicked.connect(print)
        lay.addWidget(sel)

        r = DataRangeSelectorWidget()

        r.set_range(df.index.min(), df.index.max())
        lay.addWidget(r)
        w.setLayout(lay)
        self._main.addWidget(w)

        tab = QTabWidget()

        mean_df = df.resample("12h").mean()
        tab.addTab(PTScatterWidget(df), "PT Scatter")
        tab.addTab(
            MinMaxWidget(df),
            "MinMax",
        )
        tab.addTab(BoxplotWidget(df, "12h"), "Boxplot")
        tab.addTab(
            HeatPerceptionWidget(mean_df),
            "Heat perception",
        )
        self._main.addWidget(tab)
        self.setLayout(self._main)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(MainWidget())
        self.setMenuBar(QMenuBar())


if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
