from pygame import Surface
from random import randint


class PuzzleBoard:
    def __init__(self, dimension: int, resolution: int, image: Surface):
        self.DIMENSION = dimension
        self.RESOLUTION = resolution
        self.TILE_SIZE = resolution // dimension
        self.__generate_tiles(image.subsurface((0, 0), (resolution, resolution)))
        self.__shuffle_tiles(dimension**dimension)

    def __generate_tiles(self, image: Surface):
        self.tiles = []
        for i in range(self.DIMENSION):
            for j in range(self.DIMENSION):
                image_segment = image.subsurface(
                    (j * self.TILE_SIZE, i * self.TILE_SIZE),
                    (self.TILE_SIZE, self.TILE_SIZE),
                )
                self.tiles.append(image_segment)
        self.tiles[-1] = None

    def __shuffle_tiles(self, shuffle_moves: int):
        empty_pos = len(self.tiles) - 1
        for _ in range(shuffle_moves):
            adjacent_positions = []
            if empty_pos + 1 < len(self.tiles):
                adjacent_positions.append(1)
            if empty_pos - 1 >= 0:
                adjacent_positions.append(-1)
            if empty_pos + self.DIMENSION < len(self.tiles):
                adjacent_positions.append(self.DIMENSION)
            if empty_pos - self.DIMENSION >= 0:
                adjacent_positions.append(-self.DIMENSION)
            empty_pos += adjacent_positions[randint(0, len(adjacent_positions) - 1)]
            self.__move_tile(empty_pos)

    def __move_tile(self, tile_position: int):
        if self.__valid_move(tile_position):
            self.tiles[self.tiles.index(None)] = self.tiles[tile_position]
            self.tiles[tile_position] = None

    def __valid_move(self, tile_position: int) -> bool:
        if tile_position + 1 < len(self.tiles):
            if not self.tiles[tile_position + 1]:
                return True
        if tile_position - 1 >= 0:
            if not self.tiles[tile_position - 1]:
                return True
        if tile_position + self.DIMENSION < len(self.tiles):
            if not self.tiles[tile_position + self.DIMENSION]:
                return True
        if tile_position - self.DIMENSION >= 0:
            if not self.tiles[tile_position - self.DIMENSION]:
                return True
        return False

    def handle_click(self, mouse_x: int, mouse_y: int):
        self.__move_tile(
            mouse_y // self.TILE_SIZE * self.DIMENSION + mouse_x // self.TILE_SIZE
        )

    def render_board(self) -> Surface:
        board_image = Surface((self.RESOLUTION, self.RESOLUTION))
        for i in range(self.DIMENSION):
            for j in range(self.DIMENSION):
                if self.tiles[i * self.DIMENSION + j]:
                    board_image.blit(
                        self.tiles[i * self.DIMENSION + j],
                        (j * self.TILE_SIZE, i * self.TILE_SIZE),
                    )
        return board_image
