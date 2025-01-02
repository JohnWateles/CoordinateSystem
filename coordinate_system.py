import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.lines as mat_lines


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
    def __init__(self, ax=None, center=(0, 0), x_t=None, y_t=None, phi_t=None, show_center=True):
        self.ax = ax        # График
        self.x_t = x_t      # Закон движения системы координат по X (мб удалить это)
        self.y_t = y_t      # Закон движения системы координат по Y (мб удалить это)
        self.phi_t = phi_t  # Закон поворота системы координат      (мб удалить это)
        self.center = center
        self.angle = 0
        self.object_names = dict()
        self.__last = ""
        if ax is None:
            raise ValueError(f"Параметр \"ax\" должен быть определён!")
        if show_center:
            self.add(f"__CENTER__OF_{repr(self)}", ax.plot([center[0]], [center[1]], 'o')[0])
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

    def add(self, name: str, any_object, x_t=None, y_t=None, phi_t=None):
        """
        Добавляет в систему объект (с его законами движение при необходимости)
        :param name:
        :param any_object:
        :param x_t:
        :param y_t:
        :param phi_t:
        :return:
        """
        self.object_names[name] = (any_object, (x_t, y_t, phi_t))
        self.__last = name
        if isinstance(any_object, (plt.Rectangle, plt.Circle)):
            self.ax.add_patch(any_object)

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

    # ИЗМЕНИТЬ МЕТОД ПРИ НЕОБХОДИМОСТИ! (метод нужен для test1())
    def __move_object(self, new_position: list | tuple, obj):
        """
        То же самое, что и move_object, только передаётся объект.
        :param new_position:
        :param obj:
        :return:
        """
        new_x = new_position[0] * np.cos(self.angle) - new_position[1] * np.sin(self.angle)
        new_y = new_position[0] * np.sin(self.angle) + new_position[1] * np.cos(self.angle)
        new_position = [new_x, new_y]

        if isinstance(obj, mat_lines.Line2D):
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
            sign = 1 if obj.name == "left" else -1
            for x_i, y_i in zip(spring.get_data()[0], spring.get_data()[1]):
                x.append(self.center[0] + new_position[0] + sign * x_i)
                y.append(self.center[1] + new_position[1] + sign * y_i)
            spring.set_data(x, y)
        elif isinstance(obj, CoordinateSystem):
            obj.move(new_position)

    # ИЗМЕНИТЬ МЕТОД ПРИ НЕОБХОДИМОСТИ! (метод нужен для test1())
    def _frame(self, i):
        for index, name_obj in enumerate(self.object_names):
            obj = self.object_names[name_obj][0]
            r_t = self.object_names[name_obj][1]

            if isinstance(obj, mat_lines.Line2D):
                x = list()
                y = list()
                for x_i, y_i in zip(obj.get_data()[0], obj.get_data()[1]):
                    pass
                # obj.set_data(x, y)
            elif isinstance(obj, Spring):
                if obj.name == "left":
                    sp_xy = create_spring_line(obj.length + r_t[0][i] + 1, 10, 0.4)

                    x = list()
                    y = list()
                    for x_i, y_i in zip(sp_xy[0], sp_xy[1]):
                        new_x, new_y = self.__rot2d(x_i, y_i, self.angle, (0, 0))
                        x.append(new_x)
                        y.append(new_y)

                    obj.spring.set_data(x, y)
                    self.__move_object([-3, 0.5], obj)
                elif obj.name == "right":
                    sp_xy = create_spring_line(obj.length - r_t[0][i] - 1, 10, 0.4)
                    x = list()
                    y = list()
                    for x_i, y_i in zip(sp_xy[0], sp_xy[1]):
                        new_x, new_y = self.__rot2d(x_i, y_i, self.angle, (0, 0))
                        x.append(new_x)
                        y.append(new_y)

                    obj.spring.set_data(x, y)
                    self.__move_object([3, 0.5], obj)

            elif isinstance(obj, plt.Rectangle):
                # x, y = obj.xy
                x = r_t[0][i] if r_t[0][i] is not None else 0
                y = r_t[1][i] if r_t[1][i] is not None else 0
                self.__move_object([x, y], obj)
            elif isinstance(obj, CoordinateSystem):
                obj._frame(i)

        if self.x_t is not None:
            self.move([self.x_t[i], self.y])

        if self.y_t is not None:
            self.move([self.x, self.y_t[i]])

        if self.phi_t is not None:
            self.rotate_to_angle(self.phi_t[i])
            pass

    def __rot2d(self, x_arg, y_arg, any_phi_arg, sc=None):
        if sc is None:
            sc = self.center
        phi_arg = any_phi_arg % (2 * np.pi)
        RX = np.cos(phi_arg) * (x_arg - sc[0]) - np.sin(phi_arg) * (y_arg - sc[1]) + sc[0]
        RY = np.sin(phi_arg) * (x_arg - sc[0]) + np.cos(phi_arg) * (y_arg - sc[1]) + sc[1]
        return RX, RY


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


