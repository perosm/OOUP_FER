from graphics.Point import Point
import math

class GeometryUtil:
    @staticmethod
    def distanceFromPoint(point1: Point, point2: Point) -> float:
        """
        racuna euklidsku udaljenost izmedu dvije tocke
        """
        return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

    @staticmethod
    def distanceFromLineSegment(s: Point, e: Point, p: Point) -> float:
        """
        Izračunaj koliko je točka P udaljena od linijskog segmenta određenog
		početnom točkom S i završnom točkom E. 
        Uočite: ako je točka P iznad/ispod
		tog segmenta, ova udaljenost je udaljenost okomice spuštene iz P na S-E.
		Ako je točka P "prije" točke S ili "iza" točke E, udaljenost odgovara
		udaljenosti od P do početne/konačne točke segmenta.
        """
        se = Point(e.x - s.x, e.y - s.y)
        sp = Point(s.x - p.x, s.y - p.y)
        proj = sp.x * se.x + sp.y * se.y   # vektorski umnozak
        seEuclidean = GeometryUtil.distanceFromPoint(s, e) # udaljenost izmedu s, e
        d = proj / seEuclidean # normalizirana projekcija tocke p na se

        if d <= 0: # p je iza tocke s
            return GeometryUtil.distanceFromPoint(s, p)
        elif d >= 1: # p je iza tocke e
            return GeometryUtil.distanceFromPoint(e, p)
        else: # p se nalazi izmedu s i e
            sePoint = Point(s.x + seEuclidean * d, s.y + seEuclidean * d)

        return GeometryUtil.distanceFromPoint(sePoint, p    )

