import tkinter
from tkinter.font import Font # https://stackoverflow.com/questions/53654549/tkinter-relation-between-font-type-and-width
from tkinter import Tk, Frame, Button, Canvas
from typing import *
from text_editor_model import TextEditorModel
from location import Location
from location_range import LocationRange
from observers import CursorObserver, TextObserver

# https://stackoverflow.com/questions/19861689/check-if-modifier-key-is-pressed-in-tkinter
mods = {
    0x0000: '',
    0x0001: 'Shift',
    0x0002: 'Caps Lock',
    0x0004: 'Control',
    0x0008: 'Left-hand Alt',
    0x0010: 'Num Lock',
    0x0080: 'Right-hand Alt',
    0x0100: 'Mouse button 1',
    0x0200: 'Mouse button 2',
    0x0400: 'Mouse button 3'
}


class TextEditor(Frame, CursorObserver, TextObserver): # Vaša komponenta treba se temeljiti na primitivnim prozorima
    # https://www.youtube.com/watch?v=xYqWu7ZF4rk&list=PLpMixYKO4EXfUS_7jgbfUKPtWSHQ1RMC4
    # https://www.youtube.com/watch?v=pwUsdn-UdF4&list=PLpMixYKO4EXfUS_7jgbfUKPtWSHQ1RMC4&index=10
    # https://stackoverflow.com/questions/72454562/difference-between-frame-and-canvas-tkinter
    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
    # widget -> text, buttons, checkboxes, menus, frames...
    def __init__(self, window: Tk, textEditorModel: TextEditorModel):
        super().__init__(window)
        # self.focus_set()
        self.window = window # Tk -> main window
        self.textEditorModel = textEditorModel
        self.textEditorModel.attach_cursor_observer(self)
        self.textEditorModel.attach_text_observer(self)
        self.startX = 14
        self.startY = 14
        self.font = Font(family='Arial', size=14) # font family, size,
        self.font_width = self.font.measure("W")
        self.font_height = self.font.metrics("linespace") - 3
        self.cursorPositionBefore = Location(0, 0)
        self.pack() # for placing GUI inside root/master
        self.initialize_canvas()

    def initialize_canvas(self):
        self.canvas = Canvas(self, height=400, width=600, bg='white')
        # https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
        # self.canvas.bind('<Button-1>', self.action_on_button1)
        self.canvas.bind('<Key>', self.action_on_key)
        #self.canvas.bind('<KeyRelease>', self.action_on_key_release)
        self.canvas.pack()
        self.canvas.focus_set() # Direct input focus to this widget.
        self.draw_text()
    
    def update_cursor_location(self, location: Location) -> None:
        #self.textEditorModel.set_cursor_location()
        # self.textEditorModel.cursorLocation = Location(event.x, event.y)
        # print(self.textEditorModel.cursorLocation)
        # print(f'({location})')
        self.draw_cursor(*self.cursor_location_to_pixel(self.textEditorModel.cursorLocation.x, self.textEditorModel.cursorLocation.y))

    def update_text(self):
        self.draw_text()
        self.draw_cursor(*self.cursor_location_to_pixel(self.textEditorModel.cursorLocation.x, self.textEditorModel.cursorLocation.y))
        self.draw_selection()

    def action_on_key(self, event) -> None:
        mod = mods[event.state]
        # referenca ?

        if event.keysym in ['Left', 'Right', 'Up', 'Down'] and mod != 'Shift':
            self.cursorPositionBefore = self.textEditorModel.cursorLocation.copy() # prije nego sto smo stisli shift

        if event.keysym == 'Left': # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
            self.textEditorModel.move_cursor_left()
            if mod == 'Shift':
                self.textEditorModel.set_selection_range(LocationRange(self.cursorPositionBefore, self.textEditorModel.cursorLocation))
            else:
                self.textEditorModel.set_selection_range(LocationRange(self.textEditorModel.cursorLocation, self.textEditorModel.cursorLocation))
        elif event.keysym == 'Right':
            self.textEditorModel.move_cursor_right()
            if mod == 'Shift':
                self.textEditorModel.set_selection_range(LocationRange(self.cursorPositionBefore, self.textEditorModel.cursorLocation))
            else:
                self.textEditorModel.set_selection_range(LocationRange(self.textEditorModel.cursorLocation, self.textEditorModel.cursorLocation))
        elif event.keysym == 'Up':
            self.textEditorModel.move_cursor_up()
            if mod == 'Shift':
                self.textEditorModel.set_selection_range(LocationRange(self.cursorPositionBefore, self.textEditorModel.cursorLocation))
            else:
                self.textEditorModel.set_selection_range(LocationRange(self.textEditorModel.cursorLocation, self.textEditorModel.cursorLocation))
        elif event.keysym == 'Down':
            self.textEditorModel.move_cursor_down()
            if mod == 'Shift':
                self.textEditorModel.set_selection_range(LocationRange(self.cursorPositionBefore, self.textEditorModel.cursorLocation))
            else:
                self.textEditorModel.set_selection_range(LocationRange(self.textEditorModel.cursorLocation, self.textEditorModel.cursorLocation))
        elif event.keysym == 'BackSpace':
            if self.textEditorModel.selectionRange.start != self.textEditorModel.selectionRange.end:
                self.textEditorModel.delete_range(self.textEditorModel.selectionRange.copy())
            else:
                self.textEditorModel.delete_before()
        elif event.keysym == 'Delete':
            if self.textEditorModel.selectionRange.start != self.textEditorModel.selectionRange.end:
                self.textEditorModel.delete_range(self.textEditorModel.selectionRange.copy())
            else:
                self.textEditorModel.delete_after()

        
    
    def draw_text(self):
        self.canvas.delete("all")
        for row_idx, line in enumerate(self.textEditorModel.all_lines()):
            self.canvas.create_text(self.startX, #  - (self.font_height / 2),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_text.html
                                    self.startY * (row_idx + 1) + (self.font_height),
                                    anchor=tkinter.SW,
                                    font=self.font,
                                    text=line,
                                    fill='black')
        
    def draw_selection(self):
        selectionRange = self.textEditorModel.get_selection_range()
        start, end = selectionRange.get_range()
        x1, y1 = start.get_coordinates()
        x2, y2 = end.get_coordinates()

        if x1 == x2 and y1 == y2:
            return
        
        if x2 >= x1:
            for row_idx in range(x1, min(x2+1, len(self.textEditorModel.lines))):
                line = self.textEditorModel.lines[row_idx]
                if row_idx == x1:
                    line = line[y1:] if x1 != x2 else line[y1:y2] 
                    self.canvas.create_rectangle(
                        self.startX + y1 * self.font_width / 2,
                        self.startY * (row_idx + 1) + self.font_height,
                        self.startX + len(line) * self.font_width / 2,
                        self.startY * (row_idx + 1) - self.font_height / 2,
                        outline='gray')
                elif row_idx == x2:
                    line = line[:y2]
                    self.canvas.create_rectangle(
                        self.startX,
                        self.startY * (row_idx + 1) + self.font_height,
                        self.startX + y2 * self.font_width / 2,
                        self.startY * (row_idx + 1) - self.font_height / 2,
                        outline='gray')
                else:
                    self.canvas.create_rectangle(
                        self.startX + y1 * self.font_width / 2,
                        self.startY * (row_idx + 1) + self.font_height,
                        self.startX + len(line) * self.font_width / 2,
                        self.startY * (row_idx + 1) - self.font_height / 2,
                        outline='gray')
        else:
            for row_idx in range(x1, max(x2 - 1, -1), -1):
                line = self.textEditorModel.lines[row_idx]
                if row_idx == x1:
                    line = line[y1:] if x1 != x2 else line[y1:y2]
                    self.canvas.create_rectangle(
                        self.startX + (x1 + len(line)) * self.font_width / 2,
                        self.startY * (row_idx + 1) - self.font_height / 2,
                        self.startX + x1 * self.font_width / 2,
                        self.startY * (row_idx + 1) + self.font_height / 2,
                        outline='gray'
                    )
                elif row_idx == x2:
                    line = line[:y2]
                    self.canvas.create_rectangle(
                        self.startX + y2 * self.font_width / 2,
                        self.startY * (row_idx + 1) - self.font_height / 2,
                        self.startX,
                        self.startY * (row_idx + 1) + self.font_height / 2,
                        outline='gray'
                    )
                else:
                    self.canvas.create_rectangle(
                        self.startX + len(line) * self.font_width / 2,
                        self.startY * (row_idx + 1) - self.font_height / 2,
                        self.startX,
                        self.startY * (row_idx + 1) + self.font_height / 2,
                        outline='gray'
                    )
        


    def cursor_location_to_pixel(self, x_char, y_char):
        """
        x_char -> oznacava redni broj reda -> y koordinata u canvasu (visina)
        y_char -> oznacava redni broj stupca -> x koordinata u canvasu (sirina)
        """
        return self.startX + (y_char) * self.font_width / 2, self.startY * x_char + self.font_height

    def draw_cursor(self, x, y):
        self.canvas.delete('cursor')
        #print("DRAW CURSOR", x, y, flush=True)
        self.canvas.create_line(x, y - self.font_height / 2, x, y + self.font_height / 2 + 3, tag='cursor')

