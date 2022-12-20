import math
import matplotlib.pyplot as plt

t = 3360  # время полета в секундах

# массивы значений
corner_arr = [0] * t  # массив угла наклона ракеты в каждую секунду полета, градусы?
mass_total_arr = [0] * t  # массив веса ракеты в каждую секунду полета, кг
mass_1_stage_arr = [0] * t  # массив веса первой ступени ракеты в каждую секунду полета, кг
mass_2_stage_arr = [0] * t  # массив веса второй ступени ракеты в каждую секунду полета, кг
time_arr = list(range(1, t + 1))  # массив времени, сек
specific_impulse_1_stage_arr = [0] * 1001
height_arr = list(range(0, 100100, 100))  # массив высоты (от 1 до 100000 с шагом 100), метры
velocity_arr = [0] * t  # массив скорости ракеты в каждую секунду полета, м/сек

# константы
pi = math.pi  # число пи
p0 = 101325  # стандартное атмосферное давление на уровне моря
cp = 1004.685  # удельная теплоёмкость при постоянном давлении
t0 = 288.16  # стандартная температура на уровне моря
m = 0.029  # молярная масса сухого воздуха
r0 = 8.31  # универсальная газовая постоянная
g0 = 9.81  # коэффициент ускорения свободного падения

# параметры ракеты
mass_total = 549000  # общий вес ракеты, кг
mass_1_stage = 421300  # вес заправленной первой ступени, кг
mass_2_stage = 96670  # вес заправленной второй ступени, кг
M0 = 31130  # вес ракеты без ступеней (общая полезная нагрузка), кг

# параметры двигателей
P0 = 845000  # расчетная тяга двигателя, когда давление на выходе сопла совпадает с давлением газа окружающей среды, Н
ve = 3070  # выходная скорость
pe = 1.5  # выходное давление
ae = 6.91  # площадь сопла
imp1 = 283  # удельный импульс двигателя первой ступени на уровне моря
imp2 = 348  # удельный импульс двигателя второй ступени для вакуума
net_flow_rate_stage1 = (421300 - 25600) / 162  # расход топлива первой ступени, кг/сек  ~2442
net_flow_rate_stage2 = (96670 - 3900) / 383  # расход топлива второй ступени, кг/сек


def mass():
    global mass_total_arr, mass_1_stage_arr, mass_2_stage_arr, time_arr
    global mass_total, mass_1_stage, mass_2_stage, net_flow_rate_stage1, net_flow_rate_stage2

    # первая ступень работает
    for i in range(0, 163):
        mass_total -= net_flow_rate_stage1
        mass_1_stage -= net_flow_rate_stage1
        mass_total_arr[i] = mass_total
        mass_1_stage_arr[i] = mass_1_stage
        mass_2_stage_arr[i] = mass_2_stage

    # отстыковка первой ступени
    mass_total -= 25600
    mass_1_stage = 0
    for i in range(163, 170):
        mass_total_arr[i] = mass_total
        mass_1_stage_arr[i] = mass_1_stage
        mass_2_stage_arr[i] = mass_2_stage

    # вторая ступень работает 1
    for i in range(170, 493):
        mass_total -= net_flow_rate_stage2
        mass_2_stage -= net_flow_rate_stage2
        mass_total_arr[i] = mass_total
        mass_1_stage_arr[i] = mass_1_stage
        mass_2_stage_arr[i] = mass_2_stage

    # двигатели выключены
    for i in range(493, 1720):
        mass_total_arr[i] = mass_total
        mass_1_stage_arr[i] = mass_1_stage
        mass_2_stage_arr[i] = mass_2_stage

    # вторая ступень работает 2
    for i in range(1720, 1781):
        mass_total -= net_flow_rate_stage2
        mass_2_stage -= net_flow_rate_stage2
        mass_total_arr[i] = mass_total
        mass_1_stage_arr[i] = mass_1_stage
        mass_2_stage_arr[i] = mass_2_stage

    # двигатели выключены
    for i in range(1781, 3346):
        mass_total_arr[i] = mass_total
        mass_1_stage_arr[i] = mass_1_stage
        mass_2_stage_arr[i] = mass_2_stage

    # отстыковка второй ступени
    mass_total -= 25600
    mass_2_stage = 0
    for i in range(3346, t):
        mass_total_arr[i] = mass_total
        mass_1_stage_arr[i] = mass_1_stage
        mass_2_stage_arr[i] = mass_2_stage

    fig, mass_total = plt.subplots()
    mass_total.set_title('Изменение массы ракеты')
    mass_total.set_xlabel('Время, секунды')
    mass_total.set_ylabel('Масса, килограммы')
    mass_total.plot(time_arr, mass_total_arr)
    mass_total.plot(time_arr, mass_1_stage_arr)
    mass_total.plot(time_arr, mass_2_stage_arr)
    mass_total.grid()


