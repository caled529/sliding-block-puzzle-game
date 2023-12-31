from os import environ

# Disables the PyGame startup message.
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import puzzle_tile
from puzzle_tile import PuzzleTile
import pygame as pg
import random as rnd


def cheat_surface(ord: int, size: int) -> pg.Surface:
    temp_surf = pg.Surface([size, size])
    temp_surf.fill(
        pg.color.Color(rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
    )
    temp_surf.blit(
        pg.font.SysFont("Calibri", 30).render(str(ord), False, (0, 0, 0)),
        (size / 2 - 10, size / 2 - 15),
    )
    return temp_surf


def render_board(
    target: pg.Surface, board: list[PuzzleTile | None], board_dimension: int
):
    target.fill(pg.color.Color(0, 0, 0))
    for i in range(len(board)):
        if board[i]:
            y_pos, x_pos = divmod(i, board_dimension)
            board[i].draw(target, x_pos, y_pos)
    pg.display.flip()


def main():
    WIN_WIDTH = 640
    WIN_HEIGHT = 640
    PUZZLE_DIMENSIONS = 3

    pg.init()
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    puzzle_tile.set_border_offset(int(WIN_WIDTH / 8))
    puzzle_tile.set_tile_size(int(3 * WIN_WIDTH / 4 / PUZZLE_DIMENSIONS))

    tiles = []
    for i in range(PUZZLE_DIMENSIONS**2 - 1):
        tiles.append(PuzzleTile(cheat_surface(i + 1, PuzzleTile.tile_size)))
    tiles.append(None)
    rnd.shuffle(tiles)

    render_board(screen, tiles, PUZZLE_DIMENSIONS)

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                BORDER_OFFSET = PuzzleTile.border_offset
                mouse_x, mouse_y = pg.mouse.get_pos()
                if mouse_x in range(
                    BORDER_OFFSET, WIN_WIDTH - BORDER_OFFSET
                ) and mouse_y in range(BORDER_OFFSET, WIN_HEIGHT - BORDER_OFFSET):
                    grid_x = int((mouse_x - BORDER_OFFSET) / PuzzleTile.tile_size)
                    grid_y = int((mouse_y - BORDER_OFFSET) / PuzzleTile.tile_size)
                    grid_pos = grid_x + grid_y * PUZZLE_DIMENSIONS
                    adjacent_positions = (
                        grid_pos - PUZZLE_DIMENSIONS,
                        grid_pos - 1,
                        grid_pos + 1,
                        grid_pos + PUZZLE_DIMENSIONS,
                    )
                    for adj_pos in adjacent_positions:
                        if adj_pos >= 0 and adj_pos < len(tiles):
                            if not tiles[adj_pos]:
                                tiles[adj_pos] = tiles[grid_pos]
                                tiles[grid_pos] = None
                                break
                render_board(screen, tiles, PUZZLE_DIMENSIONS)
            if event.type == pg.QUIT or event.type == pg.KEYDOWN:
                running = False
    pg.quit()


main()
