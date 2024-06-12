from typing import *
from location import Location
from location_range import LocationRange
from observers import CursorObserver, TextObserver
from iterators import TextIterator

class TextEditorModel: # izdavac informacija
    """
    Sve podatke o tekstu kojeg uređujemo, 
    položaju kursora te trenutno označenom dijelu teksta (selekciji) 
    potrebno je enkapsulirati zasebnim razredom TextEditorModel.
    """
    lines = [] # lista redaka teksta
    selectionRange = LocationRange(Location(0, 0), Location(0, 0)) # koordinate (redak,stupac) početka i kraja označenog dijela teksta 
    cursorLocation = Location(0, 0) # koordinate trenutnog položaja kursora, odnosno znaka ispred kojeg se nalazi kursor
    cursorObservers: List[CursorObserver] = [] #
    textObservers: List[TextObserver] = []
    
    def __init__(self, text: str) -> None:
        self.lines = text.split("\n")
        print(len(self.lines))
        self.selectionRange = LocationRange(Location(0, 0), Location(0, 0))
        self.cursorLocation = Location(0, 0)

    def all_lines(self) -> Iterator[str]: 
        """
        vraća iterator koji prolazi kroz sve retke dokumenta
        """
        return TextIterator(self.lines)
    
    def lines_range(self, index1: int, index2: int) -> Iterator[str]:
        """
        vraća iterator koji prolazi kroz dani raspon redaka
        (prvi uključiv, drugi isključiv). 
        """
        return TextIterator(self.lines[index1, index2])
    
    def attach_cursor_observer(self, cursorObserver: CursorObserver):
        self.cursorObservers.append(cursorObserver)
    
    def detach_cursor_observers(self, cursorObserver: CursorObserver):
        self.cursorObservers.remove(cursorObserver)

    def move_cursor_left(self):
        if self.cursorLocation.y != 0: # ako nismo dosli do pocetka retka
            self.cursorLocation.y -= 1
        elif self.cursorLocation.y == 0: # ako smo dosli do pocetka retka
            if self.cursorLocation.x != 0: # ako postoji redaka prije
                self.cursorLocation.x -= 1 # umanjujemo redak
                self.cursorLocation.y = len(self.lines[self.cursorLocation.x]) # duljina novog (umanjenog) retka
            else: # ako ne postoji redaka prije
                pass
        
        self.notify_cursor_location()

    def move_cursor_right(self):
        if self.cursorLocation.y != len(self.lines[self.cursorLocation.x]): # ako nismo dosli do kraja retka
            self.cursorLocation.y += 1 # povecava cursor
        elif self.cursorLocation.y == len(self.lines[self.cursorLocation.x]): # dosli smo do kraja retka 
            if self.cursorLocation.x != len(self.lines) - 1: # ako postoji jos redaka
                self.cursorLocation.x += 1
                self.cursorLocation.y = 0
            else: # ako ne postoji redaka prije
                pass

        self.notify_cursor_location()

    def move_cursor_up(self):
        if self.cursorLocation.x != 0: # ako ima jos redaka povise
            self.cursorLocation.x -= 1 # idemo jedan red povise
        elif self.cursorLocation.x == 0: # ako smo dosli do prvog retka
            self.cursorLocation.y = 0 # prebacujemo se na prvi stupac

        self.notify_cursor_location()
    
    def move_cursor_down(self):
        if self.cursorLocation.x != len(self.lines) - 1: # ako postoji redaka ispod
            self.cursorLocation.x += 1
        elif self.cursorLocation.x == len(self.lines) - 1:
            self.cursorLocation.y = len(self.lines[self.cursorLocation.x])

        self.notify_cursor_location()

    def notify_cursor_location(self):
        for cursorObserver in self.cursorObservers:
            cursorObserver.update_cursor_location(self.cursorLocation)

    def attach_text_observer(self, textObserver: TextObserver):
        self.textObservers.append(textObserver)

    def detach_text_observer(self, textObserver: TextObserver):
        self.textObservers.remove(textObserver)

    def delete_before(self): # BackSpace
        x, y = self.cursorLocation.get_coordinates()
        if len(self.lines) == 0:
            return
        
        if y > 0 and y <= len(self.lines[x]):
            self.lines[x] = self.lines[x][:y-1] + self.lines[x][y:]
        elif y == 0 and len(self.lines[x]) == 0:
            beforeLines = self.lines[:x]
            afterLines = self.lines[x+1:]
            self.lines = beforeLines + afterLines

        self.notify_text_observers()
        self.move_cursor_left()


    def delete_after(self): # Delete
        x, y = self.cursorLocation.get_coordinates()
        if len(self.lines) == 0:
            return

        if y != len(self.lines[x]) + 1: # nalazimo se negdje u recenici
            self.lines[x] = self.lines[x][:y] + self.lines[x][y+1:]
        
        if y == len(self.lines[x]) and x < len(self.lines) - 1: # dvije recenice se spajaju
            self.lines[x] = self.lines[x] + self.lines[x+1]
            beforeLines = self.lines[:x]
            afterLines = self.lines[x+1:]
            self.lines = beforeLines + afterLines


        self.notify_text_observers()


    def delete_range(self, locationRange: LocationRange):
        start, end = locationRange.get_range()
        x1, y1 = start.copy().get_coordinates()
        x2, y2 = end.copy().get_coordinates()
        if x1 <= x2:        
            for row_idx in range(x1, min(x2+1, len(self.lines))):
                if row_idx == x1: # prvi redak
                    if x1 != x2: # ako se nalaze u razlicitim retcima
                        #print("Ostaje1", self.lines[row_idx][:y1])
                        self.lines[row_idx] = self.lines[row_idx][:y1]
                    else: # ako se nalaze u istim
                        #print("Ostaje2", self.lines[row_idx][:y1] + self.lines[row_idx][y2:])
                        self.lines[row_idx] = self.lines[row_idx][:y1] + self.lines[row_idx][y2:] # ako se nalaze u iston retku 
                elif row_idx == x2: # ako smo dosli do krajnjeg retka
                    #print("Ostaje3", self.lines[row_idx][y2:])
                    self.lines[row_idx] = self.lines[row_idx][y2:]
                else: # ako je meduredak
                    self.lines[row_idx] = ''
            self.cursorLocation = start
        elif x1 > x2:
            for row_idx in range(x1, max(x2-1, -1), -1):
                if row_idx == x1: # zadnji redak
                    if x1 != x2:
                        #print("to remove1", self.lines[row_idx][:y1])
                        self.lines[row_idx].replace(self.lines[row_idx][:y1], "")
                    else: # u istom retku kraj i pocetak
                        #print("to remove2", self.lines[row_idx][y2:y1])
                        self.lines[row_idx].replace(self.lines[row_idx][y2:y1], "")
                elif row_idx == x2:
                    #print("to remove2", self.lines[row_idx][y2:])
                    self.lines[row_idx].replace(self.lines[row_idx][y2:], "")
                else:
                    self.lines[row_idx] = ''
            self.cursorLocation = end
        tmp = []
        for line in self.lines:
            if len(line) != 0:
                tmp.append(line)
        
        
        self.lines = tmp
        
        self.notify_text_observers()
        self.notify_cursor_location()


    def get_selection_range(self) -> LocationRange:
        return self.selectionRange

    def set_selection_range(self, range: LocationRange):
        self.selectionRange = range
        #print(self.selectionRange.start, self.selectionRange.end)
        self.notify_text_observers()

    def notify_text_observers(self):
        for textObserver in self.textObservers:
            textObserver.update_text()