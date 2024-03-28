from typing import Callable, Any

import matplotlib
from PyQt5.QtWidgets import QWidget
import numpy as np
from matplotlib.patches import Rectangle

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt


class PlotWidget(FigureCanvasQTAgg):
    def __init__(self, parent: QWidget | None = None, width: int = 5, height: int = 4, dpi: int = 100):
        self.figure, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def clear(self) -> None:
        self.ax.clear()

    def add_func(self, f: Callable[[Any], float], a: float, b: float):
        x = np.linspace(a, b, 1000)
        y = f(x)
        self.ax.plot(x, y)

    def add_rect(self, x: float, y: float, width: float, height: float) -> None:
        self.ax.add_patch(Rectangle((x, y), width, height, fill=False, alpha=0.5, color="grey"))

    def add_trapezoid(self, x: float, y: float, width: float, height: float, delta: float) -> None:
        self.ax.plot([x, x, x+width, x+width, x], [y, y+height, y+height+delta, y, y], alpha=0.5, color="grey")

    def add_point(self, x: float, y: float) -> None:
        self.ax.scatter(x, y)
