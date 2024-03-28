from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from src.ui.py.settings_collection_widget import Ui_Form


class SettingsCollectionWidget(QWidget):
    current_changed = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.combo.currentIndexChanged.connect(self.__current_changed)

    @property
    def current(self) -> int:
        return self.ui.combo.currentIndex()

    def __current_changed(self, new: int) -> None:
        self.ui.stacked_widget.setCurrentIndex(new)
        self.current_changed.emit(new)

    def add_widget(self, widget: QWidget, caption: str) -> None:
        self.ui.combo.addItem(caption, self.ui.combo.count())
        self.ui.stacked_widget.addWidget(widget)
