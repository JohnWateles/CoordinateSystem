import numpy as np
# import sympy as sp
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import matplotlib.lines as mat_lines
from time import perf_counter
import ctypes


def show_execution_time(func):
    """
    Выводит в консоль время выполнения функции в мкс
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        _e = perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {(perf_counter() - _e) * 1_000_000} mcs;")     # ARGS: {args, kwargs}")
        return result
    return wrapper


_coord_sys_funcs = ctypes.WinDLL("./coord_sys_funcs.dll")
_coord_sys_funcs.rotation2D.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                        ctypes.c_double, ctypes.c_double,
                                        ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]


class CoordinateSystem:
    def __init__(self, ax=None, center=(0, 0), color=None, show_center=False, show_axes=False):
        self.ax = ax
        self.center = center
        self.angle = 0  # Угол в радианах
        self.object_names = dict()
        self.__last = ""
        if ax is None:
            raise ValueError(f"Параметр \"ax\" должен быть определён!")
        if (color is None) and show_center:
            self.add(f"__CENTER__OF_{repr(self)}", ax.plot([center[0]], [center[1]], 'o')[0])
        elif show_center:
            self.add(f"__CENTER__OF_{repr(self)}", ax.plot([center[0]], [center[1]], 'o', color=color)[0])
        else:
            self.add(f"__CENTER__OF_{repr(self)}", ax.plot([center[0]], [center[1]], color=(0, 0, 0))[0])
            # Центр должен быть, иначе неправильно работают методы rotate_to_angle() и move_object()
        if show_axes:
            axis_length = 3
            axis_width = 0.8
            self.add(f"__AXIS_OX__OF_{repr(self)}", ax.plot([center[0], center[0] + axis_length],
                                                            [center[1], center[1]],
                     color=(1, 0, 0), lw=axis_width)[0])
            self.add(f"__AXIS_OY__OF_{repr(self)}", ax.plot([center[0], center[0]],
                                                            [center[1], center[1] + axis_length],
                     color=(0, 0, 1), lw=axis_width)[0])

    @property
    def x(self):
        """
        Возвращает координату центра по оси Ox
        :return:
        """
        return self.center[0]

    @property
    def y(self):
        """
        Возвращает координату центра по оси Oy
        :return:
        """
        return self.center[1]

    @property
    def xy(self):
        return [self.x, self.y]

    @property
    def last(self):
        """
        Возвращает имя последнего добавленного в систему объекта
        :return:
        """
        return self.object_names[self.__last][0]

    def get(self, name: str):
        """
        Возвращает объект по имени name
        :param name:
        :return:
        """
        return self.object_names[name][0]

    def add(self, name: str, any_object):
        """
        Добавляет в систему объект (с его законами движение при необходимости)
        :param name:
        :param any_object:
        :return:
        """
        self.object_names[name] = (any_object, )
        self.__last = name
        if isinstance(any_object, (plt.Rectangle, plt.Circle)):
            self.ax.add_patch(any_object)

    # @show_execution_time
    def rotate(self, angle, center=None):
        """
        Передаётся значение angle в радианах.
        Поворачивает систему координат на угол angle.
        :param angle:
        :param center:
        :return:
        """
        angle = angle % (2 * np.pi)
        if center is None:
            center = self.center
        for index, name_obj in enumerate(self.object_names):
            obj = self.object_names[name_obj][0]
            if isinstance(obj, mat_lines.Line2D):
                xy = obj.get_data()
                x = np.array(xy[0], dtype=np.float64)
                y = np.array(xy[1], dtype=np.float64)
                new_x = (x - center[0]) * np.cos(angle) - (y - center[1]) * np.sin(angle) + center[0]
                new_y = (x - center[0]) * np.sin(angle) + (y - center[1]) * np.cos(angle) + center[1]
                if name_obj == f"__CENTER__OF_{repr(self)}":
                    self.center = new_x[0], new_y[0]
                obj.set_data(new_x, new_y)
            elif isinstance(obj, plt.Rectangle):
                x1, y1 = obj.xy
                obj.xy = self.__rot2d(x1, y1, angle, center)
                curr_angle = obj.angle
                obj.angle = curr_angle + angle * 180 / np.pi
            elif isinstance(obj, plt.Circle):
                x1, y1 = obj.center
                obj.center = self.__rot2d(x1, y1, angle, center)
            elif isinstance(obj, CoordinateSystem):
                obj.rotate(angle, center)
        self.angle += angle
        self.angle = self.angle % (2 * np.pi)

    def rotate_to_angle(self, angle, center=None):
        """
        Передаётся значение angle в градусах.
        Поворачивает систему координат к углу angle.
        :param angle:
        :param center:
        :return:
        """
        # angle -= 0 # Вычитаем 90 градусов из-за изменённой оси отсчёта градусов для класса CoordinateSystem
        angle *= (np.pi / 180)
        angle = angle % (2 * np.pi)

        self.rotate(angle - self.angle, center)

    def rotate_to_local_angle(self, name: str, angle):
        """
        Изменяет угол системы координат относительно другой системы
        :param name:
        :param angle: Значение угла в градусах
        :return:
        """
        obj = self.object_names[name][0]
        if not isinstance(obj, CoordinateSystem):
            raise ValueError("Not CoordinateSystem!")

        obj.rotate_to_angle((180 / np.pi) * self.angle + angle)

    # @show_execution_time
    def move(self, new_position: list | tuple):
        """
        Перемещает систему координат по координатам new_position.
        :param new_position:
        :return:
        """
        for name_obj in self.object_names:
            obj = self.object_names[name_obj][0]
            if isinstance(obj, mat_lines.Line2D):
                xy = obj.get_data()
                x = np.array(xy[0], dtype=np.float64)
                y = np.array(xy[1], dtype=np.float64)
                x += new_position[0] - self.x
                y += new_position[1] - self.y
                obj.set_data(x, y)
            elif isinstance(obj, plt.Rectangle):
                x1, y1 = obj.xy
                obj.xy = x1 + new_position[0] - self.center[0], y1 + new_position[1] - self.center[1]
            elif isinstance(obj, plt.Circle):
                x1, y1 = obj.center
                obj.center = x1 + new_position[0] - self.center[0], y1 + new_position[1] - self.center[1]
            elif isinstance(obj, CoordinateSystem):
                new_x = obj.x + new_position[0] - self.center[0]
                new_y = obj.y + new_position[1] - self.center[1]
                obj.move([new_x, new_y])
        self.center = new_position

    # @show_execution_time
    def move_object(self, name: str = None, new_position: list | tuple = (0, 0)):
        """
        Перемещает объект внутри системы координат, не перемещая её.
        В переменной new_position координаты относительно системы координат self
        :param new_position:
        :param name:
        :return:
        """

        # Переходим в координаты системы self
        new_x = new_position[0] * np.cos(self.angle) - new_position[1] * np.sin(self.angle)
        new_y = new_position[0] * np.sin(self.angle) + new_position[1] * np.cos(self.angle)
        new_position = [new_x, new_y]
        obj = self.object_names[name][0]
        if isinstance(obj, mat_lines.Line2D):
            if name == f"__CENTER__OF_{repr(self)}":
                return
            xy = obj.get_data()
            length = len(xy[0])
            x = np.zeros(length, dtype=np.float64)
            y = np.zeros(length, dtype=np.float64)
            x += new_position[0] + self.x
            y += new_position[1] + self.y
            obj.set_data(x, y)
        elif isinstance(obj, plt.Rectangle):
            obj.xy = self.x + new_position[0], self.y + new_position[1]
        elif isinstance(obj, plt.Circle):
            obj.center = self.x + new_position[0], self.y + new_position[1]
        elif isinstance(obj, CoordinateSystem):
            new_x = self.x + new_position[0]
            new_y = self.y + new_position[1]
            obj.move([new_x, new_y])

    # @show_execution_time
    def __rot2d(self, _x_, _y_, _phi_, center=None):
        """
        Функция поворота координат на угол _phi_ относительно центра center
        :param _x_:
        :param _y_:
        :param _phi_: угол поворота в радианах
        :param center:
        :return:
        """
        if center is None:
            center = self.center
        """
        _phi_ = _phi_ % (2 * np.pi)
        _new_x_ = np.cos(_phi_) * (_x_ - center[0]) - np.sin(_phi_) * (_y_ - center[1]) + center[0]
        _new_y_ = np.sin(_phi_) * (_x_ - center[0]) + np.cos(_phi_) * (_y_ - center[1]) + center[1]
        """
        _new_x_ = ctypes.c_double()
        _new_y_ = ctypes.c_double()
        _coord_sys_funcs.rotation2D(_x_, _y_, _phi_, center[0], center[1], ctypes.byref(_new_x_), ctypes.byref(_new_y_))
        _new_x_ = _new_x_.value
        _new_y_ = _new_y_.value

        return _new_x_, _new_y_


def __get_spring_line(length, coils, diameter, pos=(0, 0)):
    """
    Создаёт пружину по координатам pos
    :param length:
    :param coils:
    :param diameter:
    :param pos:
    :return:
    """
    x = np.linspace(0 + pos[0], length + pos[0], coils * 2)
    y = [(diameter * 0.5 * (-1) ** i) + pos[1] for i in range(len(x))]
    return np.array([x, y])


def get_spring_line(length, coils, diameter, pos=(0, 0), angle=None, center=(0, 0)):
    """
    Создаёт пружину по координатам pos, наклонённую на угол angle вокруг центра center
    :param length:
    :param coils:
    :param diameter:
    :param pos:
    :param angle: Угол в радианах
    :param center:
    :return:
    """
    x = np.linspace(0 + pos[0], length + pos[0], coils * 2)
    y = [-np.sign(i) * (diameter * 0.5 * (-1) ** i) + pos[1] if (i != (len(x) - 1)) else pos[1] for i in range(len(x))]
    if (angle is not None) and (center is not None):
        rotated_x = list()
        rotated_y = list()
        for _x, _y in zip(x, y):
            new_x, new_y = CoordinateSystem._CoordinateSystem__rot2d(None, _x, _y, angle, center)
            rotated_x.append(new_x)
            rotated_y.append(new_y)
        return np.array([rotated_x, rotated_y])
    return np.array([x, y])


def main():
    pass


if __name__ == "__main__":
    main()
