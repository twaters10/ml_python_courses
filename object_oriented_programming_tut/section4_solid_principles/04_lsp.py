# Liskov Substitution Principle (LSP)
# Objects of a superclass should be replaceable with objects of a subclass without affecting the 
# correctness of the program.

# Violation of LSP
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

# class Rectangle(Shape):
#     def __init__(self, width: float = 0.0, height: float = 0.0):
#         self._width = width
#         self._height = height
    
#     @property
#     def width(self) -> float:
#         return self._width
#     @width.setter
#     def width(self, value: float):
#         self._width = value
    
#     @property
#     def height(self) -> float:
#         return self._height

#     @height.setter
#     def height(self, value: float):
#         self._height = value

#     def area(self) -> float:
#         return self._width * self._height
    
# class Square(Rectangle):
#     def __init__(self, side: float = 0.0):
#         super().__init__(side, side)
        
#     # Overriding the width setter to maintain square properties
#     @Rectangle.width.setter
#     def width(self, value: float):
#         self._width = value
#         self._height = value
#     # Overriding the height setter to maintain square properties
#     @Rectangle.height.setter
#     def height(self, value: float):
#         self._width = value
#         self._height = value
        
# This violates LSP because a Square cannot be used interchangeably with Rectangle. 
# Therefore square cannot be subclass of rectanble
# rectangle = Square()
# rectangle.width = 4
# rectangle.height = 5
# print("Rectangle Area:", rectangle.area())


# Refactored Solution
class Rectangle(Shape):
    def __init__(self, width: float = 0.0, height: float = 0.0):
        self.width = width
        self.height = height
        
    def area(self) -> float:
        return self.width * self.height
    
class Square(Shape):
    def __init__(self, side: float = 0.0):
        self.side = side
        
    def area(self) -> float:    
        return self.side**2

# Now both Rectangle and Square can be used interchangeably as they both implement the Shape interface
rectangle = Rectangle()
rectangle.width = 4
rectangle.height = 5
print("Rectangle Area:", rectangle.area())

sq = Square()
sq.side = 4
print("Square Area:", sq.area())
# This adheres to the Liskov Substitution Principle, as both Rectangle and Square can be used
# interchangeably without affecting the correctness of the program.

def return_area (shape: Shape) -> float:
    return shape.area()

# Example usage
print("Rectangle Area:", return_area(rectangle))
print("Square Area:", return_area(sq))