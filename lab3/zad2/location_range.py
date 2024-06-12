from location import Location

class LocationRange:
    #start = Location(0, 0)
    #end = Location(0, 0)

    def __init__(self, start: Location, end: Location) -> None:
        self.start = start
        self.end = end

    def get_range(self):
        return self.start, self.end
    
    def copy(self):
        return LocationRange(self.start, self.end)
    #def __str__(self) -> str:
    #    print(f'Start: {self.start}, End: {self.end}')