import math


#------------- Others -------------#

def check_int(*args):
    for param in args:
        if type(param) is int or type(param) is float:
            return True
        else:
            raise TypeError("Parameter passed in should be integer or float!")



def cotangent(degrees):
    rad = math.radians(degrees)
    return (1 / math.tan(rad))



def oblate_surface_area(a, c):
    if c > a:
        raise ValueError("For an oblate ellipsoid, radius (equatorial radius) must be greater than half height (polar radius).")
    
    # angular eccentricity
    angular_eccentricity = math.acos(c / a)
    
    # Calculate
    sin_e = math.sin(angular_eccentricity)
    term = c**2 / sin_e * math.log((1 + sin_e) / math.cos(angular_eccentricity))
    S = 2 * math.pi * (a**2 + term)
    return S

def prolate_surface_area(a, c):
    if a > c:
        raise ValueError("For a prolate ellipsoid, radius (polar radius) must be greater than half width (equatorial radius).")
    
    # angular eccentricity
    angular_eccentricity = math.acos(a / c)
    
    # Calculate
    sin_e = math.sin(angular_eccentricity)
    term = a * c * angular_eccentricity / sin_e
    S = 2 * math.pi * (a**2 + term)
    return S

#------------- 2D -------------#



"""
Some of the return values are only for approximation. For example, ellipse perimeters.
The ellipse perimeter function uses Ramanujan's Approximation Theorum's Approximation Perimeter Calculation.

The others are pretty Normal for 2D shaped.

Polygons and Circles (area) are correct but is rounded to specific decimal places according to Python.
"""

class Square:
    def __init__(self, side):
        check_int(side)
        self.side = side

    def area(self):
        return self.side ** 2
    
    def perimeter(self):
        return self.side * 4


class Rect:
    def __init__(self, width: float, height: float):
        check_int(width, height)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return (self.width + self.height) * 2


class Parallelogram:
    def __init__(self, width: float, height: float):
        check_int(width, height)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
    
    def perimeter(self, sideA, sideB):
        return (sideA + sideB) * 2


class Triangle:
    def __init__(self, width: float, height: float):
        check_int(width, height)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height / 2


class Trapezoid:
    def __init__(self, top: float, bottom: float, height: float):
        check_int(top, bottom, height)
        self.top = top
        self.bottom = bottom
        self.height = height

    def area(self):
        return (self.top + self.bottom) * self.height / 2


class Circle:
    def __init__(self, radius: float):
        check_int(radius)
        self.radius = radius

    def area(self):
        return (self.radius ** 2) * math.pi
    
    def perimeter(self):
        return (self.radius * 2) * math.pi


class Ellipse:
    def __init__(self, radiusA: float, radiusB: float):
        check_int(radiusA, radiusB)
        self.radiusa = radiusA
        self.radiusb = radiusB

    def area(self):
        return (self.radiusa * self.radiusb) * math.pi
    
    def perimeter(self):
        sab = self.radiusa + self.radiusb
        segmenta = 3 * sab
        segmentb = 3 * self.radiusa + self.radiusb
        segmentc = self.radiusa + 3 * self.radiusb
        segmentd = math.sqrt(segmentb * segmentc)
        segmente = segmenta - segmentd
        answer = math.pi * segmente
        return answer


class Rhombus:
    def __init__(self, diagonalA: float, diagonalB: float):
        check_int(diagonalA, diagonalB)
        self.p = diagonalA
        self.q = diagonalB

    def area(self):
        return (self.p * self.q) / 2
    
    def perimeter(self, side: float):
        return side * 4


class Kite:
    def __init__(self, diagonalA: float, diagonalB: float):
        check_int(diagonalA, diagonalB)
        self.p = diagonalA
        self.q = diagonalB

    def area(self):
        return (self.p * self.q) / 2
    
    def perimeter(self, sidea: float, sideb: float):
        return (sidea + sideb) * 2


class Pentagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        segmenta = 5 + (2 * math.sqrt(5))
        segmentb = math.sqrt(5 * segmenta)
        answer = (1/4) * segmentb * (self.side ** 2)
        return answer

    def perimeter(self):
        return self.side * 5


class Hexagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        return ((3 * math.sqrt(3)) / 2) * (self.side ** 2)

    def perimeter(self):
        return self.side * 6


class Septagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        segmenta = (7/4) * (self.side ** 2)
        segmentb = cotangent((180 / 7))
        return segmenta * segmentb

    def perimeter(self):
        return self.side * 7


class Octagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        segment = 2 * (1 + math.sqrt(2))
        return (self.side ** 2) * segment
    
    def perimeter(self):
        return self.side * 8


class Nonagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        segmenta = (9/4) * (self.side ** 2)
        segmentb = cotangent((180 / 9))
        return segmenta * segmentb

    def perimeter(self):
        return self.side * 9


class Decagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        segmenta = (5/2) * (self.side ** 2)
        segmentb = 5 + (2 * math.sqrt(5))
        return segmenta * segmentb

    def perimeter(self):
        return self.side * 10


class Hendecagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        segmenta = (11/4) * (self.side ** 2)
        segmentb = cotangent((math.pi / 11))
        return segmenta * segmentb

    def perimeter(self):
        return self.side * 11


class Dodecagon:
    def __init__(self, side: float):
        check_int(side)
        self.side = side

    def area(self):
        segmenta = 3 * (2 + math.sqrt(3))
        return segmenta * (self.side ** 2)

    def perimeter(self):
        return self.side * 12




