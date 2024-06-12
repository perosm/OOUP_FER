from abc import ABC, abstractmethod
from typing import *
from graphics.GraphicalObject import GraphicalObject, GraphicalObjectListener
from graphics.AbstractGraphicalObject import AbstractGraphicalObject
from graphics.GraphicalObject import GraphicalObject
from utils.GeometryUtil import GeometryUtil
from graphics.Point import Point

class DocumentModelListener(ABC):
    @abstractmethod
    def documentChange(self, documentModel: 'DocumentModel'):
        pass

class GraphicalObjectListenerImpl(GraphicalObjectListener):
    def __init__(self, document_model: 'DocumentModel'):
        self.document_model = document_model

    def graphicalObjectChanged(self, go: GraphicalObject):
        self.document_model.notifyListeners()

    def graphicalObjectSelectionChanged(self, go: GraphicalObject):
        if go.isSelected():
            if go not in self.document_model.selectedObjects:
                self.document_model.selectedObjects.append(go)
        else:
            self.document_model.selectedObjects.remove(go)

        self.document_model.notifyListeners()

class DocumentModel:
    SELECTION_PROXIMITY: float = 10.0
    
    # kolekcija svih grafickih objekata
    objects: List[GraphicalObject] = []
    # read-only proxy oko kolekcije grafickih objekata
    roObjects: List[GraphicalObject] = []
    # kolekcija prijavljenih promatraca
    listeners: List[DocumentModelListener] = []
    # kolekcija selektiranih objekata
    selectedObjects: List[GraphicalObject] = []
    # read-only proxy oko kolekcije selektiranih objekata
    roSelectedObjects: List[GraphicalObject] = []

    # promatrac koji ce bit registriran nad svim objektima crteza
    #goListener: GraphicalObjectListener = None

    def __init__(self) -> None:
        self.goListener = GraphicalObjectListenerImpl(self)

    # brisanje svih objekata iz modela (pazite da se sve potrebno odregistrira)
    # potom obavijeste svi promatraci modela
    def clear(self) -> None:
        for object in self.objects:
            object.removeGraphicalObjectListener(self.goListener)

        self.selectedObjects = [] # ?
        self.objects = []

        self.notifyListeners()

    # dodavanje objekta u dokument 
    # (pazite je li već selektiran; registrirajte model kao promatrača)
    def addGraphicalObject(self, obj: GraphicalObject) -> None:
        # DocumentModel je subjekt koji svojim klijentima omogućava 
        # dojavu informacija o dodavanju i uklanjanju grafickih objekata
        # sam DocumentModel prijavit će se kao promatrač nad svakim 
        # grafičkim objektom koji mu pripada
        # i u situacijama kada ga grafički objekt obavijesti da je 
        # došlo do promjene u grafičkom objektu, 
        # DocumentModel će o tome obavijestiti svoje promatrače.
        # Na ovaj način osigurano je da je dovoljno da se platno 
        # za crtanje prijavi samo na DocumentModel.
        obj.addGraphicalObjectListener(self.goListener)
        self.objects.append(obj)

        self.notifyListeners()
    
    # uklanjanje objekta iz dokumenta 
    # (pazite je li već selektiran; odregistrirajte model kao promatrača) 
    def removeGraphicalObject(self, obj: GraphicalObject) -> None:
        if obj is None:
            return
        
        obj.removeGraphicalObjectListener(self.goListener)
        if obj in self.getSelectedObjects():
            self.selectedObjects.remove(obj)
        self.objects.remove(obj)

        self.notifyListeners()
    # vrati nepromjenjivu listu postojećih objekata 
    # (izmjene smiju ići samo kroz metode modela)
    def list(self):
        return self.objects
    
    # prijava
    def addDocumentModelListener(self, l: DocumentModelListener) -> None:
        if l in self.listeners:
            return
        
        self.listeners.append(l)

    # odjava
    def removeDocumentModelListener(self, l: DocumentModelListener) -> None:
        if l not in self.listeners:
            return
        print("ALI ON JE U LISTENERIMA???")
        self.listeners.remove(l)

    # obavjestavanje
    def notifyListeners(self) -> None:
        for listener in self.listeners:
            listener.documentChange(self)

    # vrati nepromjenjivu listu selektiranih objekata
    def getSelectedObjects(self) -> List[GraphicalObject]:
        return self.selectedObjects
    
    # pomakni predani objekt u listi objekata na jedno mjesto kasnije
    # time ce se on iscrtati kasnije
    # (pa ce time mozda veci dio biti vidljiv)
    def increaseZ(self, go: GraphicalObject) -> None:
        cnt = 0

        for object in self.objects:
            if object == go:
                break
            cnt += 1

        if cnt < len(self.objects) - 1:
            self.objects[cnt], self.objects[cnt + 1] = self.objects[cnt + 1], self.objects[cnt]
        
        self.notifyListeners()
    
    # pomakni predani objekt u listi objekata na jedno mjesto ranije
    def decreaseZ(self, go: GraphicalObject) -> None:
        cnt = 0

        for object in self.objects:
            if object == go:
                break
            cnt += 1

        if cnt > 0:
            self.objects[cnt], self.objects[cnt-1] = self.objects[cnt-1], self.objects[cnt]

        self.notifyListeners()
    # pronađi postoji li u modelu neki objekt koji klik na točku koja je
    # predana kao argument selektira i vrati ga ili vrati null. Točka selektira
    # objekt kojemu je najbliža uz uvjet da ta udaljenost nije veća od
    # SELECTION_PROXIMITY. Status selektiranosti objekta ova metoda NE dira.
    def findSelectedGraphicalObject(self, mousePoint: Point) -> GraphicalObject:
        min_dist = 2**32-1
        min_index = -1
        for i in range(len(self.objects)):
            dist = self.objects[i].selectionDistance(mousePoint)
            if dist < min_dist and dist < self.SELECTION_PROXIMITY:
                min_dist = dist
                min_index = i

        if min_index == -1:
            return None
        
        return self.objects[min_index]
    
    # pronađi da li u predanom objektu predana točka miša selektira neki hot-point.
    # točka miša selektira onaj hot-point objekta kojemu je najbliža uz uvjet da ta
    # udaljenost nije veća od SELECTION_PROXIMITY. Vraća se indeks hot-pointa 
    # kojeg bi predana točka selektirala ili -1 ako takve nema
    # status selekcije se pri tome NE dira.
    def findSelectedHotPoint(self, object: GraphicalObject, mousePoint: Point) -> int:
        min_dist = 2**32 - 1
        min_index = -1
        for i in range(len(object.getNumberOfHotPoints())):
            hotPoint_i = object.getHotPoint(i)
            dist_i = GeometryUtil.distanceFromPoint(mousePoint, hotPoint_i)
            if dist_i < min_dist and dist_i < self.SELECTION_PROXIMITY:
                min_dist = dist_i
                min_index = i

        return min_index