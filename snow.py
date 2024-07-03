import curses
import random
import time

def create_star_field(stdscr, num_stars=100):
    curses.curs_set(0)  # Скрыть курсор
    stdscr.nodelay(1)   # Не блокировать ввод при ожидании
    stdscr.timeout(50)  # Установить таймаут для ввода

    sh, sw = stdscr.getmaxyx()  # Получить размеры экрана
    stars = []
    settled_stars = {}

    while True:
        stdscr.clear()  # Очистить экран

        # Создать новые звезды на верхней части экрана
        for _ in range(num_stars // 10):  # Добавлять звезды постепенно
            x = random.randint(0, sw - 1)
            y = 0
            char = random.choice(['*', '+', '.', 'o'])
            stars.append((y, x, char))

        # Обновить позиции звезд
        new_stars = []
        for y, x, char in stars:
            if (y, x) not in settled_stars:
                if 0 <= y < sh and 0 <= x < sw:  # Проверка координат
                    try:
                        stdscr.addch(y, x, char)  # Нарисовать звезду
                    except curses.error as e:
                        print(f"Error drawing star at ({y}, {x}): {e}")
                new_y = y + 1  # Переместить звезду вниз
                if new_y == sh:  # Если звезда достигла нижней части экрана
                    if x not in settled_stars:
                        settled_stars[x] = 0
                    settled_stars[x] += 1
                else:
                    new_stars.append((new_y, x, char))

        stars = new_stars

        # Нарисовать осевшие звезды
        for x, layers in settled_stars.items():
            for layer in range(layers):
                y = sh - 1 - layer
                if 0 <= y < sh and 0 <= x < sw:  # Проверка координат
                    try:
                        stdscr.addch(y, x, '*')
                    except curses.error as e:
                        print(f"Error drawing settled star at ({y}, {x}): {e}")

        stdscr.refresh()  # Обновить экран
        time.sleep(0.1)   # Пауза для создания эффекта анимации

        # Выход при нажатии клавиши
        if stdscr.getch() != -1:
            break

def main():
    curses.wrapper(create_star_field)

if __name__ == "__main__":
    main()
