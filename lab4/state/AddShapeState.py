from .State import State
from graphics.Point import Point
from graphics.GraphicalObject import GraphicalObject
from model.DocumentModel import DocumentModel

class AddShapeState(State):

    def __init__(self, model: DocumentModel, prototype: GraphicalObject) -> None:
        self.model: DocumentModel = model
        self.prototype: GraphicalObject = prototype

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        go: GraphicalObject = self.prototype.duplicate()
        go.translate(mousePoint)
        self.model.addGraphicalObject(go)
        
    def __str__(self) -> str:
        return f'Crtamo {self.prototype.getShapeName}'