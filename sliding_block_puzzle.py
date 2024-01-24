from os import environ

# Disables the PyGame startup message.
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from puzzle_board import PuzzleBoard
import pygame as pg


def gen_image(size: int) -> pg.Surface:
    image = pg.Surface((size, size))
    for i in range(size):
        for j in range(size):
            red = 255 - (i + j) * 128 // size
            green = i * 256 // size
            blue = j * 256 // size
            image.set_at((i, j), pg.color.Color(red, green, blue))
    return image


def draw(target: pg.Surface, board: PuzzleBoard, border_offset: int):
    target.fill(pg.color.Color(0, 0, 0))
    target.blit(board.render_board(), (border_offset, border_offset))
    pg.display.flip()


def main():
    WIN_RES = 640
    BORDER_OFFSET = 50

    pg.init()

    screen = pg.display.set_mode((WIN_RES, WIN_RES))
    board = PuzzleBoard(4, WIN_RES - 2 * BORDER_OFFSET, gen_image(WIN_RES))
    running = True

    draw(screen, board, BORDER_OFFSET)

    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if mouse_x in range(
                    BORDER_OFFSET, WIN_RES - BORDER_OFFSET
                ) and mouse_y in range(BORDER_OFFSET, WIN_RES - BORDER_OFFSET):
                    board.handle_click(mouse_x - BORDER_OFFSET, mouse_y - BORDER_OFFSET)
            if event.type == pg.QUIT or event.type == pg.KSCAN_ESCAPE:
                running = False
        draw(screen, board, BORDER_OFFSET)

    pg.quit()


main()
