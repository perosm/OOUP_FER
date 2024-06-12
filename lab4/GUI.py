from tkinter import *
from typing import *
import os
from graphics.GraphicalObject import GraphicalObject, GraphicalObjectListener
from model.DocumentModel import DocumentModel
from CustomCanvas import CustomCanvas
from graphics.Oval import Oval
from graphics.LineSegment import LineSegment
from graphics.Point import Point
from state.State import State
from state.IdleState import IdleState
from state.AddShapeState import AddShapeState
from state.SelectShapeState import SelectShapeState
from state.EraserState import DeleteShapeState
from SVGRenderer import SVGRendererImpl
from graphics.CompositeShape import CompositeShape

class GUI(Frame):
    objects: List[GraphicalObject] = [] # lista graf. objekata s kojima ce moci graditi crtez
    model: DocumentModel = None #  Prozor također definira jedan primjerak modela dokumenta
    currentState: State = IdleState() 

    def __init__(self, root, objects: List[GraphicalObject]) -> None:
        super().__init__(root)
        self.root = root
        self.objects = objects
        self.createButtons() # za stvaranje gumbova na alatnoj traci
        self.model = DocumentModel()
        self.currentState = IdleState()
        self.focus_set()
        self.pack()
        self.canvas = CustomCanvas(self.root, self.model, self.currentState) # TO DO: Napravit platno za crtanje
        self.model.addDocumentModelListener(self.canvas)
        # self.canvas.bind('<Key>', self.returnToInitialState)
        self.bind('<Escape>', self.returnToInitialState) # https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
        

    def createButtons(self):
        toolbar = Frame(self.master, bd=1, relief=RAISED)
        toolbar.pack(side=TOP, fill=X)

        lineSegmentButton = Button(toolbar, text=self.objects[0].getShapeName(), command=self.lineSegmentCommandButton)
        lineSegmentButton.pack(side=LEFT)

        ovalButton = Button(toolbar, text=self.objects[1].getShapeName(), command=self.ovalCommandButton)
        ovalButton.pack(side=LEFT)

        selectButton = Button(toolbar, text="Select", command=self.selectCommandButton)
        selectButton.pack(side=LEFT)

        deleteButton = Button(toolbar, text="Delete", command=self.deleteCommandButton)
        deleteButton.pack(side=LEFT)

        exportToSVGButton = Button(toolbar, text="SVG Export", command=self.exportToSVGCommandButton)
        exportToSVGButton.pack(side=LEFT)

        saveButton = Button(toolbar, text="Save", command=self.saveComandButton)
        saveButton.pack(side=LEFT)

        loadButton = Button(toolbar, text="Load", command=self.loadCommandButton)
        loadButton.pack(side=LEFT)

    def lineSegmentCommandButton(self):
        print(f'Promjena stanja u AddShapeState')
        self.currentState = AddShapeState(model=self.model, prototype=LineSegment())
        self.canvas.currentState = self.currentState

    def ovalCommandButton(self):
        print(f'Promjena stanja u AddShapeState')
        self.currentState = AddShapeState(model=self.model, prototype=Oval())
        self.canvas.currentState = self.currentState

    def selectCommandButton(self):
        print(f'Promjena stanja u SelectState')
        self.currentState = SelectShapeState(model=self.model)
        self.canvas.currentState = self.currentState


    def deleteCommandButton(self):
        print(f'Promjena stanja u DeleteState')
        self.currentState = DeleteShapeState(model=self.model, canvas=self.canvas)
        self.canvas.currentState = self.currentState

    def exportToSVGCommandButton(self):
        directoy = input("Upisite ime direktorija za spremanje: ")
        fileName = input("Upisite ime file-a za spremanje: ")
        r = SVGRendererImpl(directory=directoy, fileName=fileName)
        for object in self.model.objects:
            object.render(r=r)
        r.close()
    
    def saveComandButton(self):
        directory = input("Upisite ime direktorija za spremanje: ")
        fileName = input("Upisite ime file-a za spremanje: ")
        rows: List[str] = []
        for object in self.model.objects:
            object.save(rows=rows)

        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, fileName+".txt"), 'w') as file:
            file.writelines(rows)

    def loadCommandButton(self):
        directory = input("Upisite ime direktorija za loadanje: ")
        fileName = input("Upisite ime file-a za loadanje: ")
        rows: List[str] = []
        with open(os.path.join(directory, fileName+".txt"), 'r') as file:
            rows = file.readlines()
        file.close()
        mappings = {"@LINE": LineSegment(),
                    "@OVAL": Oval(),
                    "@COMP": CompositeShape()}
        
        stack: List[GraphicalObject] = []
        for row in rows:
            elements: List[str] = row.strip().split(" ")
            obj = mappings[elements[0]]
            data = ' '.join(elements[1:])
            obj.load(stack, data)
        
        self.canvas.model = self.model
        for object in stack:
            self.model.addGraphicalObject(object)

    def returnToInitialState(self, event):
        print(f'Promjena stanja u IdleState')
        self.currentState = IdleState()
        self.canvas.currentState = self.currentState
    
