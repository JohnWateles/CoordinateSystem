import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from coordinate_system import CoordinateSystem, SpiralSpring, get_spring_line, show_execution_time
import math


def test_abs():
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])
    show_center = True
    show_axes = True
    acs = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)

    def frame(i):
        pass

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test1():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[-15, 15], ylim=[-15, 15])

    show_center = True
    show_axes = True
    abs_system = CoordinateSystem(ax, color=(1, 0, 0), show_center=show_center, show_axes=show_axes)
    s1 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    s2 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    s3 = CoordinateSystem(ax, color=(0, 0, 0), show_center=show_center, show_axes=show_axes)
    abs_system.add("s1", s1)
    abs_system.add("s2", s2)
    abs_system.add("s3", s3)

    t = sp.Symbol('t')
    _time = np.linspace(0, 520, 10000)

    X_T = 5 * sp.cos(0.5 * t)
    Y_T = 6 * sp.sin(0.5 * t)
    PHI_T = 180 * sp.sin(0.8 * t) + 180
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
    # __x_t = X_T
    # __y_t = Y_T
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

    s1.add("point1", point1)
    s1.add("point2", point2)
    s1.add("point3", point3)
    s1.add("point4", point4)

    distance2 = 1
    point1 = ax.plot([0], [distance2], 'o')[0]
    point2 = ax.plot([-distance2], [0], 'o')[0]
    point3 = ax.plot([0], [-distance2], 'o')[0]
    point4 = ax.plot([distance2], [0], 'o')[0]

    s2.add("point1", point1)
    s2.add("point2", point2)
    s2.add("point3", point3)
    s2.add("point4", point4)

    distance3 = 2.3
    point1 = ax.plot([0], [distance3], 'o')[0]
    point2 = ax.plot([-distance3], [0], 'o')[0]
    point3 = ax.plot([0], [-distance3], 'o')[0]
    point4 = ax.plot([distance3], [0], 'o')[0]

    s3.add("point1", point1)
    s3.add("point2", point2)
    s3.add("point3", point3)
    s3.add("point4", point4)

    # @show_execution_time
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
        abs_system.rotate_to_local_angle("s1", PHI_T[i])
        # abs_system.get("s1").rotate_to_angle(PHI_T[i])   # s1.rotate_to_angle(PHI_T[i])

        k = 0.05
        abs_system.move_object("s2", [5 * np.cos(k * i), 6 * np.sin(k * i)])

        new_i = (i + 100) % 10000
        abs_system.move_object("s3", [X_T[new_i], Y_T[new_i]])
        abs_system["s3"].rotate_to_angle(0)         # s3.rotate_to_angle(0)

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
    show_axes = False
    s1 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)

    t = np.linspace(np.pi, 2 * np.pi, 127)
    track_radius = 5
    x_t = track_radius * np.cos(t)
    y_t = track_radius * np.sin(t)
    line, = ax.plot(x_t, y_t, "-", color=(0, 0, 0), lw=2)

    circle_radius = 0.8
    position = [0, -track_radius + circle_radius + 0.05]
    circle = plt.Circle(position, circle_radius, color=(0.3, 0.3, 0.8))
    s1.add("circle", circle)

    s2 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)

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
        angle = 80 * np.cos(coefficient * i)
        s1.rotate_to_angle(angle)
        s1.rotate_to_local_angle("s2", 30 * np.sin(coefficient * i))
        # s2.rotate_to_angle(30 * np.sin(coefficient * i) + angle)

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test3():
    # 30
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[0, 15], ylim=[0, 15])

    # Начальное расположение объектов, настройка зависимостей:
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
    PHI_T = -80 * sp.cos(coefficient * t)
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

    show_center = False     #  or True
    show_axes = False       #  or True
    acs = CoordinateSystem(ax, color=(0, 0, 0), show_center=show_center)

    # Добавляем кастомные оси чёрного цвета для удобства восприятия:
    ###
    line1, = ax.plot([0, 5], [0, 0], lw=0.8, color=(0, 0, 0))
    line2, = ax.plot([0, 0], [0, 5], lw=0.8, color=(0, 0, 0))
    acs.add("OX", line1)
    acs.add("OY", line2)
    ###

    line_length = 5             # Длина бордовых линий (можно изменить)
    distance_to_point1 = 4.2    # Расстояние до точки в системе s1 (можно изменить)
    distance_to_point2 = 2.8    # Расстояние до точки в системе s2 (можно изменить)

    # Настраиваем начальные положения систем координат:
    ###
    s1 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    line, = ax.plot([0, line_length], [0, 0], lw=3, color=(0.6, 0.2, 0.4))  # Бордовая линия в s1
    point, = ax.plot([distance_to_point1], [0], "*", color=(0, 0, 0))       # Точка для начала/конца пружины
    s1.add("line", line)
    s1.add("point", point)

    s2 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    line, = ax.plot([0, line_length], [0, 0], lw=3, color=(0.6, 0.2, 0.4))  # Бордовая линия в s2
    point, = ax.plot([distance_to_point2], [0], "*", color=(0, 0, 0))       # Точка для конца/начала пружины
    s2.add("line", line)
    s2.add("point", point)

    acs.add("s1", s1)
    acs.add("s2", s2)

    phi2 = 120
    phi1 = 30

    acs.rotate_to_local_angle("s1", phi2)
    acs.rotate_to_local_angle("s2", phi1)

    # Создаём систему координат для пружины
    s_spring = CoordinateSystem(ax, show_center=show_center, color=(0.5, 0.5, 0.5), show_axes=show_axes)

    # Добавляем пружину
    point1 = s1["point"].get_data()  # ([...], [...]) Точка начала/конца
    point2 = s2["point"].get_data()  # ([...], [...]) Точка конца/начала
    vector = [point1[0][0] - point2[0][0], point1[1][0] - point2[1][0]]
    distance = np.sqrt((vector[0]) ** 2 + (vector[1]) ** 2)     # Расстояние между точками - длина пружины
    vector = [vector[0] / distance, vector[1] / distance]       # Нормализуем вектор (на всякий)
    e_vector = [1, 0]
    alpha = np.arccos(vector[0] * e_vector[0] + vector[1] * e_vector[1]) * (180 / np.pi)    # Ищем угол наклона
    spring_xy = get_spring_line(distance, 15, 0.5)
    spring, = ax.plot(spring_xy[0], spring_xy[1], color=(0.5, 0.5, 0.5))    # Рисуем пружину

    s_spring.add("spring", spring)  # Добавляем график пружины в систему координат для пружины
    s_spring.move([point1[0][0], point1[1][0]])     # Переносим систему в точку point1
    s_spring.rotate_to_angle(alpha - 180)           # Поворот системы на необходимый угол

    acs.add("s_spring", s_spring)   # Добавляем в абсолютную систему
    ###

    def frame(i):
        coefficient1 = 0.01
        coefficient2 = 0.025
        _phi1 = 390 * ((np.sin(coefficient1 * i)) / 2)
        _phi2 = 335 * ((np.sin(-coefficient2 * i) + 0.8) / 2)

        # Повторяем действия при настройке начальных положений с некоторыми изменениями:
        ###
        acs.rotate_to_local_angle("s1", _phi2)  # Поворачиваем систему s1 на соответствующий угол
        acs.rotate_to_local_angle("s2", _phi1)  # Поворачиваем систему s2 на соответствующий угол
        _s_spring = acs["s_spring"]     # Получаем объект системы координат для пружины
        _point1 = acs["s1"]["point"].get_data()     # Получаем координаты точки начала/конца пружины
        _point2 = acs["s2"]["point"].get_data()     # Получаем координаты точки конца/начала пружины
        _vector = [_point1[0][0] - _point2[0][0], _point1[1][0] - _point2[1][0]]
        _distance = math.sqrt((_vector[0]) ** 2 + (_vector[1]) ** 2)    # Длина пружины
        _vector = [_vector[0] / _distance, _vector[1] / _distance]      # Нормализуем
        _e_vector = [1 * np.cos(acs.angle), 1 * np.sin(acs.angle)]      # Единичный вектор
        _alpha = np.arccos(_vector[0] * _e_vector[0] + _vector[1] * _e_vector[1]) * (180 / np.pi)   # Угол поворота

        # Создаём пружину уже повёрнутую на угол (_s_spring.angle), соответствующий текущему углу системы _s_spring
        _spring_xy = get_spring_line(_distance, 15, 0.5, pos=_s_spring.center, angle=_s_spring.angle,
                                     center=acs.center)
        _s_spring["spring"].set_data(_spring_xy)

        """
        _point1 = CoordinateSystem._rot2d(None, _point1[0][0], _point1[1][0], acs.angle, acs.center)
        _point2 = CoordinateSystem._rot2d(None, _point2[0][0], _point2[1][0], acs.angle, acs.center)
        _point1 = (np.array([_point1[0]]), np.array([_point1[1]]))
        _point2 = (np.array([_point2[0]]), np.array([_point2[1]]))
        """
        # Ищем точку с максимальным значением по y (тк иначе всё плохо работает, вероятно, из-за области \
        # значений функции np.arccos()), чтобы переместить туда систему координат пружины (_s_spring)
        new_xy = max(_point1, _point2, key=lambda mas: mas[1][0])
        new_x = new_xy[0]
        new_y = new_xy[1]
        if _point2 is new_xy:
            _alpha = -_alpha
        else:
            _alpha += 180

        acs.rotate_to_local_angle("s_spring", _alpha)   # Поворачиваем систему координат пружины на нужный угол
        new_pos_x = new_x - acs.x
        new_pos_y = new_y - acs.y
        acs.move_object("s_spring", [new_pos_x, new_pos_y])     # Перемещаем систему координат пружины в нужную точку

        # Меняем положение точки начала/конца пружины (можно закомментировать, тогда точка будет статичной)
        s1.move_object("point", [1.2 * distance_to_point1 * ((np.sin(0.06 * i) + 1.5) / 3), 0])
        ###

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test5():
    # 22
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    show_center = False     # or True
    show_axes = False       # or True

    acs = CoordinateSystem(ax, color=(0, 0, 0), show_center=True, show_axes=show_axes)
    s1 = CoordinateSystem(ax, center=(0, 0), show_center=show_center, show_axes=show_axes)
    s2 = CoordinateSystem(ax, center=(0, 0), show_center=show_center, show_axes=show_axes)

    # Инициализация начальных положений систем координат:
    ####################################################################################################################
    acs.add("s1", s1)

    radius1 = 4
    t = np.linspace(0, 2 * np.pi, 127)
    x = radius1 * np.cos(t)
    y = radius1 * np.sin(t)
    circle, = ax.plot(x, y, lw=3, color=(0.5, 0.5, 0.5))
    rect_width = 1.5
    rect_height = 0.4
    rectangle1 = plt.Rectangle([0 - rect_width / 2, radius1], width=rect_width, height=rect_height,
                               color=(0.5, 0.5, 0.5))
    rectangle2 = plt.Rectangle([radius1 + rect_height, 0 - rect_width / 2],
                               width=rect_width, height=rect_height, angle=90,
                               color=(0.5, 0.5, 0.5))
    rectangle3 = plt.Rectangle([0 - rect_width / 2, -radius1 - rect_height], width=rect_width, height=rect_height,
                               color=(0.5, 0.5, 0.5))
    rectangle4 = plt.Rectangle([-radius1, 0 - rect_width / 2],
                               width=rect_width, height=rect_height, angle=90,
                               color=(0.5, 0.5, 0.5))
    s1.add("circle", circle)
    s1.add("rectangle1", rectangle1)
    s1.add("rectangle2", rectangle2)
    s1.add("rectangle3", rectangle3)
    s1.add("rectangle4", rectangle4)
    s1.add("s2", s2)

    line_length = 3
    line, = ax.plot([0, 0], [0, -line_length], lw=2, color=(0, 0, 0))
    radius2 = 0.7
    small_circle = plt.Circle([0, -line_length], radius2, color=(0, 0, 0))
    small_circle.set_zorder(2)  # Чтобы круг рисовался поверх других объектов
    distance = 0.55  # От расстояния до точки будет зависеть размер спиральной пружины
    point, = ax.plot([s2.x], [s2.y - distance])
    s2.add("lineAB", line)
    s2.add("small_circle", small_circle)
    s2.add("point", point)
    s2.move([-2, 1])

    position = s2["point"].get_data()
    pos_x = position[0][0]
    pos_y = position[1][0]
    coils = 2
    spiral_spring = SpiralSpring(ax, s2.center, [pos_x, pos_y], coils, color=(0.4, 0.3, 0.2))
    ####################################################################################################################

    def frame(i):
        phi = 3 * i
        psi = 30 * np.sin(0.1 * i)

        # Поворот системы s1 на угол phi
        acs.rotate_to_local_angle("s1", phi)

        # Поворот системы s2 на угол psi
        acs["s1"]["s2"].rotate_to_angle(psi)

        acs.move([3 * np.sin(0.01 * i), 3 * np.cos(0.01 * i)])  # Не обязательно

        # Отрисовка спиральной пружины
        _position = s2["point"].get_data()
        _pos_x = _position[0][0]
        _pos_y = _position[1][0]
        spiral_spring.update(acs["s1"]["s2"].center, [_pos_x, _pos_y])

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test6():
    # 39
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])
    show_center = False     # or True
    show_axes = False       # or True

    acs = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    s1 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    s2 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)

    black = (0, 0, 0)
    line_width = 2

    length1 = 5
    length2 = 0.7
    rect_width = 1.5
    rect_height = 0.7
    rect_color = (0.3, 0.3, 0.8)

    spring_coils = 8
    spring_diameter = 0.5

    def init_s1():
        wide_line, = ax.plot([-length1 / 2, length1 / 2], [0, 0], lw=line_width, color=black)
        short_line1, = ax.plot([-length1 / 2, -length1 / 2], [0, length2], lw=line_width, color=black)
        short_line2, = ax.plot([length1 / 2, length1 / 2], [0, length2], lw=line_width, color=black)

        rectangle = plt.Rectangle([0 - rect_width / 2, 0], width=rect_width, height=rect_height, color=rect_color)

        spring_color = (0.6, 0.6, 0.6)

        s1.add("wide_line", wide_line)
        s1.add("short_line1", short_line1)
        s1.add("short_line2", short_line2)
        s1.add("rectangle", rectangle)
        spring_xy = get_spring_line(abs(length1 / 2 - rect_width / 2), spring_coils, spring_diameter,
                                    pos=[-length1 / 2, length2 / 2])
        s1.add("spring1", ax.plot(spring_xy[0], spring_xy[1], color=spring_color, zorder=-1)[0])
        spring_xy = get_spring_line(abs(length1 / 2 - rectangle.xy[0] - rect_width), spring_coils, spring_diameter,
                                    pos=[rect_width / 2, length2 / 2])
        s1.add("spring2", ax.plot(spring_xy[0], spring_xy[1], color=spring_color, zorder=-1)[0])

        length = 6
        s1.move([0, length])
        line, = ax.plot([0, 0], [0, length], lw=line_width, color=black)
        s1.add("line", line)

    def init_s2():
        s2.add("s1", s1)

    def init_acs():
        acs.add("s2", s2)

    init_s1()   # Инициализация начального положения системы s1
    init_s2()   # Инициализация начального положения системы s2
    init_acs()  # Инициализация начального положения абсолютной системы координат acs

    def frame(i):
        x_t = -(length1 / 2 - rect_width) * np.sin(0.07 * i) - rect_width / 2

        phi = 90 * (np.sin(0.02 * i))

        # Сначала двигаем прямоугольник, иначе появляется задержка у пружин
        s1.move_object("rectangle", [x_t, 0])

        # Ищем позиции ключевых точек
        xy = s1["short_line1"].get_data()
        pos1 = ((xy[0][0] + xy[0][1]) / 2, (xy[1][0] + xy[1][1]) / 2)
        xy = s1["short_line2"].get_data()
        pos3 = ((xy[0][0] + xy[0][1]) / 2, (xy[1][0] + xy[1][1]) / 2)
        corners = s1["rectangle"].get_corners()
        pos2 = ((corners[1][0] + corners[2][0]) / 2, (corners[1][1] + corners[2][1]) / 2)
        pos4 = ((corners[0][0] + corners[3][0]) / 2, (corners[0][1] + corners[3][1]) / 2)

        # Ищем длину левой и правой пружин
        first_length = np.sqrt((pos1[0] - pos4[0]) ** 2 + (pos1[1] - pos4[1]) ** 2)
        second_length = np.sqrt((pos2[0] - pos3[0]) ** 2 + (pos2[1] - pos3[1]) ** 2)

        # Изменяем положения пружин
        epsilon = 0.02  # Чтоб прям красиво было
        spring_xy = get_spring_line(first_length - epsilon, spring_coils, spring_diameter,
                                    pos=pos1, angle=acs["s2"].angle)
        s1["spring1"].set_data(spring_xy)

        spring_xy = get_spring_line(second_length, spring_coils, spring_diameter,
                                    pos=(pos2[0] + epsilon, pos2[1]), angle=acs["s2"].angle)
        s1["spring2"].set_data(spring_xy)

        # Поворачиваем систему s2 на угол phi
        acs.rotate_to_local_angle("s2", phi)

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test7():
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    ax.plot([0, 0], [-10, 10], "--", lw=1)

    show_center = False     # or True
    show_axes = False       # or True
    acs = CoordinateSystem(ax, color=(1, 0, 0), show_center=show_center, show_axes=show_axes)
    s1 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    s2 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)

    radius1 = 0.2
    circle1 = plt.Circle((0, 0), radius1, color=(0, 0, 0))
    s1.add("point", circle1)

    line1_length = 1
    line2_length = 3
    s1.move([0, line1_length + line2_length])

    abs_line, = ax.plot([0, 0], [line1_length, line1_length + line2_length], lw=5, color=(0, 0, 0))
    s1.add("abs_line", abs_line)

    line, = ax.plot([0, 0], [0, line1_length], lw=5, color=(0, 0, 0))
    radius2 = 0.2
    circle2 = plt.Circle((0, line1_length), radius2, color=(0, 0, 0))
    s2.add("line", line)
    s2.add("point", circle2)

    acs.add("s1", s1)
    acs.add("s2", s2)
    # acs.add("abs_line", abs_line)

    def frame(i):
        alpha1 = (180 * (0.05 * i) + 90) % 360
        acs.rotate_to_local_angle("s2", alpha1)

        curX, curY = acs["s2"]["point"].center
        curX, curY = curX - acs.x, curY - acs.y
        newX = 0
        newY = np.sqrt(line2_length ** 2 - curX ** 2) + curY
        alpha = -(180 / np.pi) * np.arcsin((line1_length / line2_length) * np.sin((np.pi / 180) * alpha1))

        acs.move_object("s1", [newX, newY])
        acs.rotate_to_local_angle("s1", alpha)

        # !!! acs.move([3 * np.sin(0.01 * i), 3 * np.cos(0.01 * i)])
        # !!! acs.rotate(-np.pi / 180)

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test8():
    # 21
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[-15, 15], ylim=[-15, 15])

    show_center = False     # or True
    show_axes = False       # or True
    acs = CoordinateSystem(ax, color=(0, 0, 0), show_center=show_center, show_axes=show_axes)
    s1 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    s2 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    s_disk = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    lengthAB = 8
    lengthA1A = 5
    line_width = 5
    black = (0, 0, 0)

    s1.add("A1A", ax.plot([0, 0], [0, -lengthA1A], lw=line_width, color=black))
    s1.add("pointA", ax.plot([0], [-lengthA1A], "o", color=(0, 0, 0)))
    s2.add("B1B", ax.plot([0, 0], [0, -lengthA1A], lw=line_width, color=black))
    s2.add("pointB", ax.plot([0], [-lengthA1A], "o", color=(0, 0, 0)))
    s1.move([-lengthAB / 2, 2])
    s2.move([lengthAB / 2, 2])

    lengthOC = 3
    disk_radius = 2
    s_disk.add("lineOC", ax.plot([0, 0], [0, -lengthOC], lw=2, color=black))
    s_disk.add("pointC", ax.plot([0], [-lengthOC]))
    s_disk.add("disk", plt.Circle((0, -lengthOC), disk_radius, color=(*black, 0.2)))
    s_disk.move([0, 2 - lengthA1A])

    lineAB = ax.plot([-lengthAB / 2, lengthAB / 2], [2 - lengthA1A, 2 - lengthA1A], lw=line_width, color=black)

    acs.add("s1", s1)
    acs.add("s2", s2)
    acs.add("s_disk", s_disk)
    acs.add("lineAB", lineAB)

    # @show_execution_time
    def frame(i):
        phi = 70 * np.sin(0.05 * i)
        theta = 40 * np.sin(0.05 * (i - 15))

        acs.rotate_to_local_angle("s1", phi)
        acs.rotate_to_local_angle("s2", phi)

        pointA = acs["s1"]["pointA"].get_data()
        pointB = acs["s2"]["pointB"].get_data()
        new_x = pointA[0][0], pointB[0][0]
        new_y = pointA[1][0], pointB[1][0]
        center = (new_x[0] + new_x[1]) / 2, (new_y[0] + new_y[1]) / 2

        acs["s_disk"].move(center)
        acs.rotate_to_local_angle("s_disk", theta)
        acs["lineAB"].set_data(new_x, new_y)

        acs.move([5 * np.cos(0.01 * i), 3 * np.sin(0.01 * i)])
    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test_spiral_spring():
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])
    show_center = True
    show_axes = True
    acs = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)

    coordinates1 = [1, 0]

    s1 = CoordinateSystem(ax, show_center=show_center, show_axes=show_axes)
    point, = ax.plot([coordinates1[0]], [coordinates1[1]], "o")
    s1.add("point", point)

    coils = 2
    spiral_spring = SpiralSpring(ax, [0, 0], coordinates1, coils)

    acs.add("s1", s1)

    def frame(i):
        acs["s1"].rotate_to_angle(-670 * (np.sin(0.03 * i) - 570))
        acs.move_object("s1", [3 * np.sin(0.02 * i), 3 * np.cos(0.02 * i)])
        acs.move([3 * np.cos(0.02 * i), 3 * np.sin(0.02 * i)])

        new_pos = acs["s1"]["point"].get_data()
        new_x = new_pos[0][0]
        new_y = new_pos[1][0]
        spiral_spring.update(acs["s1"].center, [new_x, new_y])

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()


