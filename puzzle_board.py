from pygame import Surface
from random import choice


class PuzzleBoard:
    def __init__(self, dimension: int, resolution: int, image: Surface):
        self.DIMENSION = dimension
        self.RESOLUTION = resolution
        self.TILE_SIZE = resolution // dimension
        self.__generate_tiles(image.subsurface((0, 0), (resolution, resolution)))
        self.__shuffle_tiles(dimension**3)

    def __generate_tiles(self, image: Surface):
        self.tiles = []
        for i in range(self.DIMENSION):
            self.tiles.append([])
            for j in range(self.DIMENSION):
                image_segment = image.subsurface(
                    (i * self.TILE_SIZE, j * self.TILE_SIZE),
                    (self.TILE_SIZE, self.TILE_SIZE),
                )
                self.tiles[i].append(image_segment)
        self.tiles[-1][-1] = None
        self.empty_x, self.empty_y = self.DIMENSION - 1, self.DIMENSION - 1

    def __shuffle_tiles(self, shuffle_moves: int):
        for _ in range(shuffle_moves):
            self.__move_tile(
                # unzip choice to pass position arguments seperately
                *choice(
                    (
                        (self.empty_x + 1, self.empty_y),
                        (self.empty_x - 1, self.empty_y),
                        (self.empty_x, self.empty_y + 1),
                        (self.empty_x, self.empty_y - 1),
                    )
                )
            )

    def __move_tile(self, tile_x, tile_y):
        if self.__valid_move(tile_x, tile_y):
            self.tiles[self.empty_x][self.empty_y] = self.tiles[tile_x][tile_y]
            self.tiles[tile_x][tile_y] = None
            self.empty_x, self.empty_y = tile_x, tile_y

    def __valid_move(self, tile_x: int, tile_y: int) -> bool:
        if tile_x not in range(self.DIMENSION) or tile_y not in range(self.DIMENSION):
            return False
        if tile_x + 1 in range(self.DIMENSION):
            if self.tiles[tile_x + 1][tile_y] == None:
                return True
        if tile_x - 1 in range(self.DIMENSION):
            if self.tiles[tile_x - 1][tile_y] == None:
                return True
        if tile_y + 1 in range(self.DIMENSION):
            if self.tiles[tile_x][tile_y + 1] == None:
                return True
        if tile_y - 1 in range(self.DIMENSION):
            if self.tiles[tile_x][tile_y - 1] == None:
                return True
        return False

    def handle_click(self, mouse_x: int, mouse_y: int):
        self.__move_tile(mouse_x // self.TILE_SIZE, mouse_y // self.TILE_SIZE)

    def render_board(self) -> Surface:
        board_image = Surface((self.RESOLUTION, self.RESOLUTION))
        for i in range(self.DIMENSION):
            for j in range(self.DIMENSION):
                if self.tiles[i][j]:
                    board_image.blit(
                        self.tiles[i][j],
                        (i * self.TILE_SIZE, j * self.TILE_SIZE),
                    )
        return board_image
