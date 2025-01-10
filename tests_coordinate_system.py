import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from coordinate_system import CoordinateSystem, get_spring_line
from time import perf_counter
import math


def test_abs():
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    def frame(i):
        pass

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test1():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[-15, 15], ylim=[-15, 15])

    abs_system = CoordinateSystem(ax, color=(1, 0, 0))
    s1 = CoordinateSystem(ax)
    s2 = CoordinateSystem(ax)
    s3 = CoordinateSystem(ax, color=(0, 0, 0))
    abs_system.add("s1", s1)
    abs_system.add("s2", s2)
    abs_system.add("s3", s3)

    t = sp.Symbol('t')
    _time = np.linspace(0, 520, 10000)

    X_T = 5 * sp.cos(0.5 * t)
    Y_T = 6 * sp.sin(0.5 * t)
    PHI_T = 180 * sp.cos(0.8 * t) - 90
    F_X_T = sp.lambdify(t, X_T, "numpy")
    F_Y_T = sp.lambdify(t, Y_T, "numpy")
    F_PHI_T = sp.lambdify(t, PHI_T, "numpy")
    X_T = F_X_T(_time)
    Y_T = F_Y_T(_time)
    PHI_T = F_PHI_T(_time)

    ABS_X_T, ABS_Y_T = 5 * sp.cos(0.1 * t), 5 * sp.sin(0.1 * t)
    ABS_X_T = sp.lambdify(t, ABS_X_T, "numpy")
    ABS_Y_T = sp.lambdify(t, ABS_Y_T, "numpy")
    ABS_X_T = ABS_X_T(_time)
    ABS_Y_T = ABS_Y_T(_time)

    __t = np.linspace(0, 2 * np.pi, 43)
    __x_t = 5 * np.cos(__t)
    __y_t = 6 * np.sin(__t)
    line, = ax.plot(__x_t, __y_t, "--", color=(0, 0, 0), lw=0.8)  # Траектория движения
    abs_system.add("line", line)

    __t = np.linspace(0, 2 * np.pi, 127)
    __x_t = 5 * np.cos(__t)
    __y_t = 5 * np.sin(__t)
    ax.plot(__x_t, __y_t, "-.", color=(0, 0, 0), lw=0.6)  # Глобальная траектория движения

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
    point1 = ax.plot([0], [distance2], 'o')[0]
    point2 = ax.plot([-distance2], [0], 'o')[0]
    point3 = ax.plot([0], [-distance2], 'o')[0]
    point4 = ax.plot([distance2], [0], 'o')[0]

    line1 = ax.plot([0, 0], [0, 4], color=(0, 0, 1), lw=line_width)[0]
    line2 = ax.plot([0, 4], [0, 0], color=(1, 0, 0), lw=line_width)[0]

    s2.add("point1", point1)
    s2.add("point2", point2)
    s2.add("point3", point3)
    s2.add("point4", point4)
    s2.add("line_OY", line1)
    s2.add("line_OX", line2)

    distance3 = 2.3
    point1 = ax.plot([0], [distance3], 'o')[0]
    point2 = ax.plot([-distance3], [0], 'o')[0]
    point3 = ax.plot([0], [-distance3], 'o')[0]
    point4 = ax.plot([distance3], [0], 'o')[0]

    line1 = ax.plot([0, 0], [0, 4], color=(0, 0, 1), lw=line_width)[0]
    line2 = ax.plot([0, 4], [0, 0], color=(1, 0, 0), lw=line_width)[0]

    s3.add("point1", point1)
    s3.add("point2", point2)
    s3.add("point3", point3)
    s3.add("point4", point4)
    s3.add("line_OY", line1)
    s3.add("line_OX", line2)

    def frame(i):
        # Изменение положения точек внутри системы s1
        coefficient = 13
        value1 = distance1 * (np.cos(0.03 * (distance1 * 0 * coefficient + i)) ** 2)
        value2 = distance1 * (np.cos(0.03 * (distance1 * 1 * coefficient + i)) ** 2)
        value3 = distance1 * (np.cos(0.03 * (distance1 * 2 * coefficient + i)) ** 2)
        value4 = distance1 * (np.cos(0.03 * (distance1 * 3 * coefficient + i)) ** 2)
        s1.move_object("point1", [0, value1])
        s1.move_object("point2", [-value2, 0])
        s1.move_object("point3", [0, -value3])
        s1.move_object("point4", [value4, 0])

        # Изменение положения точек внутри системы s2
        coefficient = 13
        value1 = distance2 * (np.cos(0.06 * (distance2 * 0 * coefficient + i)) ** 2)
        value2 = distance2 * (np.cos(0.06 * (distance2 * 1 * coefficient + i)) ** 2)
        value3 = distance2 * (np.cos(0.06 * (distance2 * 2 * coefficient + i)) ** 2)
        value4 = distance2 * (np.cos(0.06 * (distance2 * 3 * coefficient + i)) ** 2)
        s2.move_object("point1", [0, value1])
        s2.move_object("point2", [-value2, 0])
        s2.move_object("point3", [0, -value3])
        s2.move_object("point4", [value4, 0])

        # Изменение положения точек внутри системы s3
        value1 = distance3 * (np.cos(0.1 * i))
        value2 = distance3 * (np.cos(0.1 * i))
        value3 = distance3 * (np.cos(0.1 * i))
        value4 = distance3 * (np.cos(0.1 * i))
        s3.move_object("point1", [0, value1])
        s3.move_object("point2", [-value2, 0])
        s3.move_object("point3", [0, -value3])
        s3.move_object("point4", [value4, 0])

        # ...
        abs_system.move_object("s1", [X_T[i], Y_T[i]])
        abs_system.get("s1").rotate_to_angle(PHI_T[i])   # s1.rotate_to_angle(PHI_T[i])

        k = 0.05
        abs_system.move_object("s2", [5 * np.cos(k * i), 6 * np.sin(k * i)])

        new_i = (i + 100) % 10000
        abs_system.move_object("s3", [X_T[new_i], Y_T[new_i]])
        abs_system.get("s3").rotate_to_angle(90)         # s3.rotate_to_angle(90)

        abs_system.move([ABS_X_T[i], ABS_Y_T[i]])
        abs_system.rotate(-np.pi / 300)

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test2():
    # 25
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    show_center = False
    s1 = CoordinateSystem(ax, show_center=show_center)
    if show_center:
        line_width = 0.4
        line_length = 2
        line1 = ax.plot([0, line_length], [0, 0], color=(1, 0, 0), lw=line_width)[0]
        line2 = ax.plot([0, 0], [0, line_length], color=(0, 0, 1), lw=line_width)[0]
        s1.add("lineOX", line1)
        s1.add("lineOY", line2)

    t = np.linspace(np.pi, 2 * np.pi, 127)
    track_radius = 5
    x_t = track_radius * np.cos(t)
    y_t = track_radius * np.sin(t)
    line, = ax.plot(x_t, y_t, "-", color=(0, 0, 0), lw=2)

    circle_radius = 0.8
    position = [0, -track_radius + circle_radius + 0.05]
    circle = plt.Circle(position, circle_radius, color=(0.3, 0.3, 0.8))
    s1.add("circle", circle)

    s2 = CoordinateSystem(ax, show_center=show_center)
    if show_center:
        line1 = ax.plot([0, line_length], [0, 0], color=(1, 0, 0), lw=line_width)[0]
        line2 = ax.plot([0, 0], [0, line_length], color=(0, 0, 1), lw=line_width)[0]
        s2.add("lineOX", line1)
        s2.add("lineOY", line2)

    s2.move(position)

    s1.add("s2", s2)

    line_length = 3
    line, = ax.plot([position[0], position[0]], [position[1], position[1] - line_length], color=(0.2, 0.2, 0.1))
    s2.add("line", line)

    small_circle_radius = 0.3
    small_circle = plt.Circle([position[0], position[1] - line_length], radius=small_circle_radius)
    s2.add("small_circle", small_circle)

    def frame(i):
        coefficient = 0.05
        angle = 80 * np.sin(coefficient * i) + 90
        s1.rotate_to_angle(angle)
        s2.rotate_to_angle(40 * np.sin(0.1 * i) + 90)
        # s1.rotate_to_local_angle("s2", 40 * np.sin(coefficient * i) + 90)

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test3():
    # 30
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
    spring_xy = get_spring_line(spring_length, 10, 0.4, pos=(0, rectangle_height / 2))
    spring = ax.plot(spring_xy[0], spring_xy[1])[0]
    ###

    # Вычисления:
    ###
    t = sp.Symbol("t")
    coefficient = 1.5
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

        _spring_xy = get_spring_line(X_T[i] - rectangle_width // 2, 10, 0.4,
                                     pos=(0, rectangle_height / 2))
        spring.set_data(_spring_xy[0], _spring_xy[1])

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test4():
    # 37
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    show_center = False
    acs = CoordinateSystem(ax, show_center=show_center, color=(0, 0, 0))

    line_length = 5
    distance_to_point1 = 4
    distance_to_point2 = 3.4

    s1 = CoordinateSystem(ax, show_center=show_center)
    line, = ax.plot([0, 0], [0, line_length], lw=3, color=(0.2, 0.2, 0.7))
    point, = ax.plot([0], [distance_to_point1], "*", color=(0, 0, 0))
    s1.add("line", line)
    s1.add("point", point)

    s2 = CoordinateSystem(ax, show_center=show_center)
    line, = ax.plot([0, 0], [0, line_length], lw=3, color=(0.2, 0.2, 0.7))
    point, = ax.plot([0], [distance_to_point2], "*", color=(0, 0, 0))
    s2.add("line", line)
    s2.add("point", point)

    acs.add("s1", s1)
    acs.add("s2", s2)

    phi2 = 120
    phi1 = 30

    acs.rotate_to_local_angle("s1", phi2)
    acs.rotate_to_local_angle("s2", phi1)

    s_spring = CoordinateSystem(ax, show_center=show_center, color=(0.5, 0.5, 0.5))

    point1 = s1.get("point").get_data()  # ([...], [...])
    point2 = s2.get("point").get_data()  # ([...], [...])
    vector = [point1[0][0] - point2[0][0], point1[1][0] - point2[1][0]]
    distance = np.sqrt((vector[0]) ** 2 + (vector[1]) ** 2)
    vector = [vector[0] / distance, vector[1] / distance]
    e_vector = [1, 0]
    alpha = np.arccos(vector[0] * e_vector[0] + vector[1] * e_vector[1]) * (180 / np.pi)
    spring_xy = get_spring_line(distance, 15, 0.5)
    spring, = ax.plot(spring_xy[0], spring_xy[1], color=(0.5, 0.5, 0.5))

    s_spring.add("spring", spring)
    s_spring.move([point1[0][0], point1[1][0]])
    s_spring.rotate_to_angle(alpha - 90)

    acs.add("s_spring", s_spring)

    def frame(i):
        coefficient1 = 0.03
        coefficient2 = 0.05
        _phi1 = 30 * ((np.sin(coefficient1 * i) + 1) / 2)
        _phi2 = 120 * ((np.sin(-coefficient2 * i) + 1) / 2)
        acs.rotate_to_local_angle("s1", _phi2)
        acs.rotate_to_local_angle("s2", _phi1)

        _s_spring = acs.get("s_spring")
        _point1 = acs.get("s1").get("point").get_data()
        _point2 = acs.get("s2").get("point").get_data()
        _vector = [_point1[0][0] - _point2[0][0], _point1[1][0] - _point2[1][0]]
        _distance = math.sqrt((_vector[0]) ** 2 + (_vector[1]) ** 2)
        _vector = [_vector[0] / _distance, _vector[1] / _distance]
        _e_vector = [1, 0]
        _alpha = np.arccos(_vector[0] * _e_vector[0] + _vector[1] * _e_vector[1]) * (180 / np.pi) - 90
        _spring_xy = get_spring_line(_distance, 15, 0.5, pos=_s_spring.xy, angle=_s_spring.angle,
                                     center=_s_spring.center)
        _s_spring.get("spring").set_data(_spring_xy[0], _spring_xy[1])

        if _phi2 - _phi1 < -2:
            _alpha = 180 - _alpha
        acs.rotate_to_local_angle("s_spring", _alpha)
        acs.move_object("s_spring", [_point1[0][0] - acs.x, _point1[1][0] - acs.y])

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test5():
    # 22
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    def frame(i):
        pass

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test6():
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    ax.plot([0, 0], [-10, 10], "--", lw=1)

    show_center = False
    acs = CoordinateSystem(ax, show_center=show_center, color=(1, 0, 0))

    s1 = CoordinateSystem(ax, show_center=show_center)
    radius1 = 0.2
    circle1 = plt.Circle((0, 0), radius1, color=(0, 0, 0))
    s1.add("circle1", circle1)

    line1_length = 0.8
    line2_length = 3
    s1.move([0, line1_length + line2_length])

    abs_line, = ax.plot([0, 0], [line1_length, line1_length + line2_length], lw=5, color=(0, 0, 0))
    s1.add("abs_line", abs_line)

    s2 = CoordinateSystem(ax, show_center=show_center)
    line, = ax.plot([0, 0], [0, line1_length], lw=5, color=(0, 0, 0))
    radius2 = 0.2
    circle2 = plt.Circle((0, line1_length), radius2, color=(0, 0, 0))
    s2.add("line", line)
    s2.add("point", circle2)

    acs.add("s1", s1)
    acs.add("s2", s2)
    # acs.add("abs_line", abs_line)

    def frame(i):
        # return
        alpha1 = (180 * (0.05 * i) + 90) % 360
        acs.rotate_to_local_angle("s2", alpha1)

        curX, curY = acs.get("s2").get("point").center
        curX, curY = curX - acs.x, curY - acs.y

        newX = 0
        newY = np.sqrt(line2_length ** 2 - curX ** 2) + curY
        alpha = -(180 / np.pi) * np.arcsin((line1_length / line2_length) * np.sin((np.pi / 180) * (alpha1 - 90))) + 90
        acs.rotate_to_local_angle("s1", alpha)
        acs.move_object("s1", [newX, newY])

        # acs.move([3 * np.sin(0.01 * i), 3 * np.cos(0.01 * i)])
        # acs.rotate(np.pi / 180)

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test228():
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

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()