def specific_impulse_1_stage():
    global specific_impulse_1_stage_arr, height_arr
    global p0, cp, t0, m, r0, g0, ve, pe, ae, net_flow_rate_stage1

    for i in range(len(height_arr)):
        h = height_arr[i]
        pa = p0 * pow(1 - (g0 * h) / (cp * t0), (cp * m / r0))  # давление окружающего воздуха
        thrust = net_flow_rate_stage1 * ve + (pe - pa) * ae  # реактивная тяга
        imp = thrust / (net_flow_rate_stage1 * g0)  # удельный импульс
        specific_impulse_1_stage_arr[i] = imp

    fig, specific_impulse = plt.subplots()
    specific_impulse.set_title('Изменение удельного импульса 1 ступени')
    specific_impulse.set_xlabel('Удельный импульс, секунды')
    specific_impulse.set_ylabel('Высота, метры')
    specific_impulse.plot(specific_impulse_1_stage_arr[:250], height_arr[:250])
    specific_impulse.grid()


def velocity():
    global M0, imp1, imp2
    velocity_cur = 0  # текущая скорость

    for i in range(1, t):
        if i < 162:  # первая ступень работает
            delta_v = imp1 * g0 * math.log(((M0 + mass_1_stage_arr[i - 1] + mass_2_stage_arr[i - 1]) /
                                            (M0 + mass_1_stage_arr[i] + mass_2_stage_arr[i])), math.e)
            velocity_cur += delta_v
            velocity_cur = max(0, velocity_cur)
            velocity_arr[i] = velocity_cur

        elif 170 <= i < 493 or 1720 <= i < 1781:  # вторая ступень работает
            delta_v = imp2 * g0 * math.log(((M0 + mass_2_stage_arr[i - 1]) / (M0 + mass_2_stage_arr[i])), math.e)
            velocity_cur += delta_v
            velocity_arr[i] = velocity_cur

        else:  # двигатели отключены
            velocity_cur -= 0.05
            velocity_arr[i] = velocity_cur

    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение скорости')
    velocity_cur.set_ylabel('Скорость, метры в секунду')
    velocity_cur.set_xlabel('Время в секунды')
    velocity_cur.plot(time_arr, velocity_arr)
    velocity_cur.grid()


def corner():
    global time_arr, corner_arr
    # for i in range(1, len(time_arr)):
    for i in range(len(time_arr)):
        if i < 325:
            corner_arr[i] = - ((i - 325) * (i - 325)) / (325 * 325) + 1
        else:
            # corner_arr[i] = math.cos(90)# * pi
            corner_arr[i] = 1

            # corner =/If[t < 140, (t / 300) * pi, (14 / 30) * pi];

    fig, corner = plt.subplots()
    corner.set_title('Изменение угла наклона ракеты')
    corner.set_ylabel('Угол наклона ракеты')
    corner.set_xlabel('Время в секунды')
    corner.plot(time_arr[:1000], corner_arr[:1000])
    corner.grid()


mass()
specific_impulse_1_stage()
velocity()
corner()

plt.show()
