from abc import ABC, abstractmethod
import re
import ast, operator
from typing import *

binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}

class Sheet:
    pass
class Cell:
    pass

class Subject(ABC):
    """
    Subject interface; Methods for publisher
    """
    @abstractmethod
    def attach(self, cell: Cell) -> None:
        pass

    @abstractmethod
    def detach(self, cell: Cell) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

class Observer(ABC):
    """
    Observer interface; Methods for subscriber
    """

    @abstractmethod
    def update(self, subject: Cell) -> None:
        pass
    

class Cell(Subject, Observer):
    observers = []
    def __init__(self, sheet: Sheet, value: str, exp: str) -> None:
        self.sheet = sheet # kako bi omogucili propagiranje promjena na razini celija
        self.value = value # cacheirana vrijednost sadrzaja u numerickom podatkovnom clanu
        self.exp = exp # za cuvanje sadrzaja (izraza ili broja ali u stringu)

    def attach(self, cell: Cell) -> None:
        self.observers.append(cell) 
    
    def detach(self, cell: Cell) -> None:
        self.observers.remove(cell)
    
    def notify(self) -> None:
        for cell in self.observers: 
            cell.update()
    
    def update(self) -> None:
        self.sheet.evaluate(self)
    

class Sheet:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        # 2D Polje tablice popunjeno Cellovima
        self.cells = [[Cell(self, 0, '') for i in range(rows)] for j in range(cols)]

    def set(self, ref: str, content: str) -> None:
        """
            Sadrzaj polja na adresi ref postavlja na tekst content.
        """
        whichCell = self.cell(ref)
        tmpExp = whichCell.exp # samo zbog ispisa
        whichCell.exp = content

        usedCells = self.get_refs(whichCell)

        if len(usedCells) == 0:
            whichCell.value = int(content)
        else:
            for uc in usedCells: # svi cellovi na koje trenutni cell utjece
                if ref in uc.exp:
                    whichCell.exp = tmpExp # samo zato sta u startu mijenjan expression, pa da u ispisu ne bude npr. 'A3' = ... jer je cirkularna def 
                    raise RuntimeError("Circular definition")

                if whichCell not in uc.observers:
                    # print(f'Na {ref} se dodaje {rc.exp} cija je vrijednost:{rc.value}')
                    uc.attach(whichCell)

        self.evaluate(whichCell)
        whichCell.notify() # obavjestavamo sve cellove koje azurirani referencira


    def cell(self, ref: str) -> Cell:
        """
            Dohvaca referencu na polje zadano tekstnom adresom ref
            sheet.cell("A1") -> vraca (0,0)
        """
        cell_character_as_num = ord(ref[0]) - ord('A')
        cell_num = int(ref[1:]) - 1

        return self.cells[cell_character_as_num][cell_num]
    
    def get_refs(self, cell: Cell) -> List[Cell]:
        """
            Vraca listu svih polja koja zadano polje referencira
            Npr. ako vrijedi cell.exp=="A3-B4", 
            metoda treba vratiti polja na adresama A3 i B4
        """
        
        # https://www.w3schools.com/python/python_regex.asp
        refs = re.findall(r'[A-Z]\d', cell.exp)
        refedCells = list()
        for r in refs:
            refedCells.append(self.cell(r))
        
        return refedCells
    
    def evaluate(self, cell: Cell) -> int:
        """
            izračunava numeričku vrijednost zadanog polja
        """
        if cell.exp.isdigit():
            cell.value = int(cell.exp)
        else:
            refs = re.findall(r'[A-Z]\d', cell.exp)
            refedCells = self.get_refs(cell)
            D = {}
            for i in range(len(refs)):
                D[refs[i]] = refedCells[i].value
            cell.value = eval_expression(cell.exp, D)

 
    def print(self) -> None:
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                if self.cells[i][j].exp == '':
                    break
                print(f'Cell {chr(ord("A")+i)}{j+1}: {self.cells[i][j].exp} = {str(self.cells[i][j].value)}')


def eval_expression(exp, variables={}):
    def _eval(node):
        if isinstance(node, ast.Expression): #Num prije
            return _eval(node.body)
        elif isinstance(node, ast.Name):
            return variables[node.id]
        elif isinstance(node, ast.BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise Exception('Unsupported type {}'.format(node))

    node = ast.parse(exp, mode='eval')
    return _eval(node.body)


if __name__=="__main__":
    s=Sheet(5,5)
    print()

    s.set('A1','2')
    s.set('A2','5')
    s.set('A3','A1+A2')
    s.print()
    print()

    s.set('A1','4')
    s.set('A4','A1+A3')
    s.print()
    print()

    try:
        s.set('A1','A3')
    except RuntimeError as e:
        print("Caught exception:",e)

    s.set('A5','A3-A1')
    s.print()
    print()
    s.set('A5','A3*A1')
    s.print()
    print()
    s.set('A5','A3/A1')
    s.print()
    print()
    s.set('A5','A3-A4')
    s.print()
    print()
    