import curses
import time
from art import text2art

def main(stdscr):
    # Отключение курсора
    curses.curs_set(0)

    # Инициализация цветовых пар
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Текст для отображения
    text = "JAHAMARS"
    ascii_art = text2art(text, font='def-leppard')
    ## def-leppard, rozzo, frakture
    effects = {
        "blink": False,
        "gradient": False,
        "speed": 0.03
    }

    start_x = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Применение эффектов
        if effects.get("blink", False):
            if int(time.time() * 2) % 2 == 0:
                display_text = ascii_art
            else:
                display_text = " " * len(ascii_art)
        else:
            display_text = ascii_art

        if effects.get("gradient", False):
            for y, line in enumerate(display_text.split('\n')):
                for x, char in enumerate(line):
                    color_pair = curses.color_pair((x % 7) + 1)
                    if y + height // 2 < height:
                        stdscr.addstr(y + height // 2, (start_x + x) % width, char, color_pair)
        else:
            for y, line in enumerate(display_text.split('\n')):
                if y + height // 2 < height:
                    stdscr.addstr(y + height // 2, start_x % width, line)

        stdscr.refresh()

        # Сдвиг текста
        start_x -= 1

        time.sleep(effects["speed"])

if __name__ == "__main__":
    curses.wrapper(main)
