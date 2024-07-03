import curses
import random
import time

def draw_ground(stdscr, ground_y):
    """Рисует землю на заданной высоте"""
    sh, sw = stdscr.getmaxyx()
    for x in range(sw):
        stdscr.addch(ground_y, x, '-')

def create_raindrop_effect(stdscr, y, x):
    """Создает эффект брызг от падения капли"""
    splash_chars = ['.', ',', '\'']
    offsets = [(-1, 0), (0, -1), (0, 1)]
    sh, sw = stdscr.getmaxyx()
    for i, (dy, dx) in enumerate(offsets):
        ny, nx = y + dy, x + dx
        if 0 <= ny < sh and 0 <= nx < sw:
            stdscr.addch(ny, nx, splash_chars[i % len(splash_chars)])

def create_lightning(stdscr, ground_y):
    """Создает молнию с непредсказуемым узором"""
    sh, sw = stdscr.getmaxyx()
    lightning_path = [(0, random.randint(0, sw - 1))]
    while lightning_path[-1][0] < ground_y - 1:
        y, x = lightning_path[-1]
        next_step = (y + 1, x + random.choice([-1, 0, 1]))
        next_step = (next_step[0], max(0, min(sw - 1, next_step[1])))
        lightning_path.append(next_step)

    for y, x in lightning_path:
        stdscr.addch(y, x, '*')
        stdscr.refresh()
        time.sleep(0.001)  # Уменьшение задержки для ускорения анимации молнии

    time.sleep(0.01)  # Задержка, чтобы молния была видна
    for y, x in lightning_path:
        if 0 <= y < sh and 0 <= x < sw:
            stdscr.addch(y, x, ' ')  # Стираем молнию

def create_rain(stdscr, num_drops=100):
    """Создает анимацию дождя"""
    curses.curs_set(0)  # Скрыть курсор
    stdscr.nodelay(1)   # Не блокировать ввод при ожидании
    stdscr.timeout(50)  # Установить таймаут для ввода

    sh, sw = stdscr.getmaxyx()  # Получить размеры экрана
    ground_y = sh - 2  # Уровень земли
    drops = []

    # Создать начальные капли дождя
    for _ in range(num_drops):
        x = random.randint(0, sw - 1)
        y = random.randint(0, ground_y - 1)
        drops.append((y, x))

    while True:
        stdscr.clear()  # Очистить экран

        # Рисовать землю
        draw_ground(stdscr, ground_y)

        # Обновить позиции капель дождя
        new_drops = []
        for y, x in drops:
            stdscr.addch(y, x, '|')  # Нарисовать каплю дождя
            if y < ground_y - 1:
                new_y = y + 1  # Переместить каплю вниз
                new_drops.append((new_y, x))
            else:
                create_raindrop_effect(stdscr, y, x)  # Создать эффект брызг
                new_y = 0  # Возвратить каплю наверх
                new_drops.append((new_y, x))

        drops = new_drops

        # Случайно создаем молнию
        if random.random() < 0.09:  # Вероятность появления молнии
            create_lightning(stdscr, ground_y)

        stdscr.refresh()  # Обновить экран
        time.sleep(0.1)   # Пауза для создания эффекта анимации

        # Выход при нажатии клавиши
        if stdscr.getch() != -1:
            break

def main():
    curses.wrapper(create_rain)

if __name__ == "__main__":
    main()
