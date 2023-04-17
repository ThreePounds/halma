from dataclasses import dataclass
from enum import IntEnum, auto
from functools import cached_property
from typing import Iterator

class Content(IntEnum):
    NONE = 0
    EMPTY = auto()
    PEG = auto()

@dataclass(frozen=True)
class Tile():
    index: int
    row: int
    column: int
    content: Content = Content.NONE

@dataclass(frozen=True)
class Board():
    tiles: tuple[Tile, ...]
    
    def __iter__(self) -> Iterator[Tile]:
        return iter(self.tiles)
    
    def __getitem__(self, index: int) -> Tile:
        return self.tiles[index]
   
    @classmethod
    def English(cls):
        """New empty English board."""
        board = []
        for x in range(7):
            for y in range(7):
                if x in [0, 1, 5, 6] and y in [0, 1, 5, 6]:
                    # corner
                    board.append(Tile(x * 10 + y, x, y))
                else:
                    # empty tile
                    board.append(Tile(x * 10 + y, x, y, Content.EMPTY))
        return cls(tuple(board))

    @cached_property
    def pegs(self) -> Tile:
        return iter(tile for tile in self if tile.content is Content.PEG)