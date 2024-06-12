from typing import *
from typing import List
from graphics.AbstractGraphicalObject import AbstractGraphicalObject
from graphics.GraphicalObject import GraphicalObject
from utils.GeometryUtil import GeometryUtil
from graphics.Point import Point
from graphics.GraphicalObject import GraphicalObject, GraphicalObjectListener
from graphics.Rectangle import Rectangle
from Renderer import Renderer


class LineSegment(AbstractGraphicalObject):
    def __init__(self, s: Point=Point(10, 0), e: Point=Point(0, 10)) -> None:
        super().__init__([s, e])

    def selectionDistance(self, mousePoint: Point) -> float:
        return GeometryUtil.distanceFromLineSegment(s=self.hotPoints[0], e=self.hotPoints[1], p=mousePoint)
    
    def getBoundingBox(self) -> Rectangle:
        x_min = min(self.hotPoints[0].getX(), self.hotPoints[1].getX())
        y_min = min(self.hotPoints[0].getY(), self.hotPoints[1].getY())
        x_max = max(self.hotPoints[0].getX(), self.hotPoints[1].getX())
        y_max = max(self.hotPoints[0].getY(), self.hotPoints[1].getY())
        width = x_max - x_min
        height = y_max - y_min
        return Rectangle(x=x_min, y=y_min, width=width, height=height)
    
    def duplicate(self) -> GraphicalObject:
        return LineSegment(self.hotPoints[0], self.hotPoints[1])
    
    def getShapeName(self) -> str:
        return "Linija"
    
    def render(self, r: Renderer) -> None:
        r.drawLine(self.hotPoints[0], self.hotPoints[1])

    def __str__(self) -> str:
        return f'Linijski segment {self.hotPoints[0]} {self.hotPoints[1]}'

    def getShapeID(self) -> str:
        return f'@LINE'
    
    def load(self, stack: List[GraphicalObject], data: str) -> None:
        coords = [int(coord) for coord in data.split()]
        s = Point(coords[0], coords[1])
        e = Point(coords[0], coords[1])
        stack.append(LineSegment(s=s, e=e))
    
    def save(self, rows: List[str]) -> None:
        s = self.getHotPoint(0)
        e = self.getHotPoint(1)
        rows.append(f'{self.getShapeID()} {s.x} {s.y} {e.x} {e.y}\n')