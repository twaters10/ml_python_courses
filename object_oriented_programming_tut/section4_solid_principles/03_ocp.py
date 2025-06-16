# Open/Closed Principle (OCP) - Software entities (classes, modules, functions, etc.) 
# should be open for extension but closed for modification.

from enum import Enum # Enum is used to define a set of named or constant values
import math
class ShapeType(Enum):
    CIRCLE = "circle"
    RECTANGLE = "rectangle"

# This violates the Open/Closed Principle (OCP) because if we want to add a new shape,
# we would need to modify the Shape class directly.
# Instead, we should design the class to be extensible without modification.
# class Shape():
#     # Type hinting is used to specify the type of the parameters and return values
#     def __init__(self, shape_type: ShapeType, radius: float = 0, width: float = 0, height: float = 0): 
#         self.shape_type = shape_type
#         self.radius = radius # For Circle
#         self.width = width   # For Rectangle
#         self.height = height # For Rectangle
    
#     def area(self) -> float: # returns the area of the shape as float
#         if self.shape_type == ShapeType.CIRCLE:
#             return math.pi * self.radius**2 # Area of Circle: πr² 
#         elif self.shape_type == ShapeType.RECTANGLE:
#             return self.width * self.height # Area of Rectangle: width * height
#         else:
#             raise ValueError("Unknown shape type")
        
        
# circle = Shape(ShapeType.CIRCLE, radius=5)
# rectangle = Shape(ShapeType.RECTANGLE, width=4, height=6)
# print(f"{circle.shape_type} area: {circle.area()}")
# print(f"{rectangle.shape_type} area: {rectangle.area()}") 

# This is a proper implementation because if we want to add a new shape,
# we can do so by creating a new class that extends the Shape class without modifying it.
from abc import ABC, abstractmethod # ABC is used to define an abstract base class
class Shape(ABC):
    @abstractmethod
    def calculate_area(self) -> float: # returns the area of the shape as float
        pass
    
class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
        
    def calculate_area(self) -> float:
        return math.pi * self.radius**2
    
class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        
    def calculate_area(self) -> float:
        return self.width * self.height
    
class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
        
    def calculate_area(self) -> float:
        return 0.5 * self.base * self.height

circle = Circle(radius=5)
rectangle = Rectangle(width=4, height=6)
triangle = Triangle(base=3, height=4)
print(f"Triangle area: {triangle.calculate_area()}")
print(f"Circle area: {circle.calculate_area()}")
print(f"Rectangle area: {rectangle.calculate_area()}")