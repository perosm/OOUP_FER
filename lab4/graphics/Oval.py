import copy
import math
from typing import *
from typing import List
from graphics.AbstractGraphicalObject import AbstractGraphicalObject
from graphics.Point import Point
from graphics.GraphicalObject import GraphicalObject
from graphics.Rectangle import Rectangle
from utils.GeometryUtil import GeometryUtil
from Renderer import Renderer

class Oval(AbstractGraphicalObject):
    center: Point = Point(10, 10)
    def __init__(self, s: Point=Point(10, 0), e: Point=Point(0, 10)) -> None:
        super().__init__([s, e])
        self.center = Point(s.getX(), e.getY())

    def selectionDistance(self, mousePoint: Point) -> float:
        pointsOnOval = []
        a = self.hotPoints[0]
        b = self.hotPoints[1]
        # TO DO: POPRAVIT UDALJENOST!
        self.center = Point(b.getX(), a.getY())
        radiusX = a.getX() - self.center.getX()
        radiusY = b.getY() - self.center.getY()
        #print(f'a={a}, b={b}, center={self.center}, mouse={mousePoint}')
        for degree in range(360):
            x_i = self.center.getX() + radiusX * math.cos((degree / 360) * 2 * math.pi)
            y_i = self.center.getY() + radiusY * math.sin((degree / 360) * 2 * math.pi)
            pointsOnOval.append(Point(x_i, y_i))

        min_distance = 2**32-1
        for point in pointsOnOval:
            distance = GeometryUtil.distanceFromPoint(mousePoint, point)
            if distance < min_distance:
                min_distance = distance
        
        return distance 

    def getBoundingBox(self) -> Rectangle:
        a = self.hotPoints[0]
        b = self.hotPoints[1]
        self.center = Point(b.getX(), a.getY())
        dleft = a.x - self.center.getX()
        dupper = b.y - self.center.getY()
        upperLeft = Point(self.center.x - dleft, self.center.y - dupper)
        height = 2 * GeometryUtil.distanceFromPoint(self.center, a)
        width = 2 * GeometryUtil.distanceFromPoint(self.center, b)
        
        return Rectangle(x=upperLeft.getX(), y=upperLeft.getY(), width=width, height=height)
    
    def duplicate(self) -> GraphicalObject: # pazi da se ne kopira popis prijavljenih promatraca 
        return Oval(self.hotPoints[0], self.hotPoints[1])
    
    def getShapeName(self) -> str:
        return "Oval"
    
    def render(self, r: Renderer) -> None:
        pointsOnOval = []
        a = self.hotPoints[0]
        b = self.hotPoints[1]
        self.center = Point(b.getX(), a.getY())
        radiusX = a.getX() - self.center.getX()
        radiusY = b.getY() - self.center.getY()

        for degree in range(360):
            x_i = self.center.getX() + radiusX * math.cos((degree / 360) * 2 * math.pi)
            y_i = self.center.getY() + radiusY * math.sin((degree / 360) * 2 * math.pi)
            pointsOnOval.append(Point(x_i, y_i))
        
        r.fillPolygon(pointsOnOval) # TO DO?

    def getShapeID(self) -> str:
        return "@OVAL"
    
    def load(self, stack: List[GraphicalObject], data: str) -> None:
        coords = [int(coord) for coord in data.split()]
        a = Point(coords[0], coords[1])
        b = Point(coords[0], coords[1])
        stack.append(Oval(s=a, e=b))
    
    def save(self, rows: List[str]) -> None:
        a = self.getHotPoint(0)
        b = self.getHotPoint(1)
        rows.append(f'{self.getShapeID()} {a.x} {a.y} {b.x} {b.y}\n')
    
    def __str__(self) -> str:
        return f'Oval {self.hotPoints[0]} {self.hotPoints[1]}'