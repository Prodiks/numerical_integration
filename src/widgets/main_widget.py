from enum import IntEnum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QMessageBox

from src.model import Model
from src.ui.py.main_widget import Ui_main_widget
from src.widgets.integral_input_widget import IntegralInputWidget
from src.widgets.integral_result_widget import IntegralResultWidget
from src.widgets.plot_widget import PlotWidget
from src.widgets.settings_collection_widget import SettingsCollectionWidget
from src.widgets.settings_input_widget import SettingsInputWidget


class Methods(IntEnum):
    LEFT_RECTS = 0
    RIGHTS_RECTS = 1
    MIDDLE_RECTS = 2
    TRAPEZOIDS = 3
    MONTE_CARLO = 4


class MainWidget(QWidget):
    def __init__(self, model: Model) -> None:
        super().__init__(None)
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)

        self.__model = model

        self.__plot_widget = PlotWidget(self)
        self.__integral_input_widget = IntegralInputWidget(self)
        self.ui.layout.addWidget(self.__plot_widget, 0, 0, 3, 1)
        self.ui.layout.setColumnStretch(1, 2)
        self.ui.layout.addWidget(self.__integral_input_widget, 0, 1, 1, 1)
        self.__integral_input_widget.expression_changed.connect(self.__integral_expression_changed)
        self.__integral_input_widget.set_value(self.__model.fx_str, str(self.__model.a), str(self.__model.b))

        self.__settings_collection_widget = SettingsCollectionWidget(self)
        self.__left_rect_input_widget = SettingsInputWidget(self, "Количество прямоугольников",
                                                            self.__model.MAX_FIGURES, self.__model.MIN_FIGURES,
                                                            self.__model.DELTA_FIGURES)
        self.__right_rect_input_widget = SettingsInputWidget(self, "Количество прямоугольников",
                                                             self.__model.MAX_FIGURES, self.__model.MIN_FIGURES,
                                                             self.__model.DELTA_FIGURES)
        self.__middle_rect_input_widget = SettingsInputWidget(self, "Количество прямоугольников",
                                                              self.__model.MAX_FIGURES, self.__model.MIN_FIGURES,
                                                              self.__model.DELTA_FIGURES)
        self.__trapezoid_input_widget = SettingsInputWidget(self, "Количество трапеций", self.__model.MAX_FIGURES,
                                                            self.__model.MIN_FIGURES, self.__model.DELTA_FIGURES)
        self.__point_input_widget = SettingsInputWidget(self, "Количество точек", self.__model.MAX_POINTS,
                                                        self.__model.MIN_POINTS, self.__model.DELTA_POINTS)

        self.__left_rect_input_widget.set_value(self.__model.left_rect_count)
        self.__right_rect_input_widget.set_value(self.__model.right_rect_count)
        self.__middle_rect_input_widget.set_value(self.__model.middle_rect_count)
        self.__trapezoid_input_widget.set_value(self.__model.trapezoid_count)
        self.__point_input_widget.set_value(self.__model.point_count)

        self.__settings_collection_widget.add_widget(self.__left_rect_input_widget, "Метод левых прямоугольников")
        self.__settings_collection_widget.add_widget(self.__right_rect_input_widget, "Метод правых прямоугольников")
        self.__settings_collection_widget.add_widget(self.__middle_rect_input_widget,
                                                     "Метод центральных прямоугольников")
        self.__settings_collection_widget.add_widget(self.__trapezoid_input_widget, "Метод трапеций")
        self.__settings_collection_widget.add_widget(self.__point_input_widget, "Метод Монте-Карло")
        self.ui.layout.addWidget(self.__settings_collection_widget, 1, 1, 1, 1)
        self.__integral_edit = IntegralResultWidget(self)
        self.ui.layout.addWidget(self.__integral_edit, 2, 1, 1, 1)

        self.__left_rect_input_widget.value_changed.connect(self.__left_rect_count_changed)
        self.__right_rect_input_widget.value_changed.connect(self.__right_rect_count_changed)
        self.__middle_rect_input_widget.value_changed.connect(self.__middle_rect_count_changed)
        self.__trapezoid_input_widget.value_changed.connect(self.__trapezoid_rect_count_changed)
        self.__point_input_widget.value_changed.connect(self.__point_count_changed)
        self.__settings_collection_widget.current_changed.connect(self.__current_changed)

        self.__redraw_current()

    def __current_changed(self, _: int) -> None:
        self.__redraw_current()

    def __left_rect_count_changed(self, count: int) -> None:
        self.__model.left_rect_count = count
        self.__redraw_current()

    def __right_rect_count_changed(self, count: int) -> None:
        self.__model.right_rect_count = count
        self.__redraw_current()

    def __middle_rect_count_changed(self, count: int) -> None:
        self.__model.middle_rect_count = count
        self.__redraw_current()

    def __trapezoid_rect_count_changed(self, count: int) -> None:
        self.__model.trapezoid_count = count
        self.__redraw_current()

    def __point_count_changed(self, count: int) -> None:
        self.__model.point_count = count
        self.__redraw_current()

    def __integral_expression_changed(self, fx: str, a: str, b: str) -> None:
        if self.__model.fx_str == fx.replace(' ', '') and self.__model.a == int(a) and self.__model.b == int(b):
            return
        try:
            self.__model.fx = fx
        except SyntaxError as ex:
            # QMessageBox.critical(self, 'Ошибка', 'Некорректная функция')
            self.__integral_input_widget.set_value(self.__model.fx_str, str(self.__model.a), str(self.__model.b))
        else:
            self.__model.a = a
            self.__model.b = b
            self.__redraw_current()

    def __redraw_current(self) -> None:
        match self.__settings_collection_widget.current:
            case Methods.LEFT_RECTS:
                self.__redraw_left_rect_plot()
                self.__integral_edit.set_value(f'Результат интегрирования методом левых прямоугольников = '
                                               f'{self.__model.integrate_left_rects()}')
            case Methods.RIGHTS_RECTS:
                self.__redraw_right_rect_plot()
                self.__integral_edit.set_value(f'Результат интегрирования методом правых прямоугольников = '
                                               f'{self.__model.integrate_right_rects()}')
            case Methods.MIDDLE_RECTS:
                self.__redraw_middle_rect_plot()
                self.__integral_edit.set_value(f'Результат интегрирования методом центральных прямоугольников = '
                                               f'{self.__model.integrate_middle_rects()}')
            case Methods.TRAPEZOIDS:
                self.__redraw_trapezoid_plot()
                self.__integral_edit.set_value(f'Результат интегрирования методом трапеций = '
                                               f'{self.__model.integrate_trapezoids()}')
            case Methods.MONTE_CARLO:
                self.__redraw_monte_carlo()
                positive_points, negative_points, out_points, integral = self.__model.integrate_monte_carlo()
                self.__integral_edit.set_value(f'Результат интегрирования методом Монте-Карло = {integral}\n'
                                               f'Точек принадлежащих функции = {positive_points + negative_points}\n'
                                               f'Из них {positive_points} выше оси OX\n'
                                               f'Точек не принадлежащих функции = {out_points}')
            case _:
                raise ValueError

    def __redraw_left_rect_plot(self) -> None:
        self.__plot_widget.clear()
        self.__plot_widget.add_func(self.__model.fx, self.__model.a, self.__model.b)
        for r in self.__model.left_rects():
            self.__plot_widget.add_rect(*r)
        self.__plot_widget.draw()

    def __redraw_right_rect_plot(self) -> None:
        self.__plot_widget.clear()
        self.__plot_widget.add_func(self.__model.fx, self.__model.a, self.__model.b)
        for r in self.__model.right_rects():
            self.__plot_widget.add_rect(*r)
        self.__plot_widget.draw()

    def __redraw_middle_rect_plot(self) -> None:
        self.__plot_widget.clear()
        self.__plot_widget.add_func(self.__model.fx, self.__model.a, self.__model.b)
        for r in self.__model.middle_rects():
            self.__plot_widget.add_rect(*r)
        self.__plot_widget.draw()

    def __redraw_trapezoid_plot(self) -> None:
        self.__plot_widget.clear()
        self.__plot_widget.add_func(self.__model.fx, self.__model.a, self.__model.b)
        for r in self.__model.trapezoids():
            self.__plot_widget.add_trapezoid(*r)
        self.__plot_widget.draw()

    def __redraw_monte_carlo(self) -> None:
        self.__plot_widget.clear()
        self.__plot_widget.add_func(self.__model.fx, self.__model.a, self.__model.b)
        self.__model.generate_points()
        for p in self.__model.points():
            self.__plot_widget.add_point(*p)
        self.__plot_widget.draw()