def test1():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[-15, 15], ylim=[-15, 15])
    center = [0, 7]
    s1 = CoordinateSystem(ax, center)
    side_x = 3
    s1.add("line1", ax.plot([-side_x, side_x], [center[1], center[1]], linewidth=2, color=(0, 0, 0))[0])
    s1.add("line2", ax.plot([-side_x, -side_x], [center[1], center[1] + 1], linewidth=2, color=(0, 0, 0))[0])
    s1.add("line3", ax.plot([side_x, side_x], [center[1], center[1] + 1], linewidth=2, color=(0, 0, 0))[0])

    t = sp.Symbol('t')
    X_T_relative = 1 * (sp.sin(1 * t) - 1)
    Y_T_relative = 0.00000001 * sp.sin(t)
    # VX_T_relative = sp.diff(X_T_relative, t)

    _time = np.linspace(0, 520, 10000)
    F_X_T_relative = sp.lambdify(t, X_T_relative, "numpy")
    F_Y_T_relative = sp.lambdify(t, Y_T_relative, "numpy")
    # F_VX_T_relative = sp.lambdify(t, VX_T_relative, "numpy")
    X_T_relative = F_X_T_relative(_time)
    Y_T_relative = F_Y_T_relative(_time)
    # VX_T_relative = F_VX_T_relative(_time)

    # for index, value in enumerate(VX_T_relative):
    #     X_T_relative[index] -= value

    length = center[1] - center[0]
    PHI_T = 90 * sp.sin(0.2 * t) + 90

    X_T_endure = 0.5 * sp.cos(PHI_T * (sp.pi / 180))
    Y_T_endure = 0.5 * sp.sin(PHI_T * (sp.pi / 180))
    F_X_T_endure = sp.lambdify(t, X_T_endure, "numpy")
    F_Y_T_endure = sp.lambdify(t, Y_T_endure, "numpy")
    X_T_endure = F_X_T_endure(_time)
    Y_T_endure = F_Y_T_endure(_time)

    for index, values in enumerate(zip(X_T_endure, Y_T_endure)):
        value_x, value_y = values
        X_T_relative[index] += value_x - value_y

    # PHI_T = 0.000000000000000001 * sp.sin(t)
    # V_PHI_T = sp.diff(PHI_T)
    # X_T_endure = sp.sin(PHI_T)
    # Y_T_endure = sp.cos(PHI_T)
    F_PHI_T = sp.lambdify(t, PHI_T, "numpy")
    # F_V_PHI_T = sp.lambdify(t, V_PHI_T, "numpy")
    PHI_T_VALUES = F_PHI_T(_time)
    # V_PHI_T_VALUES = F_V_PHI_T(_time)

    s1.add("rectangle1", plt.Rectangle([center[0] - 1, center[1]], width=2, height=1, color=(0.6, 0.6, 0.6)),
           X_T_relative, Y_T_relative)
    # ax.add_patch(s1.last)

    spring_xy = create_spring_line(2, 10, 0.4, pos=(-side_x, center[1] + 0.5))
    s1.add("spring1", Spring(ax.plot(spring_xy[0], spring_xy[1], linewidth=1, color=(0, 0.5, 0.8))[0], "left", 2),
           X_T_relative, Y_T_relative)
    spring_xy = create_spring_line(2, 10, 0.4, pos=(center[0] + 1, center[1] + 0.5))
    s1.add("spring2", Spring(ax.plot(spring_xy[0], spring_xy[1], linewidth=1, color=(0, 0.5, 0.8))[0], "right", 2),
           X_T_relative, Y_T_relative)

    center2 = [0, 0]
    s = CoordinateSystem(ax, center2)
    s.add("line", ax.plot([center2[0], center2[0]], [center2[0], center[1]], linewidth=2, color=(0, 0, 0))[0])
    s.add("CoordinateSystem1", s1)
    s.phi_t = PHI_T_VALUES

    def frame(i):
        s._frame(i)
        pass

    _ = FuncAnimation(figure, frame, interval=1, frames=12000)
    plt.show()


