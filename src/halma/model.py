from dataclasses import dataclass
from enum import IntEnum, auto
from functools import cached_property

class Content(IntEnum):
    NONE = 0
    EMPTY = auto()
    PEG = auto()

Directions = {
    'up': -10,
    'right': 1,
    'down': 10,
    'left': -1,
}

@dataclass(frozen=True)
class Board():
    tiles: dict[int, Content]

    def __iter__(self):
        return iter(self.tiles.items())

    def __getitem__(self, index: int):
        return self.tiles[index]

    @cached_property
    def moves(self):
        for index in self.pegs:
            for offset in Directions.values():
                try:
                    if (
                        self[index + offset] is Content.PEG 
                        and self[index + offset * 2] is Content.EMPTY
                    ):
                        yield (index, offset)
                except KeyError:
                    pass
                    
    def move_peg(self, index, offset):
        tiles = self.tiles.copy()
        tiles[index] = Content.EMPTY
        tiles[index + offset] = Content.EMPTY
        tiles[index + offset * 2] = Content.PEG
        return self.__class__(tiles)
    
    @cached_property
    def pegs(self):
        return tuple(index for index, content in self if content is Content.PEG)
    
    @cached_property
    def holes(self):
        return tuple(index for index, content in self if content is Content.EMPTY)

new_board = Board({0: Content.PEG, 1: Content.PEG, 2: Content.EMPTY, 3: Content.PEG, 4: Content.EMPTY})

if __name__ == '__main__':
    for move in new_board.moves:
        index, offset = move
        