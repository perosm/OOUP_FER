from typing import Type

class Point:
    x: int = None
    y: int = None

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def translate(self, dp: 'Point') -> 'Point':
        return Point(self.x + dp.x, self.y + dp.y)
    
    def difference(self, p: 'Point') -> 'Point':
        return Point(self.x - p.x, self.y - p.y)
    
    def __str__(self) -> str:
        return f'{self.x, self.y}'