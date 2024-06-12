import copy
from Renderer import Renderer
from .State import State
from graphics.Point import Point
from graphics.GraphicalObject import GraphicalObject
from model.DocumentModel import DocumentModel
from graphics.Rectangle import Rectangle
from graphics.CompositeShape import CompositeShape


class SelectShapeState(State):
    def __init__(self, model: DocumentModel) -> None:
        self.model = model

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        if ctrlDown:
            object = self.model.findSelectedGraphicalObject(mousePoint=mousePoint)
            object.setSelected(True)
        else:
            # deselektiranje objekata
            for selectedObj in self.model.getSelectedObjects():
                selectedObj.setSelected(False)

            object = self.model.findSelectedGraphicalObject(mousePoint=mousePoint)

            if object is not None:
                object.setSelected(True)


    def afterDraw(self, r: Renderer) -> None:
        selectionCnt = len(self.model.getSelectedObjects())

        if selectionCnt == 1:
            for so in self.model.selectedObjects:
                boundingBox: Rectangle = so.getBoundingBox()
                x, y = boundingBox.getX(), boundingBox.getY()
                height, width = boundingBox.getHeight(), boundingBox.getWidth()
                r.create_rectangle(x, y, x+height, y+width)
                for j in range(so.getNumberOfHotPoints()):
                    hotPoint: Point = so.getHotPoint(j)
                    r.create_rectangle(hotPoint.getX()-2, hotPoint.getY()-2, hotPoint.getX()+2, hotPoint.getY()+2)
        else:
            for so in self.model.selectedObjects:            
                boundingBox: Rectangle = so.getBoundingBox()
                x, y = boundingBox.getX(), boundingBox.getY()
                height, width = boundingBox.getHeight(), boundingBox.getWidth()
                r.create_rectangle(x, y, x+height, y+width)


    # TO DO:
    def mouseDragged(self, mousePoint: Point) -> None:
        if len(self.model.getSelectedObjects()) == 0 or len(self.model.getSelectedObjects()) > 1:
            return
        object = self.model.getSelectedObjects()[0]
        min_dist = 2**32-1
        closest_hp_index = -1
        for i in range(object.getNumberOfHotPoints()):
            dist = object.getHotPointDistance(i, mousePoint)
            if dist < min_dist:
                closest_hp_index = i

        object.setHotPoint(closest_hp_index, mousePoint)
        

    def keyPressed(self, keyCode: int) -> None:
        if keyCode == 1: # desno
            for object in self.model.getSelectedObjects():
                object.translate(Point(1, 0))
        elif keyCode == 2: # lijevo
            for object in self.model.getSelectedObjects():
                object.translate(Point(-1, 0))
        elif keyCode == 3: # gore
            for object in self.model.getSelectedObjects():
                object.translate(Point(0, -1))
        elif keyCode == 4: # dolje
            for object in self.model.getSelectedObjects():
                object.translate(Point(0, 1))
        elif keyCode == 5: # blize promatracu
            self.model.increaseZ(self.model.getSelectedObjects()[0])
        elif keyCode == 6: # dalje promatracu
            self.model.decreaseZ(self.model.getSelectedObjects()[0])
        elif keyCode == 7: # tipka G brise selektirane objekte i stvara kompozit
            objectsMakingComposite = copy.deepcopy(self.model.getSelectedObjects())
            
            while len(self.model.getSelectedObjects()) != 0:
                object = self.model.getSelectedObjects()[0]
                if object is not None:
                    self.model.removeGraphicalObject(object)

            compositeObject: CompositeShape = CompositeShape(objectsMakingComposite, False)
            self.model.addGraphicalObject(compositeObject)
            compositeObject.setSelected(True)

        elif keyCode == 8:
            compositeObject = self.model.getSelectedObjects()[0]
            if compositeObject.getShapeName() == "CompositeShape":
                self.model.removeGraphicalObject(compositeObject)
                for object in compositeObject.getShapes():
                    self.model.addGraphicalObject(object)
                    object.setSelected(True)

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass