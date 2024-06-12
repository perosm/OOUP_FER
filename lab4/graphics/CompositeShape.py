from typing import *
from typing import List
from .GraphicalObject import GraphicalObject
from .AbstractGraphicalObject import AbstractGraphicalObject
from Renderer import Renderer
from graphics.Point import Point
from graphics.Rectangle import Rectangle
from utils.GeometryUtil import GeometryUtil

class CompositeShape(AbstractGraphicalObject):
    def __init__(self, shapes: List[GraphicalObject] = None, selected: bool = False) -> None:
        self.shapes: List[GraphicalObject] = shapes
        self.selected = selected

    def getShapes(self) -> List[GraphicalObject]:
        return self.shapes
    
    def translate(self, delta: Point) -> None:
        for shape in self.shapes:
            shape.translate(delta=delta)

    def isSelected(self) -> bool:
        return super().isSelected()
    
    def setSelected(self, selected: bool) -> None:
        super().setSelected(selected)

    def render(self, r: Renderer) -> None:
        for shape in self.shapes:
            shape.render(r=r)

        if not self.isSelected():
            return
        
        bb: Rectangle = self.getBoundingBox()
        # ako smo selektirani -> crtamo bounding box oko citave grupe


    def getBoundingBox(self) -> Rectangle: # TO DO: NAPRAVIT DOBAR BOUNDING BOX
        points: List[Point] = []
        for shape in self.shapes:
            shapeBB: Rectangle = shape.getBoundingBox()
            points.append(Point(shapeBB.getX(), shapeBB.getY()))
            points.append(Point(shapeBB.getX() + shapeBB.getWidth(), shapeBB.getY() + shapeBB.getWidth()))

        minPointX, minPointY = 2**32-1, 2**32-1
        maxPointX, maxPointY = -1, -1
        
        for point in points:
            if point.getX() > maxPointX:
                maxPointX = point.getX()
            if point.getY() > maxPointY:
                maxPointY = point.getY()
            if point.getX() < minPointX:
                minPointX = point.getX()
            if point.getY() < minPointY:
                minPointY = point.getY()

        width = maxPointX - minPointX
        height = maxPointY - minPointY 

        return Rectangle(minPointX, minPointY, height, width)

    
    # metode koje ne trebaju
    def duplicate(self) -> GraphicalObject:
        new_shapes = [shape.duplicate() for shape in self.shapes]
        return CompositeShape(new_shapes, self.selected)

    def getShapeName(self) -> str:
        return "CompositeShape"
    
    def selectionDistance(self, mousePoint: Point) -> float:
        min_distance = 2**32-1
        for shape in self.shapes:
            distance = shape.selectionDistance(mousePoint)
            if distance < min_distance:
                min_distance = distance

        return min_distance
    

    def getShapeID(self) -> str:
        return "@COMP"
    
    def load(self, stack: List[GraphicalObject], data: str) -> None:
        howManyPops = int(data.strip())
        objectsThatCompose: List[GraphicalObject] = [] 
        for i in range(howManyPops):
            objectsThatCompose.append(stack.pop())
            
        stack.append(CompositeShape(objectsThatCompose, False))
    
    def save(self, rows: List[str]) -> None:
        for object in self.shapes:
            object.save(rows=rows)
        rows.append(f'{self.getShapeID()} {len(self.shapes)}\n')

    def __str__(self) -> str:
        return f'Kompozit s {len(self.shapes)} objekata'