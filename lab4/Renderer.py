from abc import ABC, abstractmethod
from graphics.Point import Point
from typing import *

class Renderer:
    @abstractmethod
    def drawLine(self, s: Point, e: Point) -> None:
        pass

    @abstractmethod
    def fillPolygon(self, points: List[Point]) -> None:
        pass