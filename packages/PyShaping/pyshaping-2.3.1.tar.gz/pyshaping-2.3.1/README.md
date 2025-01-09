# PyShaping Library  
A python module for math lovers or just people who needs it.  
  
## Introduction  
The module can calculate the **Areas** and **Perimeters** of 2D shapes.  
The module can calculate the **Volumes** and **Surface Areas** of 3D shapes.  
The module is lightweight, and only requires the python built-in `math` library.  
  
Every function is stored in a shape class.  
  
## Cool Features  
There are functions for 5-point stars' **area** calculation!  
There are functions for ellipsoids and spheroids' **surface area** calculation!  
There are functions for ellipse's **perimeter** calculation!  
  
## 2D Shapes  
There are various shapes!  
Including:  
 - Square
 - Rectangle
 - Triangle
 - Rhombus
 - Parallelogram
 - Kite
 - Circle
 - Trapezoid
 - Ellipse
 - Pentagon (5 side) ~ Dodecagon (12 side)
 - Starfish (5-point star shape)

Usage:  
```
from pyshaping import Pentagon

shape = Pentagon(side=10)
print(f"Area of pentagon with side length 10 is {shape.area()}")
print(f"Perimeter of pentagon with side length 10 is {shape.perimeter()}")

```  
  
## 3D Shapes
There are again, various objects you can use!  
Including:  
 - Cube
 - Prisms (Triangular ~ Dodecagonal)
 - Sphere
 - Hemisphere
 - Sphere Cap
 - Spheroid (Oblate & Prolate)
 - Ellipsoid
 - Torus (Donut shape)
 - Sausage (Wiener Sausage shape)
  
Usage:  
```
from pyshaping import Pentagon

shape = Oblate(radius=15, halfheight=5)
print(f"Volume of the oblate spheroid is {shape.volume()}")
print(f"Surface area of the oblate spheroid is {shape.surface()}")

```