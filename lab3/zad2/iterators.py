from collections.abc import Iterable, Iterator
from typing import Any

class TextIterator(Iterator):
    position: int = 0

    def __init__(self, lines) -> None:
        self.lines = lines

    def __next__(self) -> Any:
        try:
            value = self.lines[self.position]
            self.position += 1
        except IndexError:
            raise StopIteration()
        
        return value
    

