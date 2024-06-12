from abc import ABC, abstractmethod
from location import Location 
from location_range import LocationRange

class CursorObserver(ABC):
    def update_cursor_location(self, location: Location) -> None:
        pass
    
class TextObserver(ABC):
    def update_text(self):
        pass