def test228():
    figure = plt.figure(figsize=(8, 8))
    ax = figure.add_subplot(1, 1, 1)
    ax.set(xlim=[0, 15], ylim=[0, 15])

    show_center = False
    show_axes = False
    s1 = CoordinateSystem(ax, (4.5, 2.5), show_center=show_center, show_axes=show_axes)
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

    s2 = CoordinateSystem(ax, (0 + 0.1, 2.5 + stick_height / 2), show_center=show_center, show_axes=show_axes)
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


def test_rotate_to_local_angle():
    figure = plt.figure(figsize=[8, 8])
    ax = figure.add_subplot()
    ax.set(xlim=[-10, 10], ylim=[-10, 10])

    acs = CoordinateSystem(ax, color=(0, 0, 0))
    line1, = ax.plot([0, 5], [0, 0], lw=0.8, color=(0, 0, 0))
    line2, = ax.plot([0, 0], [0, 5], lw=0.8, color=(0, 0, 0))
    acs.add("OX", line1)
    acs.add("OY", line2)

    s1 = CoordinateSystem(ax)
    line1, = ax.plot([0, 3], [0, 0], lw=0.8, color=(1, 0, 0))
    line2, = ax.plot([0, 0], [0, 3], lw=0.8, color=(0, 0, 1))
    s1.add("OX", line1)
    s1.add("OY", line2)
    s1.move([1, 1])

    acs.add("s1", s1)

    def frame(i):
        acs.rotate_to_local_angle("s1", 45 * np.sin(0.01 * i))

        acs.rotate(np.pi / 360)
        acs.move([3 * np.cos(0.05 * i), 3 * np.sin(0.05 * i)])

    _ = FuncAnimation(figure, frame, interval=20, frames=12000)
    plt.show()
