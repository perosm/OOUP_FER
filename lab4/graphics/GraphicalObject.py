from abc import ABC, abstractmethod
from typing import *
from graphics.Point import Point
from graphics.Rectangle import Rectangle
from Renderer import Renderer
#from GraphicalObjectListener import GraphicalObjectListener

class GraphicalObject:
    pass

class GraphicalObjectListener:
    # Poziva se kad se nad objektom promjeni bio što...
    @abstractmethod
    def graphicalObjectChanged(self, go: GraphicalObject) -> None:
        pass

    # Poziva se isključivo ako je nad objektom promjenjen status selektiranosti
    # (baš objekta, ne njegovih hot-point-a).
    def graphicalObjectSelectionChanged(self, go: GraphicalObject) -> None:
        pass



class GraphicalObject(ABC):
    """
    Sučelje GraphicalObject predstavlja apstraktni model jednog grafičkog objekta.
    Sučelje predviđa da svaki grafički objekt bude subjekt čije stanje čine njegovi 
    "hot-point"-i  (pozicije te status selektiranosti) te njegov status selektiranosti.
    """
    # Podrska za uredivanje objekta
    @abstractmethod
    def isSelected(self) -> bool:
        pass

    @abstractmethod
    def setSelected(self, selected: bool) -> None:
        pass

    @abstractmethod
    def getNumberOfHotPoints(self) -> int:
        pass

    @abstractmethod
    def getHotPoint(self, index: int) -> Point:
        pass

    @abstractmethod
    def setHotPoint(self, index: int, point: Point) -> None:
        pass

    @abstractmethod
    def isHotPointSelected(self, index: int) -> bool:
        pass

    @abstractmethod
    def setHotPointSelected(self, index: int, selected: bool) -> None:
        pass

    @abstractmethod
    def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
        pass

    # Geometrijska operacija nad oblikom
    @abstractmethod
    def translate(self, delta: Point) -> None:
        pass

    @abstractmethod
    def getBoundingBox(self) -> Rectangle:
        pass

    @abstractmethod
    def selectionDistance(self, mousePoint: Point) -> float:
        pass

    # Podrska za crtanje (dio mosta)
    
    @abstractmethod
    def render(self, r: Renderer) -> None:
        pass
    
    # Observer za dojavu promjena modelu
    @abstractmethod
    def addGraphicalObjectListener(self, l: GraphicalObjectListener) -> None:
        pass

    @abstractmethod
    def removeGraphicalObjectListener(self, l: GraphicalObjectListener) -> None:
        pass

    @abstractmethod
    # podrska za prototip (alatna traka, stvaranje objekata u crtezu, ...)
    def getShapeName(self) -> str:
        pass

    @abstractmethod
    def duplicate(self) -> 'GraphicalObject':
        pass

    # Podrska za snimanje i ucitavanje
    
    @abstractmethod
    def getShapeID(self) -> str:
        pass
    
    @abstractmethod
    def load(self, stack: List['GraphicalObject'], data: str) -> None:
        pass

    @abstractmethod
    def save(self, rows: List[str]) -> None:
        pass
    