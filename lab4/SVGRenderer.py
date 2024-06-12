from typing import *
from typing import List
import os.path
from graphics.Point import Point
from Renderer import Renderer

class SVGRendererImpl(Renderer):
    def __init__(self, directory: str, fileName: str) -> None:
        self.lines: List[str] = []
        self.directory = directory
        self.fileName = fileName
        self.lines.append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">')
    
    def close(self) -> None:
        self.lines.append('</svg>')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(os.path.join(self.directory, self.fileName+".svg"), 'w') as file:
            file.write('\n'.join(self.lines))
    
    def drawLine(self, s: Point, e: Point) -> None:
        line_svg = f'<line x1="{s.x}" y1="{s.y}" x2="{e.x}" y2="{e.y}" style="stroke:blue;stroke-width:1"/>'
        self.lines.append(line_svg)
    
    def fillPolygon(self, points: List[Point]) -> None:
        points_str = " ".join(f'{p.x},{p.y}' for p in points)
        polygon_svg = f'<polygon points="{points_str}" style="stroke:blue; fill:blue; stroke-width:1" />'
        self.lines.append(polygon_svg)