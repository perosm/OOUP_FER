from tkinter import *
from typing import List
from Renderer import Renderer
from graphics.Point import Point
from model.DocumentModel import DocumentModel, DocumentModelListener
from state.State import State


# https://stackoverflow.com/questions/19861689/check-if-modifier-key-is-pressed-in-tkinter
mods = {
    0x0000: '',
    0x0001: 'Shift',
    0x0002: 'Caps Lock',
    0x0004: 'Control',
    0x0005: 'Shift+Control',
    0x0008: 'Left-hand Alt',
    0x0010: 'Num Lock',
    0x0080: 'Right-hand Alt',
    0x0100: 'Mouse button 1',
    0x0200: 'Mouse button 2',
    0x0400: 'Mouse button 3'
}

class CustomCanvas(Canvas, Renderer, DocumentModelListener): # platno za crtanje
    
    def __init__(self, root, model: DocumentModel, state: State):
        super().__init__()
        self.root = root
        self.model: DocumentModel = model
        self.currentState: State = state
        self.configure(bg='lightblue')
        self.pack(expand=True, fill=BOTH) # https://stackoverflow.com/questions/28089942/difference-between-fill-and-expand-options-for-tkinter-pack-method
        self.paintComponent()
        self.declareEvents()

    def declareEvents(self):
        self.bind("<ButtonPress-1>", self.mouseDown)
        self.bind("<B1-Motion>", self.mouseDragged)
        self.bind("<ButtonRelease-1>", self.mouseUp)
        self.bind("<Key>", self.keyPressed)
        # self.bind("", self.currentState.onLeaving)
        self.focus_set()
        

    # samo za provjeru
    def mouseDown(self, event):
        mod = mods[event.state]
        mousePoint = Point(event.x, event.y)
        shiftDown = self.checkShiftDown(mod)
        CTRLDown = self.checkCTRLDown(mod)
        self.currentState.mouseDown(mousePoint=mousePoint, shiftDown=shiftDown, ctrlDown=CTRLDown)
        

    def mouseDragged(self, event):
        mousePoint = Point(event.x, event.y)
        self.currentState.mouseDragged(mousePoint=mousePoint)


    def mouseUp(self, event):
        #mod = mods[event.state]
        mousePoint = Point(event.x, event.y)
        #shiftDown = self.checkShiftDown(mod)
        #CTRLDown = self.checkCTRLDown(mod)
        self.currentState.mouseUp(mousePoint=mousePoint, shiftDown=False, ctrlDown=False)


    def keyPressed(self, event):
        if event.keysym == 'Right':
            self.currentState.keyPressed(keyCode=1)
        elif event.keysym == 'Left':
            self.currentState.keyPressed(keyCode=2)
        elif event.keysym == 'Up':
            self.currentState.keyPressed(keyCode=3)
        elif event.keysym == 'Down':
            self.currentState.keyPressed(keyCode=4)
        elif event.keysym == 'plus':
            self.currentState.keyPressed(keyCode=5)
        elif event.keysym == 'minus':
            self.currentState.keyPressed(keyCode=6)
        elif event.keysym == 'g':
            self.currentState.keyPressed(keyCode=7)
        elif event.keysym =='u':
            self.currentState.keyPressed(keyCode=8)


    def checkShiftDown(self, mod):
        return mod == 'Shift'

    def checkCTRLDown(self, mod):
        return mod == 'Control'

    def paintComponent(self):
        self.delete("all")
        for object in self.model.objects:
            object.render(self)
    
    def drawLine(self, s: Point, e: Point) -> None:
        self.create_line(s.getX(), s.getY(), e.getX(), e.getY(), fill='blue')

    def fillPolygon(self, points: List[Point]) -> None:
        P = [coord for point in points for coord in (point.getX(), point.getY())]
        
        self.create_polygon(P, fill='blue', outline='black')

    def documentChange(self, documentModel: DocumentModel):
        self.model = documentModel
        self.paintComponent()
        self.currentState.afterDraw(self)

    