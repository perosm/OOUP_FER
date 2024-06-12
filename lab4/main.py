from typing import *
from tkinter import Tk
from graphics.GraphicalObject import GraphicalObject
from graphics.LineSegment import LineSegment
from graphics.Oval import Oval
from GUI import GUI

if __name__ == '__main__':
    objects: List[GraphicalObject] = []
    objects.append(LineSegment())
    objects.append(Oval())

    root = Tk()
    root.geometry("600x400")
    gui = GUI(root, objects)
    root.mainloop()