#------------- 3D -------------#

class Cube:
    def __init__(self, length: float, width: float, height: float):
        check_int(length, width, height)
        self.length = length
        self.width = width
        self.height = height
    
    def volume(self):
        return self.length * self.width * self.height

    def surface(self):
        seta = self.width * self.length
        setb = self.length * self.height
        setc = self.height * self.width
        return seta * 2 + setb * 2 + setc * 2


class Sphere:
    def __init__(self, radius: float):
        check_int(radius)
        self.radius = radius

    def volume(self):
        return (4/3) * (self.radius ** 3) * math.pi

    def surface(self):
        return 4 * (self.radius ** 2) * math.pi


class Hemisphere:
    def __init__(self, radius: float):
        check_int(radius)
        self.radius = radius

    def volume(self):
        return ((4/3) * (self.radius ** 3) * math.pi) / 2

    def surface(self):
        return 3 * (self.radius ** 2) * math.pi


class Spherecap:
    def __init__(self, sphereradius: float, capradius: float, capheight: float):
        check_int(sphereradius, capradius, capheight)
        self.sr = sphereradius
        self.cr = capradius
        self.ch = capheight

    def volume(self):
        return (1/6) * math.pi * self.ch * (self.cr ** 2 * 3 + self.ch ** 2)

    def surface(self):
        return 2 * self.sr * self.ch * math.pi


class TriPrism:
    def __init__(self, height: float):
        self.height = height

    def volume(self, width: float, length: float):
        return width * length / 2 * self.height

    def surface(self, baseA: float, baseB: float, baseC: float):
        tb = baseA * baseB
        sa = baseA * self.height
        sb = baseB * self.height
        sc = baseC * self.height
        return tb + sa + sb + sc


class RegularPrism:
    def __init__(self, basesides: float, baselength: float, height: float):
        check_int(basesides, baselength, height)
        if basesides > 12:
            raise ValueError("Cannot initiate prism class with a base polygon with too many sides! (Max: 12)")
        self.height = height
        self.base = basesides
        self.length = baselength

    def volume(self):
        bases = [
            0,
            0,
            0,
            Triangle(self.length, self.length).area(),
            Square(self.length).area(),
            Pentagon(self.length).area(),
            Hexagon(self.length).area(),
            Septagon(self.length).area(),
            Octagon(self.length).area(),
            Nonagon(self.length).area(),
            Decagon(self.length).area(),
            Hendecagon(self.length).area(),
            Dodecagon(self.length).area(),
        ]
        base = bases[self.base]
        return base * self.height

    def surface(self):
        bases = [
            0,
            0,
            0,
            Triangle(self.length, self.length).area(),
            Square(self.length).area(),
            Pentagon(self.length).area(),
            Hexagon(self.length).area(),
            Septagon(self.length).area(),
            Octagon(self.length).area(),
            Nonagon(self.length).area(),
            Decagon(self.length).area(),
            Hendecagon(self.length).area(),
            Dodecagon(self.length).area(),
        ]
        base = bases[self.base]
        sides = self.length * self.height * self.base
        return base * 2 + sides

class Ellipsoid:
    def __init__(self, radiusa: float, radiusb: float, halfwidth: float):
        check_int(radiusa, radiusb, halfwidth)
        self.a = radiusa
        self.b = radiusb
        self.width = halfwidth

    def volume(self):
        return (4/3) * math.pi * self.a * self.b * self.width

    def surface(self):
        a, b, c = self.a, self.b, self.width
        p = 1.6075
        term = (a**p * b**p + a**p * c**p + b**p * c**p) / 3
        S = 4 * math.pi * (term**(1 / p))
        return S


class Oblate:
    def __init__(self, radius: float, halfheight: float):
        check_int(radius, halfheight)
        self.radius = radius
        self.height = halfheight

    def volume(self):
        return (4/3) * math.pi * (self.radius ** 2) * self.height

    def surface(self):
        return oblate_surface_area(self.radius, self.height)


class Prolate:
    def __init__(self, radius: float, halfwidth: float):
        check_int(radius, halfwidth)
        self.radius = radius
        self.radius = radius
        self.width = halfwidth

    def volume(self):
        return (4/3) * math.pi * (self.radius ** 2) * self.width

    def surface(self):
        return prolate_surface_area(self.radius, self.width)


class Torus:
    def __init__(self, inner: float, outer: float):
        check_int(inner, outer)
        self.inner = inner
        self.outer = outer

    def volume(self):
        return ((math.pi ** 2) / 4) * (self.inner + self.outer) * ((self.outer - self.inner) ** 2)

    def surface(self):
        return (math.pi ** 2) * (self.outer ** 2 - self.inner ** 2)


class Sausage:
    def __init__(self, length: float, height: float):
        check_int(length, height)
        self.length = length
        self.height = height

    def volume(self):
        return ((math.pi * (self.height ** 2)) / 4) * (self.length - (self.height / 2))

    def surface(self):
        return math.pi * self.height * self.length


class Starfish:
    def __init__(self, sidelength):
        check_int(sidelength)
        self.length = sidelength

    def area(self):
        return 0.4 * 5 * (self.length ** 2) / math.tan(math.pi / 5)

    def perimeter(self):
        return self.length * 10
