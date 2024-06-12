from typing import *
from utils.GeometryUtil import GeometryUtil
from graphics.GraphicalObject import GraphicalObject, GraphicalObjectListener
from graphics.Point import Point
from Renderer import Renderer

class AbstractGraphicalObject(GraphicalObject):
    hotPoints: List[Point] = []
    hotPointSelected: List[bool] = []
    selected: bool = None
    listeners: List[GraphicalObjectListener] = []

    def __init__(self, points: List[Point]) -> None:
        self.hotPoints: List[Point] = points
        self.hotPointSelected: List[bool] = [] 
        self.selected: bool = False
        self.listeners: List[GraphicalObjectListener] = []

    def getHotPoint(self, index: int) -> Point:
        return self.hotPoints[index]
    
    def setHotPoint(self, index: int, point: Point) -> None:
        self.hotPoints[index] = point
        self.notifyListeners()
    
    def getNumberOfHotPoints(self) -> int:
        return len(self.hotPoints)
    
    def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
        return GeometryUtil.distanceFromPoint(self.hotPoints[index], mousePoint)
    
    def isHotPointSelected(self, index: int) -> bool:
        return self.hotPointSelected[index]

    def setHotPointSelected(self, index: int, selected: bool) -> None:
        self.hotPointSelected[index] = selected
        #self.notifySelectionListeners()

    def isSelected(self) -> bool:
        return self.selected
    
    def setSelected(self, selected: bool) -> None:
        self.selected = selected
        self.notifySelectionListeners()
    
    def translate(self, delta: Point) -> None:
        translatedHotPoints: List[Point] = []
        for hp in self.hotPoints:
            translatedHotPoints.append(hp.translate(delta))

        self.hotPoints = translatedHotPoints
        self.notifyListeners()

    def addGraphicalObjectListener(self, l: GraphicalObjectListener) -> None:
        if l not in self.listeners:
            self.listeners.append(l)
    
    def removeGraphicalObjectListener(self, l: GraphicalObjectListener) -> None:
        if l in self.listeners:
            self.listeners.remove(l)
    
    def render(self, r: Renderer) -> None:
        return super().render(r)
    
    # Zadatak 1.3
    
    def notifyListeners(self) -> None:
        for listener in self.listeners:
            listener.graphicalObjectChanged(self)

    def notifySelectionListeners(self) -> None:
        for listener in self.listeners:
            listener.graphicalObjectSelectionChanged(self)
    
    
    