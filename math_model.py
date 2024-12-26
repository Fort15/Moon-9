import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Исходные данные для второго графика
F0 = 7938880  # Начальная тяга
beta = -12021  # Коэффициент возрастания тяги
C = 0.4  # Сопротивление воздуха
S = 83.28  # Площадь лобовой поверхности
p = 1.2255  # Плотность воздуха
phi = np.radians(75)  # Начальный угол (в радианах)
m0 = 415628  # Масса ракеты
k = 2909  # Расход топлива в секунду

G = 6.67430 * 10**-11  # Гравитационная постоянная
M = 5.29151 * 10**22  # Масса Кербина
R = 600000  # Радиус Кербина

# Начальные условия
h = [78]  # Начальная высота
v = 100  # Начальная скорость
dt = 1  # Шаг времени
t_max = 285  # Максимальное время

# Функции ускорений
def ax(t, v, phi):
    m = m0 - k * t  # Текущая масса
    return ((F0 + beta * t) * np.cos(phi) - 0.5 * C * S * p * v**2 * np.cos(phi)) / m

def ay(t, v, phi, h):
    m = m0 - k * t  # Текущая масса
    g = G * M / (h + R)**2  # Гравитационное ускорение
    return ((F0 + beta * t) * np.sin(phi) - 0.5 * C * S * p * v**2 * np.sin(phi)) / m - g

# Массивы для времени и высоты
time = np.arange(0, t_max, dt)
heights = []

# Цикл расчёта
for t in time:
    if t == 89:                       # 11 --> 10
        beta = 151000
        m = 150000
        k = 1234
    if t == 148:                      # 10 --> 9
        m = 71000
        beta = 11000
        k = 230

    # Вычисляем текущие ускорения
    a_x = ax(t, v, phi)
    a_y = ay(t, v, phi, h[-1])

    # Обновляем скорость и высоту
    v_x = v * np.cos(phi) + a_x * dt
    v_y = v * np.sin(phi) + a_y * dt
    v = np.sqrt(v_x**2 + v_y**2)  # Полная скорость
    h_new = h[-1] + v_y * dt
    h.append(h_new)

    # Записываем текущую высоту
    heights.append(h_new)

# Загрузка данных из CSV файла для первого графика
file_path = 'РН Молния (Луна-9)_20241226113553.csv'  # Укажите путь к вашему CSV файлу
data = pd.read_csv(file_path)

# Фильтрация данных до 250 секунд для первого графика
filtered_data = data[data['TimeSinceMark'] <= t_max]

# Построение графиков на одном рисунке
plt.figure(figsize=(12, 6))

# График из CSV файла
plt.plot(filtered_data['TimeSinceMark'], filtered_data['AltitudeASL'], label='KSP', color='red')

# График расчетов
plt.plot(time, heights, label='Расчеты', color='green')

# Настройка осей и легенды
plt.xlabel('Время (с)', fontsize=14)
plt.ylabel('Высота (м)', fontsize=14)
plt.grid(True)
plt.legend(fontsize=12)

plt.title('Сравнение высоты от времени', fontsize=16)
plt.xlim(0, t_max)  # Ограничение по оси X до максимального времени
plt.tight_layout()   # Убираем лишние отступы

plt.savefig('my_plot.png', dpi=300)  # Сохраняет график в файл
