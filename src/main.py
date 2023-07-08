import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QTabWidget

from src.pt_scatter_widget import PTScatterWidget


class AboutPage(QWidget):
    def __init__(self, text: str):
        super().__init__()
        layout = QGridLayout(self)
        layout.addWidget(QLabel(f"Hello: {text}"))
        self.setLayout(layout)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QTabWidget()
        self.setCentralWidget(self._main)
        self._main.addTab(PTScatterWidget(), "PT Scatter")
        for text in ("second", "third", "fourth", "fifth"):
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
