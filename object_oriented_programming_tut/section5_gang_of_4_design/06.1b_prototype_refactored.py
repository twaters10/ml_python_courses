"""
Prototyping Pattern allows objects to be copied or cloned, providing a way to create new instances by copying existing objects without explicitly 
invoking the constructor (__init__ methods)
"""
# Refactored Solution. Logic for duplicating a shape can be moved to the concrete shape class rather than having it all in shapeactions.duplicate.
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def duplicate(self) -> 'Shape': #forward reference to shape. needed to use the draw method in the ShapeActions class
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        
    def duplicate(self):
        new_circle = Circle(self.radius)
        return new_circle
    
    def draw(self):
        print(f"Drawing Circle with radius {self.radius}")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def duplicate(self):
        new_rectangle = Rectangle(self.width, self.height)
        return new_rectangle
    
    def draw(self):
        print(f"Drawing rectangle with width {self.width} and height {self.height}")

# This violates the open close principle
# Its tightly coupled to each shape object and must know what properties are part of each shape type (circle --> radius)
class ShapeActions:
    def duplicate(self, shape: Shape):
        new_shape = shape.duplicate()
        new_shape.draw()
        
shape_actions = ShapeActions()
circle = Circle(5)
rectangle = Rectangle(10, 20)
circle.draw()
rectangle.draw()
shape_actions.duplicate(circle)
shape_actions.duplicate(rectangle)



        