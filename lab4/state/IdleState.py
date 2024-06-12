from state.State import State
from graphics.Point import Point
from Renderer import Renderer
from graphics.GraphicalObject import GraphicalObject

class IdleState(State):
    def __init__(self) -> None:
        pass

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    def mouseDragged(self, mousePoint: Point) -> None:
        pass

    def keyPressed(self, keyCode: int) -> None:
        pass

    def afterDraw(self, r: Renderer, go: GraphicalObject) -> None:
        pass

    def afterDraw(self, r: Renderer) -> None:
        pass

    def onLeaving(self) -> None:
        pass