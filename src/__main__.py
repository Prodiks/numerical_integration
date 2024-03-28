import sys
import traceback
from types import TracebackType
from typing import Type

from PyQt5.QtWidgets import QApplication

from src.model import Model
from src.widgets.main_widget import MainWidget


def main() -> int:
    qapp = QApplication(sys.argv)
    qapp.setStyle("Fusion")
    font = qapp.font()
    font.setPointSize(10)
    qapp.setFont(font)
    sys.excepthook = excepthook
    model = Model()
    w = MainWidget(model)
    w.show()
    return qapp.exec()


def excepthook(exc_type: Type[BaseException], exc_value: BaseException, exc_tb: TracebackType | None) -> None:
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    QApplication.quit()


if __name__ == '__main__':
    main()
