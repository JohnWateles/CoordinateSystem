import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.lines as mat_lines


class Spring:
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
    def __init__(self, ax=None, centerX=0, centerY=0, x_t=None, y_t=None, phi_t=None):
        self.ax = ax    # График
        self.x_t = x_t      # Закон движения системы координат по X
        self.y_t = y_t      # Закон движения системы координат по Y
        self.phi_t = phi_t  # Закон поворота системы координат
        self.center = centerX, centerY
        self.angle = 0
        self.object_names = dict()
        self.__last = ""
        # self.objects = list()
        # self.r_ts = list()
        if ax is None:
            raise ValueError(f"Параметр \"ax\" должен быть определён!")
        self.add(f"__CENTER__{id(self)}", ax.plot([centerX], [centerY], 'o')[0])

    @property
    def x(self):
        return self.center[0]

    @property
    def y(self):
        return self.center[1]

    @property
    def last(self):
        """
        Возвращает последний добавленный в систему объект
        :return:
        """
        return self.object_names[self.__last][0]

    def add(self, name: str, any_object, x_t=None, y_t=None, phi_t=None):
        self.object_names[name] = (any_object, (x_t, y_t, phi_t))
        self.__last = name
        # self.objects.append(any_object)
        # self.r_ts.append((x_t, y_t, phi_t))

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

    def move_object(self, new_position: list | tuple, name: str = None):
        """
        Перемещает объекты внутри системы координат, не перемещая её.
        В переменной new_position координаты, относительно системы координат self
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
            # if index == 0 and len(obj.get_data()[0]) == 1:
            #     return
            if name == f"__CENTER__{id(self)}":
                return
            x = list()
            y = list()
            # print(obj.get_data())
            for x_i, y_i in zip(obj.get_data()[0], obj.get_data()[1]):
                x.append(self.center[0] + new_position[0])
                y.append(self.center[1] + new_position[1])
            # self.ax.plot(x, y, linewidth=2, color=(0, 0, 0))
            obj.set_data(x, y)
            # print(obj.get_data())
        elif isinstance(obj, plt.Rectangle):
            # x1, y1 = obj.xy
            obj.xy = self.center[0] + new_position[0], self.center[1] + new_position[1]
        elif isinstance(obj, Spring):
            spring = obj.spring
            x = list()
            y = list()
            for x_i, y_i in zip(spring.get_data()[0], spring.get_data()[1]):
                x.append(self.center[0] + new_position[0])
                y.append(self.center[1] + new_position[1])
            spring.set_data(x, y)
        elif isinstance(obj, CoordinateSystem):
            # BAD!!!
            obj.move(new_position)
        # self.center = new_position

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

    # ИЗМЕНИТЬ МЕТОД ПРИ НЕОБХОДИМОСТИ!
    def frame(self, i):
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
                obj.frame(i)

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
    x = np.linspace(0 + pos[0], length + pos[0], coils * 2)
    y = [(diameter * 0.5 * (-1) ** i) + pos[1] for i in range(len(x))]
    return np.array([x, y])


def main():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[-15, 15], ylim=[-15, 15])
    center = [0, 7]
    s1 = CoordinateSystem(ax, *center)
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
    ax.add_patch(s1.last)

    spring_xy = create_spring_line(2, 10, 0.4, pos=(-side_x, center[1] + 0.5))
    s1.add("spring1", Spring(ax.plot(spring_xy[0], spring_xy[1], linewidth=1, color=(0, 0.5, 0.8))[0], "left", 2),
           X_T_relative, Y_T_relative)
    spring_xy = create_spring_line(2, 10, 0.4, pos=(center[0] + 1, center[1] + 0.5))
    s1.add("spring2", Spring(ax.plot(spring_xy[0], spring_xy[1], linewidth=1, color=(0, 0.5, 0.8))[0], "right", 2),
           X_T_relative, Y_T_relative)

    center2 = [0, 0]
    s = CoordinateSystem(ax, *center2)
    s.add("line", ax.plot([center2[0], center2[0]], [center2[0], center[1]], linewidth=2, color=(0, 0, 0))[0])
    s.add("CoordinateSystem1", s1)
    s.phi_t = PHI_T_VALUES

    def frame(i):
        s.frame(i)
        pass

    _ = FuncAnimation(figure, frame, interval=1, frames=12000)
    plt.show()


if __name__ == "__main__":
    main()
