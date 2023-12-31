import pygame as pg


def set_border_offset(offset: int):
    PuzzleTile.border_offset = offset


def set_tile_size(size: int):
    PuzzleTile.tile_size = size


class PuzzleTile:
    border_offset = 0
    tile_size = 0

    def __init__(self, image: pg.Surface):
        self.image = image

    def draw(self, surface: pg.Surface, x_pos: int, y_pos: int):
        surface.blit(
            self.image,
            (
                PuzzleTile.border_offset + x_pos * PuzzleTile.tile_size,
                PuzzleTile.border_offset + y_pos * PuzzleTile.tile_size,
            ),
        )
