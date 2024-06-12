import tkinter
from tkinter import Tk, Canvas
from typing import *
from abc import ABC

class TextEditor(Canvas):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.focus_set()
        self.master = master
        self.pack() # stavlja GUI unutar root-a

        # self.bind('<Return>', self.destroy())
        self.bind("<Return>", self.on_enter_press)
    
    def draw_line(self, x1, y1, x2, y2, color):
        self.create_line(10, 10, 100, 10, fill='red')

    def draw_polygon(self, points):
        self.create_polygon(points)

    def draw_text(self, x1, y1, text):
        self.create_text(x1, y1, text=text)

    def on_enter_press(self, event):
        self.destroy()
        self.master.quit()

# https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events

if __name__ == '__main__':
    # glavni prozor aplikacije; tu se nalaze svi widgeti i komponente
    # container za cijelu GUI aplikaciju
    master = Tk()
    # za crtanje (linije, oblici, tekst, slike)
    textEditor = TextEditor(master, width=800, height=800, bg='white')
    
    textEditor.draw_line(10, 10, 100, 10, 'red')
    textEditor.draw_line(10, 10, 10, 100, 'red')
    textEditor.draw_polygon([100, 100, 200, 100, 200, 200, 100, 200])

    textEditor.draw_text(500, 500, text="tekst")
    textEditor.draw_text(600, 600, text="tekst2")
    
    # glavna petlja
    master.mainloop()

    """
    Vidimo da osnovni razred omogućava da grafički podsustav samostalno poziva 
    naš kod za crtanje kad god se za to javi potreba, iako je oblikovan i izveden
    davno prije naše grafičke komponente. Koji oblikovni obrazac to omogućava?
    ODG: Okvirna metoda?

    Vidimo također da naša grafička komponenta preko osnovnog razreda može dobiti
    informacije o pritisnutim tipkama bez potrebe za čekanjem u radnoj petlji. 
    Koji oblikovni obrazac to omogućava?
    ODG: Promatrač
    """