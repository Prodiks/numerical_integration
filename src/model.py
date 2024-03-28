import random
from typing import Callable, Tuple, Iterable, List
import numpy as np


class Model:
    MAX_FIGURES = 100
    MAX_POINTS = 200
    MIN_FIGURES = 2
    MIN_POINTS = 20
    DELTA_FIGURES = 1
    DELTA_POINTS = 10
    DEFAULT_A = -5
    DEFAULT_B = 5
    DEFAULT_FIGURE_COUNT = 10
    DEFAULT_POINT_COUNT = 10

    def __init__(self) -> None:
        self.__fx_str = 'x**2'
        self.__points: List[Tuple[float, float]] = []
        self.fx = self.__fx_str
        self.__a = self.DEFAULT_A
        self.__b = self.DEFAULT_B
        self.__left_rect_count = self.DEFAULT_FIGURE_COUNT
        self.__right_rect_count = self.DEFAULT_FIGURE_COUNT
        self.__middle_rect_count = self.DEFAULT_FIGURE_COUNT
        self.__trapezoid_count = self.DEFAULT_FIGURE_COUNT
        self.__point_count = self.DEFAULT_POINT_COUNT

    @property
    def fx(self) -> Callable[[float], float]:
        return self.__fx

    def minmax(self) -> Tuple[float, float]:
        min = self.__fx(self.__a)
        max = min
        i = self.__a + self.eps
        while i <= self.__b:
            curr_y = self.__fx(i)
            if curr_y > max:
                max = curr_y
            elif curr_y < min:
                min = curr_y
            i += self.eps
        return max, min

    @property
    def eps(self) -> float:
        return (self.__b - self.__a) / 100

    @fx.setter
    def fx(self, value: str) -> None:
        tmp = lambda x: eval(value, {'__builtins__': None, 'x': np.array(x)}, np.__dict__)
        tmp(1)
        self.__fx = tmp
        self.__fx_str = value.replace(' ', '')

    @property
    def fx_str(self) -> str:
        return self.__fx_str

    @property
    def a(self) -> int:
        return self.__a

    @a.setter
    def a(self, a: str) -> None:
        self.__a = int(a)

    @property
    def b(self) -> int:
        return self.__b

    @b.setter
    def b(self, b: str) -> None:
        self.__b = int(b)

    @property
    def left_rect_count(self) -> int:
        return self.__left_rect_count

    @left_rect_count.setter
    def left_rect_count(self, count: str) -> None:
        self.__left_rect_count = int(count)

    @property
    def right_rect_count(self) -> int:
        return self.__right_rect_count

    @right_rect_count.setter
    def right_rect_count(self, count: str) -> None:
        self.__right_rect_count = int(count)

    @property
    def middle_rect_count(self) -> int:
        return self.__middle_rect_count

    @middle_rect_count.setter
    def middle_rect_count(self, count: str) -> None:
        self.__middle_rect_count = int(count)

    @property
    def trapezoid_count(self) -> int:
        return self.__middle_rect_count

    @trapezoid_count.setter
    def trapezoid_count(self, count: str) -> None:
        self.__trapezoid_count = int(count)

    @property
    def point_count(self) -> int:
        return self.__point_count

    @point_count.setter
    def point_count(self, point_count: str) -> None:
        self.__point_count = int(point_count)

    def left_rects(self) -> Iterable[Tuple[float, float, float, float]]:
        delta = (self.__b - self.__a) / self.__left_rect_count
        i = self.__a
        while i < self.__b:
            yield i, 0, delta, self.__fx(i)
            i += delta

    def right_rects(self) -> Iterable[Tuple[float, float, float, float]]:
        delta = (self.__b - self.__a) / self.__right_rect_count
        i = self.__a
        while i < self.__b:
            yield i, 0, delta, self.__fx(i+delta)
            i += delta

    def middle_rects(self) -> Iterable[Tuple[float, float, float, float]]:
        delta = (self.__b - self.__a) / self.__middle_rect_count
        i = self.__a
        while i < self.__b:

            yield i, 0, delta, self.__fx(i+(delta/2.))
            i += delta

    def trapezoids(self) -> Iterable[Tuple[float, float, float, float, float]]:
        dx = (self.__b - self.__a) / self.__trapezoid_count
        i = self.__a
        while i < self.__b:
            ly = self.__fx(i)
            ry = self.__fx(i + dx)
            if ly < 0 and ry > 0 or ly > 0 and ry < 0:
                dy = -ly
            else:
                dy = ry - ly
            yield i, 0, dx, ly, dy
            i += dx

    def point_bounds(self) -> Tuple[float, float, float, float]:
        max, min = self.minmax()
        if min > 0 and max > 0:
            min = 0
        elif min < 0 and max < 0:
            max = 0
        return (self.__a, min, self.__b, max)

    def generate_points(self) -> None:
        self.__points = []
        x1, y1, x2, y2 = self.point_bounds()
        for _ in range(self.__point_count):
            self.__points.append((random.uniform(x1, x2), random.uniform(y1, y2)))

    def points(self) -> Iterable[Tuple[float, float]]:
        return self.__points

    def integrate_monte_carlo(self) -> Tuple[float, float, float, float]:
        positive_points = 0
        negative_points = 0
        out_points = 0
        for p in self.points():
            px, py = p
            fy = self.__fx(px)
            if 0 < py < fy:
                positive_points += 1
            elif 0 > py > fy:
                negative_points += 1
            else:
                out_points += 1
        all_points = positive_points + negative_points + out_points
        x1, y1, x2, y2 = self.point_bounds()
        bound_square = (x2 - x1) * (y2 - y1)
        assert all_points > 0
        integral = bound_square * positive_points / all_points - bound_square * negative_points / all_points
        return positive_points, negative_points, out_points, integral

    def __integrate_rects(self, rects: Iterable[Tuple[float, float, float, float]]) -> float:
        integral = 0
        for x, y, width, height in rects:
            integral += width * height
        return integral

    def integrate_left_rects(self) -> float:
        return self.__integrate_rects(self.left_rects())

    def integrate_right_rects(self) -> float:
        return self.__integrate_rects(self.right_rects())

    def integrate_middle_rects(self) -> float:
        return self.__integrate_rects(self.middle_rects())

    def integrate_trapezoids(self) -> float:
        integral = 0
        for x, y, width, height, delta in self.trapezoids():
            integral += ((2 * height + delta) / 2) * width
        return integral
