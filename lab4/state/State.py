from abc import ABC, abstractmethod
from graphics.Point import Point
from Renderer import Renderer
from graphics.GraphicalObject import GraphicalObject

class State:
    # poziva se kad progam registrira da je pritisnuta lijeva tipka miša
    @abstractmethod
    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    # poziva se kad progam registrira da je otpuštena lijeva tipka miša
    @abstractmethod
    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    # poziva se kad progam registrira da korisnik pomiče miš dok je tipka pritisnuta
    @abstractmethod
    def mouseDragged(self, mousePoint: Point) -> None:
        pass

    # poziva se kad progam registrira da je korisnik pritisnuo tipku na tipkovnici
    @abstractmethod
    def keyPressed(self, keyCode: int) -> None:
        pass

    # Poziva se nakon što je platno nacrtalo grafički objekt predan kao argument
    @abstractmethod
    def afterDraw(self, r: Renderer, go: GraphicalObject) -> None:
        pass

    # Poziva se nakon što je platno nacrtalo čitav crtež
    @abstractmethod
    def afterDraw(self, r: Renderer) -> None:
        pass
    
    # Poziva se kada program napušta ovo stanje kako bi prešlo u neko drugo
    @abstractmethod
    def onLeaving(self) -> None:
        pass