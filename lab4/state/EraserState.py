from typing import *
from .State import State
from model.DocumentModel import DocumentModel
from graphics.Point import Point
from CustomCanvas import CustomCanvas
from graphics.GraphicalObject import GraphicalObject

class DeleteShapeState(State):

    def __init__(self, model: DocumentModel, canvas: CustomCanvas) -> None:
        self.model = model
        self.canvas = canvas
        self.points: List[int] = []

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.last_x, self.last_y = mousePoint.getX(), mousePoint.getY()
    
    def mouseDragged(self, mousePoint: Point) -> None:
        self.points.extend([self.last_x, self.last_y])
        x, y = mousePoint.getX(), mousePoint.getY()
        self.canvas.create_line(self.last_x, self.last_y, x, y)
        self.last_x, self.last_y = x, y
        
    
    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.points.extend([self.last_x, self.last_y])
        toErase: List[GraphicalObject] = []
        for i in range(0, len(self.points), 2):
            currentPoint = Point(self.points[i], self.points[i+1])
            toEraseObject = self.model.findSelectedGraphicalObject(currentPoint)
            if toErase is not None:
                self.model.removeGraphicalObject(toEraseObject)
        
        self.model.notifyListeners()