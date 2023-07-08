import sys
from pathlib import Path

import pandas as pd
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QTabWidget

from src.minmax_widget import MinMaxWidget
from src.pt_scatter_widget import PTScatterWidget


class AboutPage(QWidget):
    def __init__(self, text: str):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel(f"Hello: {text}"))
        self.setLayout(layout)


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_json(path)
    df.date = pd.to_datetime(df.date, format="%Y-%m-%d %H:%M:%S")
    df.set_index("date", inplace=True)
    return df


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QTabWidget()
        self.setCentralWidget(self._main)

        df = load_dataset("../datasets/Hydra-L.json")

        self._main.addTab(PTScatterWidget(df), "PT Scatter")
        self._main.addTab(
            MinMaxWidget("Temperature ($^\circ$C)", df.BME280_temp), "MinMax"
        )
        for text in ("third", "fourth", "fifth"):
            self._main.addTab(AboutPage(text), text.capitalize())


if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
