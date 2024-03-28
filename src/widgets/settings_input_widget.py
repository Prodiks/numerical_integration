from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from src.ui.py.settings_input_widget import Ui_Form


class SettingsInputWidget(QWidget):
    value_changed = pyqtSignal(int)

    def __init__(self, parent: QWidget, text: str, max: int, min: int, step: int) -> None:
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(text)
        self.ui.slider.setMaximum(max)
        self.ui.spinbox.setMaximum(max)
        self.ui.slider.setMinimum(min)
        self.ui.spinbox.setMinimum(min)
        self.ui.spinbox.setSingleStep(step)
        self.ui.slider.setSingleStep(step)
        self.ui.slider.valueChanged.connect(self.__on_slider_value_changed)
        self.ui.spinbox.valueChanged.connect(self.__on_spinbox_value_changed)

    def set_value(self, value: int) -> None:
        self.ui.slider.setValue(value)
        self.ui.spinbox.setValue(value)

    def __on_slider_value_changed(self, value: int) -> None:
        self.ui.spinbox.setValue(value)
        self.value_changed.emit(value)

    def __on_spinbox_value_changed(self, value: int) -> None:
        self.ui.slider.setValue(value)
        self.value_changed.emit(value)