def test2():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[-15, 15], ylim=[-15, 15])

    center1 = [0, 0]
    s1 = CoordinateSystem(ax, center1)
    s2 = CoordinateSystem(ax, center1)

    t = sp.Symbol('t')
    _time = np.linspace(0, 520, 10000)

    X_T = 3 * sp.cos(0.1 * t)
    Y_T = 4 * sp.sin(0.1 * t)
    PHI_T = 180 * sp.cos(0.2 * t) - 90
    F_X_T = sp.lambdify(t, X_T, "numpy")
    F_Y_T = sp.lambdify(t, Y_T, "numpy")
    F_PHI_T = sp.lambdify(t, PHI_T, "numpy")
    X_T = F_X_T(_time)
    Y_T = F_Y_T(_time)
    PHI_T = F_PHI_T(_time)

    ax.plot(X_T, Y_T, color=(0, 0, 0), lw=0.7)  # Траектория движения

    distance1 = 2
    point1 = ax.plot([0], [distance1], 'o')[0]
    point2 = ax.plot([-distance1], [0], 'o')[0]
    point3 = ax.plot([0], [-distance1], 'o')[0]
    point4 = ax.plot([distance1], [0], 'o')[0]

    line_width = 0.4
    line1 = ax.plot([0, 0], [0, 4], color=(0, 0, 1), lw=line_width)[0]
    line2 = ax.plot([0, 4], [0, 0], color=(1, 0, 0), lw=line_width)[0]

    s1.add("point1", point1)
    s1.add("point2", point2)
    s1.add("point3", point3)
    s1.add("point4", point4)
    s1.add("line_OY", line1)
    s1.add("line_OX", line2)

    distance2 = 1
    point12 = ax.plot([0], [distance2], 'o')[0]
    point22 = ax.plot([-distance2], [0], 'o')[0]
    point32 = ax.plot([0], [-distance2], 'o')[0]
    point42 = ax.plot([distance2], [0], 'o')[0]

    line12 = ax.plot([0, 0], [0, 4], color=(0, 0, 1), lw=line_width)[0]
    line22 = ax.plot([0, 4], [0, 0], color=(1, 0, 0), lw=line_width)[0]

    s2.add("point1", point12)
    s2.add("point2", point22)
    s2.add("point3", point32)
    s2.add("point4", point42)
    s2.add("line_OY", line12)
    s2.add("line_OX", line22)

    def frame(i):
        coefficient = 13
        value1 = distance1 * (np.cos(0.03 * (distance1 * 0 * coefficient + i)) ** 2)
        value2 = distance1 * (np.cos(0.03 * (distance1 * 1 * coefficient + i)) ** 2)
        value3 = distance1 * (np.cos(0.03 * (distance1 * 2 * coefficient + i)) ** 2)
        value4 = distance1 * (np.cos(0.03 * (distance1 * 3 * coefficient + i)) ** 2)
        s1.move_object("point1", [0, value1])
        s1.move_object("point2", [-value2, 0])
        s1.move_object("point3", [0, -value3])
        s1.move_object("point4", [value4, 0])

        coefficient = 13
        value1 = distance2 * (np.cos(0.06 * (distance2 * 0 * coefficient + i)) ** 2)
        value2 = distance2 * (np.cos(0.06 * (distance2 * 1 * coefficient + i)) ** 2)
        value3 = distance2 * (np.cos(0.06 * (distance2 * 2 * coefficient + i)) ** 2)
        value4 = distance2 * (np.cos(0.06 * (distance2 * 3 * coefficient + i)) ** 2)
        s2.move_object("point1", [0, value1])
        s2.move_object("point2", [-value2, 0])
        s2.move_object("point3", [0, -value3])
        s2.move_object("point4", [value4, 0])

        s1.move([X_T[i], Y_T[i]])
        s1.rotate_to_angle(PHI_T[i])

        k = 0.05
        s2.move([3 * np.cos(k * i), 4 * np.sin(k * i)])

    _ = FuncAnimation(figure, frame, interval=1, frames=12000)
    plt.show()


