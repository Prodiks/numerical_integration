from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget
from src.ui.py.integral_input_widget import Ui_integral_input_widget


class IntegralInputWidget(QWidget):
    expression_changed = pyqtSignal(str, str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_integral_input_widget()
        self.ui.setupUi(self)
        self.ui.a_edit.editingFinished.connect(self.__expression_changed)
        self.ui.b_edit.editingFinished.connect(self.__expression_changed)
        self.ui.fx_edit.editingFinished.connect(self.__expression_changed)
        self.ui.a_edit.setValidator(QIntValidator())
        self.ui.b_edit.setValidator(QIntValidator())

    def set_value(self, fx: str, a: str, b: str) -> None:
        self.ui.fx_edit.setText(fx)
        self.ui.a_edit.setText(a)
        self.ui.b_edit.setText(b)

    def __expression_changed(self) -> None:
        self.expression_changed.emit(self.ui.fx_edit.text(), self.ui.a_edit.text(), self.ui.b_edit.text())
