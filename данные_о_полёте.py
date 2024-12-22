import csv

# Инициализация списков для хранения данных
time_since_mark = []
mass = []
altitude_asl = []
speed_surface = []

# Открытие CSV файла и чтение данных
with open('РН Молния (Луна-9)_20241222231842.csv', mode='r', newline='') as csvfile:
    reader = csv.reader(csvfile)

    # Пропускаем заголовок
    next(reader)

    # Чтение строк и добавление значений в соответствующие списки
    for row in reader:
        time_since_mark.append(float(row[0]))
        mass.append(float(row[6]) * 1000)  # Преобразуем тонны в килограммы
        altitude_asl.append(float(row[2]))
        speed_surface.append(float(row[4]))

t = 0
# Вывод данных в каждую целую секунду
for i in range(len(time_since_mark)):
    # Проверяем, является ли время целым числом
    if int(time_since_mark[i]) == t:
        t += 1
        print(
            f"Time: {int(time_since_mark[i])}s, Mass: {mass[i]} tonn, Altitude: {altitude_asl[i]} m, Speed: {speed_surface[i]} m/s")
