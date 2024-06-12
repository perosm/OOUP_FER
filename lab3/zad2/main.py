from tkinter import *
from location_range import LocationRange
from location import Location
from text_editor import TextEditor
from text_editor_model import TextEditorModel

if __name__ == '__main__':
    # main window -> where all windows and gadgets are stored
    window = Tk()
    window.title('Master Window')
    window.geometry('600x400')
    
    # za crtanje (linije, oblici, tekst, slike)
    text = "Znakovni niz\nS više\nRedaka\nZnakovni niz\nS više\nRedaka\nZnakovni niz\nS više\nRedaka"
    textEditorModel = TextEditorModel(text)
    
    textEditor = TextEditor(window, textEditorModel=textEditorModel)
    # textEditor.pack()
    window.mainloop() # checks for events (button clicks, mouse movement...)
    