import numpy as np
# import sympy as sp
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
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

type CoordSys = CoordinateSystem    # Для адекватной аннотации типа


class CoordinateSystem:
    __slots__ = ("ax", "center", "__angle", "object_names", "__last")

    def __init__(self, ax=None, center=(0, 0), color=None, show_center=False, show_axes=False):
        self.ax = ax
        self.center = center
        self.__angle = 0  # Угол в радианах
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

    @property
    def angle(self):
        """
        Возвращает угол в радианах
        :return:
        """
        return self.__angle

    @angle.setter
    def angle(self, value):
        value = value % (2 * np.pi)
        self.__angle = value

    def get(self, name: str) -> CoordSys | plt.Line2D | plt.Circle | plt.Rectangle:
        """
        Возвращает объект по имени name
        :param name:
        :return:
        """
        return self.object_names[name][0]

    def __getitem__(self, name) -> CoordSys | plt.Line2D | plt.Circle | plt.Rectangle:
        """
        Возвращает объект по имени name
        :param name:
        :return:
        """
        return self.object_names[name][0]

    def add(self, name: str, any_object):
        """
        Добавляет в систему объект
        :param name:
        :param any_object:
        :return:
        """
        self.object_names[name] = (any_object, )
        self.__last = name
        if isinstance(any_object, patches.Patch):
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
                obj.xy = self._rot2d(x1, y1, angle, center)
                curr_angle = obj.angle
                obj.angle = curr_angle + angle * 180 / np.pi
            elif isinstance(obj, plt.Circle):
                x1, y1 = obj.center
                obj.center = self._rot2d(x1, y1, angle, center)
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
        angle *= (np.pi / 180)
        angle = angle % (2 * np.pi)

        self.rotate(angle - self.angle, center)

    def rotate_to_local_angle(self, name: str, angle):
        """
        Изменяет угол системы координат относительно другой системы
        :param name: Имя системы координат
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
                obj.xy = x1 + new_position[0] - self.x, y1 + new_position[1] - self.y
            elif isinstance(obj, plt.Circle):
                x1, y1 = obj.center
                obj.center = x1 + new_position[0] - self.x, y1 + new_position[1] - self.y
            elif isinstance(obj, CoordinateSystem):
                new_x = obj.x + new_position[0] - self.x
                new_y = obj.y + new_position[1] - self.y
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
    def _rot2d(self, _x_, _y_, _phi_, center=None):
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
    x = np.linspace(0, length, coils * 2, dtype=np.float64)
    y = np.array([-np.sign(i) * (diameter * 0.5 * (-1) ** i) if (i != (len(x) - 1)) else 0 for i in range(len(x))],
                 dtype=np.float64)
    if angle is not None:
        new_x = (x - center[0]) * np.cos(angle) - (y - center[1]) * np.sin(angle) + center[0] + pos[0]
        new_y = (x - center[0]) * np.sin(angle) + (y - center[1]) * np.cos(angle) + center[1] + pos[1]
        return np.array([new_x, new_y])
    x += pos[0]
    y += pos[1]
    return np.array([x, y])


class SpiralSpring:
    def __init__(self, ax, pos1: tuple | list, pos2: tuple | list, coils=1, **kwargs):
        self.ax = ax
        self.__angle = 0
        self.__coils = coils
        self.__pos1 = pos1
        self.__pos2 = pos2
        spring_xy, _ = self.__get_spring_spiral(pos1, pos2)
        self.__line2D, = ax.plot(spring_xy[0], spring_xy[1], **kwargs)

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        value %= 2 * np.pi
        self.__angle = value

    def __get_spring_spiral(self, pos1: tuple | list, pos2: tuple | list):
        x1, y1 = pos1
        x2, y2 = pos2
        delta_x = x2 - x1
        delta_y = y2 - y1
        t_max = np.sqrt(delta_x ** 2 + delta_y ** 2)

        coils = int(self.__coils)

        if delta_y > 0:
            phi = np.arccos(delta_x / t_max) + coils * 2 * np.pi
        elif delta_x < 0:
            phi = -np.arcsin(delta_y / t_max) + coils * 2 * np.pi + np.pi
        else:
            phi = np.arcsin(delta_y / t_max) + coils * 2 * np.pi + 2 * np.pi

        help_value = (phi % (2 * np.pi))
        # Мб добавить проверку на [(help_value + self.__angle) % (2 * np.pi)] < epsilon
        if ((3 * np.pi) / 2 < self.__angle < 2 * np.pi) and (0 < help_value < (np.pi / 2)):
            self.__coils += 1
            phi += 2 * np.pi
        elif ((3 * np.pi) / 2 < help_value < 2 * np.pi) and (0 < self.__angle < (np.pi / 2)):
            self.__coils -= 1
            phi -= 2 * np.pi
        coefficient = (phi / t_max)
        t = np.linspace(0, t_max, 127)
        x = t * np.cos(coefficient * t)
        y = t * np.sin(coefficient * t)
        x += pos1[0]
        y += pos1[1]
        return np.array([x, y]), phi

    def update(self, pos1: tuple | list, pos2: tuple | list):
        """
        Обновляет положение спиральной пружины.
        (Лучше вызывать этот метод самым последним при анимировании)
        :param pos1:
        :param pos2:
        :return:
        """
        spring_xy, phi = self.__get_spring_spiral(pos1, pos2)
        self.angle = phi
        self.__line2D.set_data(spring_xy[0], spring_xy[1])
        self.__pos1 = pos1
        self.__pos2 = pos2
        return self


def main():
    pass


if __name__ == "__main__":
    main()
