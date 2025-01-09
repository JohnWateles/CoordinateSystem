import numpy as np
# import sympy as sp
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import matplotlib.lines as mat_lines
from time import perf_counter


def show_execution_time(func):
    def wrapper(*args, **kwargs):
        _e = perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {round((perf_counter() - _e) * 1000, 2)}")
        return result
    return wrapper


class Spring:
    """
    Попытка нормально анимировать пружины
    """
    def __init__(self, spring, name, length, pos=(0, 0)):
        self.spring = spring
        self.name = name
        self.length = length
        self.__pos = pos

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        """
        ...
        :param pos:
        :return:
        """
        """
        new_data = list(list(), list())
        for x, y in zip(self.spring.get_data[0], self.spring.get_data[1]):
            new_data[0].append(x + pos[0])
            new_data[1].append(y + pos[1])
        """
        self.__pos = pos


class CoordinateSystem:
    def __init__(self, ax=None, center=(0, 0), show_center=True, color=None):
        self.ax = ax
        self.center = center
        self.angle = 0
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
    def last(self):
        """
        Возвращает имя последнего добавленного в систему объекта
        :return:
        """
        return self.object_names[self.__last][0]

    def get_object(self, name: str):
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
            if isinstance(obj, Spring):
                spring = obj.spring
                x = list()
                y = list()
                for x_i, y_i in zip(spring.get_data()[0], spring.get_data()[1]):
                    new_x, new_y = self.__rot2d(x_i, y_i, angle, center)
                    x.append(new_x)
                    y.append(new_y)
                spring.set_data(x, y)
            elif isinstance(obj, mat_lines.Line2D):
                x = list()
                y = list()
                for x_i, y_i in zip(obj.get_data()[0], obj.get_data()[1]):
                    new_x, new_y = self.__rot2d(x_i, y_i, angle, center)
                    x.append(new_x)
                    y.append(new_y)
                    if index == 0:
                        self.center = new_x, new_y
                obj.set_data(x, y)
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
        angle -= 90     # Вычитаем 90 градусов из-за изменённой оси отсчёта градусов для класса CooridateSystem
        angle *= (np.pi / 180)
        angle = angle % (2 * np.pi)

        self.rotate(angle - self.angle, center)

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
                x = list()
                y = list()
                for x_i, y_i in zip(obj.get_data()[0], obj.get_data()[1]):
                    x.append(x_i + new_position[0] - self.center[0])
                    y.append(y_i + new_position[1] - self.center[1])
                obj.set_data(x, y)
            elif isinstance(obj, plt.Rectangle):
                x1, y1 = obj.xy
                obj.xy = x1 + new_position[0] - self.center[0], y1 + new_position[1] - self.center[1]
            elif isinstance(obj, plt.Circle):
                x1, y1 = obj.center
                obj.center = x1 + new_position[0] - self.center[0], y1 + new_position[1] - self.center[1]
            elif isinstance(obj, Spring):
                spring = obj.spring
                x = list()
                y = list()
                for x_i, y_i in zip(spring.get_data()[0], spring.get_data()[1]):
                    x.append(x_i + new_position[0] - self.center[0])
                    y.append(y_i + new_position[1] - self.center[1])
                spring.set_data(x, y)
            elif isinstance(obj, CoordinateSystem):
                new_x = obj.x + new_position[0] - self.center[0]
                new_y = obj.y + new_position[1] - self.center[1]
                obj.move([new_x, new_y])

        self.center = new_position

    def move_object(self, name: str = None, new_position: list | tuple = (0, 0)):
        """
        Перемещает объект внутри системы координат, не перемещая её.
        В переменной new_position координаты относительно системы координат self
        :param new_position:
        :param name:
        :return:
        """
        new_x = new_position[0] * np.cos(self.angle) - new_position[1] * np.sin(self.angle)
        new_y = new_position[0] * np.sin(self.angle) + new_position[1] * np.cos(self.angle)
        new_position = [new_x, new_y]
        if name is None:
            return
        obj = self.object_names[name][0]
        if isinstance(obj, mat_lines.Line2D):
            if name == f"__CENTER__OF_{repr(self)}":
                return
            x = list()
            y = list()
            for x_i, y_i in zip(obj.get_data()[0], obj.get_data()[1]):
                x.append(self.center[0] + new_position[0])
                y.append(self.center[1] + new_position[1])
            obj.set_data(x, y)
        elif isinstance(obj, plt.Rectangle):
            obj.xy = self.center[0] + new_position[0], self.center[1] + new_position[1]
        elif isinstance(obj, plt.Circle):
            obj.center = self.center[0] + new_position[0], self.center[1] + new_position[1]
        elif isinstance(obj, Spring):
            spring = obj.spring
            x = list()
            y = list()
            for x_i, y_i in zip(spring.get_data()[0], spring.get_data()[1]):
                x.append(self.center[0] + new_position[0])
                y.append(self.center[1] + new_position[1])
            spring.set_data(x, y)
        elif isinstance(obj, CoordinateSystem):
            new_x = self.center[0] + new_position[0]
            new_y = self.center[1] + new_position[1]
            obj.move([new_x, new_y])

    # @show_execution_time
    def __rot2d(self, _x_, _y_, _phi_, center=None):
        if center is None:
            center = self.center
        _phi_ = _phi_ % (2 * np.pi)
        _new_x_ = np.cos(_phi_) * (_x_ - center[0]) - np.sin(_phi_) * (_y_ - center[1]) + center[0]
        _new_y_ = np.sin(_phi_) * (_x_ - center[0]) + np.cos(_phi_) * (_y_ - center[1]) + center[1]
        return _new_x_, _new_y_


def create_spring_line(length, coils, diameter, pos=(0, 0)):
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


def main():
    pass


if __name__ == "__main__":
    main()
