from PyQt5.QtWidgets import QWidget
from src.ui.py.integral_result_widget import Ui_Form


class IntegralResultWidget(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.textEdit.setReadOnly(True)

    def set_value(self, value: str) -> None:
        self.ui.textEdit.setText(value)