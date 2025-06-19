"""
Prototyping Pattern allows objects to be copied or cloned, providing a way to create new instances by copying existing objects without explicitly 
invoking the constructor (__init__ methods)
"""
# Naive Solution
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def __init__(self):
        self.radius = 5
    
    def draw(self):
        print(f"Drawing Circle with radius {self.radius}")

class Rectangle(Shape):
    def __init__(self):
        self.width = 5
        self.height = 10
    
    def draw(self):
        print(f"Drawing rectangle with width {self.width} and height {self.height}")

# This violates the open close principle
# Its tightly coupled to each shape object and must know what properties are part of each shape type (circle --> radius)
class ShapeActions:
    def duplicate(self, shape: Shape):
        if isinstance(shape, Circle):
            new_circle = Circle()
            new_circle.radius = shape.radius
            new_circle.draw()
        elif isinstance(shape, Rectangle):
            new_rectangle = Rectangle()
            new_rectangle.width = shape.width
            new_rectangle.height = shape.height
            new_rectangle.draw()
        else:
            raise ValueError("Unsupported shape type")
        
circle = Circle()
circle.draw()

rectangle = Rectangle()
rectangle.draw()

shape_actions = ShapeActions()
shape_actions.duplicate(circle)
shape_actions.duplicate(rectangle)



        