def test3():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[0, 15], ylim=[0, 15])

    # Начальное расположение объектов, настройка зависимостей
    ###
    length = 10
    rectangle_width = 6
    rectangle_height = 4
    center1 = [length - rectangle_width // 2, 0]
    center2 = [length - rectangle_width // 2, rectangle_height]
    s1 = CoordinateSystem(ax, center1, show_center=False)
    s2 = CoordinateSystem(ax, center2, show_center=False)
    s1.add("cylinder_system", s2)

    rectangle = plt.Rectangle([length - rectangle_width, 0], width=rectangle_width, height=rectangle_height,
                              color=(0.6, 0.6, 0.6))
    s1.add("rectangle1", rectangle)

    white_circle = plt.Circle(center2, radius=rectangle_width // 2, color=(1, 1, 1))
    s1.add("white_circle", white_circle)

    cylinder_radius = 0.4
    cylinder = plt.Circle([center2[0], rectangle_height - (rectangle_width // 2) + cylinder_radius],
                          radius=cylinder_radius, color=(0.8, 0.3, 0.1))
    s2.add("cylinder1", cylinder)

    spring_length = length - rectangle_width
    spring_xy = create_spring_line(spring_length, 10, 0.4, pos=(0, rectangle_height / 2))
    spring = ax.plot(spring_xy[0], spring_xy[1])[0]
    ###

    # Вычисления:
    ###
    t = sp.Symbol("t")
    coefficient = 0.9
    X_T = 2 * (sp.sin(coefficient * t) + 1) + 5
    VX_T = sp.diff(X_T, t)
    WX_T = sp.diff(VX_T, t)
    PHI_T = -80 * sp.cos(coefficient * t) + 90
    V_PHI_T = sp.diff(PHI_T, t)
    W_PHI_T = sp.diff(V_PHI_T, t)

    F_X_T = sp.lambdify(t, X_T, "numpy")
    F_VX_T = sp.lambdify(t, VX_T, "numpy")
    F_WX_T = sp.lambdify(t, WX_T, "numpy")
    F_PHI_T = sp.lambdify(t, PHI_T, "numpy")
    F_V_PHI_T = sp.lambdify(t, V_PHI_T, "numpy")
    F_W_PHI_T = sp.lambdify(t, W_PHI_T, "numpy")

    _time = np.linspace(0, 520, 10000)
    X_T = F_X_T(_time)
    VX_T = F_VX_T(_time)
    WX_T = F_WX_T(_time)
    PHI_T = F_PHI_T(_time)
    V_PHI_T = F_V_PHI_T(_time)
    W_PHI_T = F_W_PHI_T(_time)
    ###

    def frame(i):
        i = i % 10000
        s1.move([X_T[i], 0])
        s2.rotate_to_angle(PHI_T[i])

        _spring_xy = create_spring_line(X_T[i] - rectangle_width // 2, 10, 0.4,
                                        pos=(0, rectangle_height / 2))
        spring.set_data(_spring_xy[0], _spring_xy[1])

    _ = FuncAnimation(figure, frame, interval=1, frames=12000)
    plt.show()


def test4():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[0, 15], ylim=[0, 15])

    show_center = False
    s1 = CoordinateSystem(ax, (4.5, 2.5), show_center=show_center)
    s1.add("rec1", plt.Rectangle((2, 1), width=5, height=3, color=(1, 0.5, 0.75)))
    s1.add("rec2", plt.Rectangle((6, 3), width=1.7, height=1.7, color=(0.9, 0.4, 0.67)))
    x = 6
    y = 3
    s1.add("rec3", plt.Rectangle((x + 0.1, y + 0.1), width=1.5, height=1.5, color=(0.9, 0.9, 0.9)))
    s1.add("rec4", plt.Rectangle((x + 0.1, y + 0.7), width=1.5, height=0.65, color=(218 / 255,
                                                                                    189 / 255,
                                                                                    179 / 255)))
    s1.add("rec5", plt.Rectangle((x + 0.1 + 0.25, y + 0.1), width=1, height=0.65, color=(218 / 255,
                                                                                         189 / 255,
                                                                                         179 / 255)))
    s1.add("rec6", plt.Rectangle((x + 0.1 + 0.25 + 0.198, y + 0.1), width=0.60, height=0.60, color=(0.9, 0.65, 0.65)))
    s1.add("rec7", plt.Rectangle((x + 1.5 - 0.3, y + 1.5 - 0.5), width=0.3, height=0.15, color=(0, 0, 0)))
    s1.add("rec8", plt.Rectangle((x + 1.5 - 0.3, y + 1.5 - 0.5), width=0.14, height=0.15, color=(1, 1, 1)))
    s1.add("rec9", plt.Rectangle((x + 1.5 - 1.3, y + 1.5 - 0.5), width=0.3, height=0.15, color=(0, 0, 0)))
    s1.add("rec10", plt.Rectangle((x + 1.5 - 1.13, y + 1.5 - 0.5), width=0.15, height=0.15, color=(1, 1, 1)))
    s1.add("rec11", plt.Rectangle((2, 0), width=0.5, height=1.5, color=(218 / 255,
                                                                        189 / 255,
                                                                        179 / 255)))
    s1.add("rec12", plt.Rectangle((2 + 4.5, 0), width=0.5, height=1.5, color=(218 / 255,
                                                                              189 / 255,
                                                                              179 / 255)))

    distance = 0.07
    stick_height = 0.2
    border_height = 2
    white_space = plt.Rectangle((0, 2.5 - distance), width=3 + distance, height=(2 * distance) + stick_height,
                                color=(1, 1, 1))
    stick = plt.Rectangle((0, 2.5), width=3, height=stick_height, color=(0, 0, 0))
    border = plt.Rectangle((0, 2.5 - (border_height / 2) + (stick_height / 2)), width=0.2, height=border_height, color=(0, 0, 0))

    s2 = CoordinateSystem(ax, (0 + 0.1, 2.5 + stick_height / 2), show_center=show_center)
    s2.add("white_space", white_space)
    s2.add("stick", stick)
    s2.add("border", border)

    s1.add("s2", s2)

    coefficient = 0.8
    t = sp.Symbol("t")
    PHI_T = 360 * sp.sin(0.2 * coefficient * t) ** 1
    X_T = 0.7 * (6 * sp.cos(coefficient * t) - 2 * sp.sin(coefficient * t) + sp.sin(coefficient * t) ** 2) + 7
    Y_T = 0.5 * (X_T * sp.sin(coefficient * t)) + 8

    PHI_T = sp.lambdify(t, PHI_T, "numpy")
    X_T = sp.lambdify(t, X_T, "numpy")
    Y_T = sp.lambdify(t, Y_T, "numpy")

    _time = np.linspace(0, 520, 10000)
    PHI_T = PHI_T(_time)
    X_T = X_T(_time)
    Y_T = Y_T(_time)

    # ax.plot(X_T, Y_T, lw=0.8)

    def frame(i):
        i = i % 10000
        s1.move([X_T[i], Y_T[i]])
        s1.rotate_to_angle(PHI_T[i])
        s1.move_object("s2", [np.sin(0.5 * i) - 3.8, 0])

    _ = FuncAnimation(figure, frame, interval=1, frames=12000)
    plt.show()


def test5():
    figure = plt.figure(figsize=(8, 8))
    g = figure.add_subplot(1, 1, 1)
    g.set(xlim=[0, 15], ylim=[0, 15])

    s1 = CoordinateSystem(g, show_center=False)
    g.plot([3, 2], [1, 2])

    def frame(i):
        pass

    _ = FuncAnimation(figure, frame, interval=1, frames=12000)
    plt.show()


def main():
    test4()


if __name__ == "__main__":
    main()
