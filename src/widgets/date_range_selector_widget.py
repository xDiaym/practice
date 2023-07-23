from datetime import datetime

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QDateTimeEdit


class DataRangeSelectorWidget(QWidget):
    FORMAT = "dd.MM.yyyy hh:mm:ss"

    date_changed = Signal(datetime, datetime)

    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout()
        self._low, self._high = QDateTimeEdit(), QDateTimeEdit()
        self._low.setDisplayFormat(self.FORMAT)
        self._high.setDisplayFormat(self.FORMAT)
        self._layout.addWidget(self._low)
        self._layout.addWidget(self._high)
        self._low.dateTimeChanged.connect(self._date_changed)
        self._high.dateTimeChanged.connect(self._date_changed)
        self.setLayout(self._layout)

    def set_range(self, low: datetime, high: datetime) -> None:
        self._low.setDateTimeRange(low, high)
        self._low.setDateTime(low)
        self._high.setDateTimeRange(low, high)
        self._high.setDateTime(high)

    def _date_changed(self) -> None:
        self.date_changed.emit(self._low.dateTime(), self._high.dateTime())
