from abc import ABC, abstractmethod
from typing import *
from time import sleep
from datetime import datetime
from typing import List

class Izvor(ABC): # ABC - Abstract Base Class
    @abstractmethod
    def ucitaj_broj(self):
        pass

class TipkovnickiIzvor(Izvor):
    def __init__(self) -> None:
        super().__init__()

    def ucitaj_broj(self) -> int:
        return int(input('Upisite broj: '))

class DatotecniIzvor(Izvor):
    imeDatoteke = None
    red = -1
    def __init__(self, imeDatoteke: str) -> None:
        self.imeDatoteke = imeDatoteke

    def ucitaj_broj(self) -> int:
        f = open(self.imeDatoteke, "r")
        redovi = f.readlines()
        self.red += 1
        return -1 if self.red >= len(redovi) else int(redovi[self.red])
        
         
class Akcija(ABC):
    @abstractmethod
    def obavijesti(self, brojevi: List[int]) -> None:
        pass

class AkcijaZapis(Akcija):
    imeDatoteke = None
    def __init__(self, imeDatoteke: str) -> None:
        self.imeDatoteke = imeDatoteke

    def obavijesti(self, brojevi: List[int]) -> None:
        with open(self.imeDatoteke, 'a') as f:
            vrijemeDatum = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            # print(''.join(str(brojevi)), vrijemeDatum)
            f.write(f'Vrijeme zapisa: {vrijemeDatum}\n\t')
            f.write(''.join(str(brojevi)))
            f.write('\n')

class AkcijaSuma(Akcija):
    def obavijesti(self, brojevi: List[int]) -> None:
        print(f'Suma svih elemenata: {sum(brojevi)}')

class AkcijaProsjek(Akcija):
    def obavijesti(self, brojevi) -> None:
        print(f'Prosjek svih elemenata: {sum(brojevi) / len(brojevi)}')

class AkcijaMedijan(Akcija):
    def obavijesti(self, brojevi: List[int]) -> None:
        medijan = 0
        sortirani_brojevi = sorted(brojevi)
        if len(brojevi) % 2 == 0:
            medijan = sortirani_brojevi[len(brojevi) // 2]
        else:
            medijan = (sortirani_brojevi[len(brojevi) // 2] + sortirani_brojevi[len(brojevi) // 2 + 1]) / 2
        
        print(f'Medijan svih elemenata: {medijan}')

class SlijedBrojeva:
    brojevi = []
    izvor = None
    akcije = []

    def __init__(self, brojevi: List[int], izvor: Izvor, akcije: List[Akcija]) -> None:
        self.brojevi = brojevi
        self.izvor = izvor
        self.akcije = akcije

    def dodaj_pretplatnika(self, akcija: Akcija) -> None:
        self.akcije.append(akcija)

    def izbrisi_pretplatnika(self, akcija: Akcija) -> None:
        self.akcije.remove(akcija)

    def kreni(self) -> None:
        while True:
            broj = self.izvor.ucitaj_broj()
            if broj == -1:
                break
            self.brojevi.append(broj)
            sleep(1)
            self.obavijesti_pretplatnike(self.brojevi)
        
        return
    
    def obavijesti_pretplatnike(self, brojevi) -> None:
        for i in range(len(self.akcije)):
            self.akcije[i].obavijesti(brojevi=brojevi)



 
if __name__ == '__main__':
    izvor = TipkovnickiIzvor()
    akcijaSuma = AkcijaSuma()
    akcijaMedijan = AkcijaMedijan()
    akcijaProsjek = AkcijaProsjek()
    akcijaZapis = AkcijaZapis(imeDatoteke='akcijazapis.txt')
    akcije = [akcijaSuma, akcijaMedijan, akcijaZapis]
    sb = SlijedBrojeva(brojevi=[1, 2, 3], izvor=izvor, akcije=akcije)
    sb.dodaj_pretplatnika(akcijaProsjek)
    # sb.izbrisi_pretplatnika(akcijaProsjek)
    sb.kreni()

    sb.izvor = DatotecniIzvor(imeDatoteke='data.txt')
    sb.kreni()

