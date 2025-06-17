# Interface Segregation Principle (ISP)

# The Interface Segregation Principle (ISP) states that no client should be forced to depend on methods/interfaces it does not use.
# Encourages fine grained interfaces. Cleaner and more maintainable code.

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def volume(self) -> float:
        pass
    
class Circle(Shape):
    def __init__(self, radius: float = 0.0):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14 * self.radius ** 2
    
    # violates ISP because Circle does not have a volume method
    def volume(self) -> float:
        raise NotImplementedError("Circle does not have volume")
    
class Sphere(Shape):
    def __init__(self, radius: float = 0.0):
        self.radius = radius
        
    def area(self) -> float:
        return 4 * 3.14 * self.radius ** 2
    
    def volume(self) -> float:
        return (4/3) * 3.14 * self.radius ** 3
    
class Rectangle(Shape):
    def __init__(self, width: float = 0.0, height: float = 0.0):
        self.width = width
        self.height = height
    def area(self) -> float:
        return self.width * self.height
    def volume(self) -> float:
        raise NotImplementedError("Rectangle does not have volume")



circle = Circle(5)
print("Circle Area:", circle.area())
try:
    print("Circle Volume:", circle.volume())
except NotImplementedError as e:
    print(e)
sphere = Sphere(5)
print("Sphere Area:", sphere.area())
print("Sphere Volume:", sphere.volume())
# This design violates ISP because Circle is forced to implement a volume method that it does not use.

# Refactored Solution
class Shape2D(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
class Shape3D(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def volume(self) -> float:
        pass
    
class Circle2D(Shape2D):
    def __init__(self, radius: float = 0.0):
        self.radius = radius
    def area(self) -> float:
        return 3.14 * self.radius ** 2
class Sphere3D(Shape3D):
    def __init__(self, radius: float = 0.0):
        self.radius = radius
    def area(self) -> float:
        return 4 * 3.14 * self.radius ** 2
    def volume(self) -> float:
        return (4/3) * 3.14 * self.radius ** 3
    
    
# Example usage
circle2d = Circle2D(5)
print("Circle2D Area:", circle2d.area())
sphere3d = Sphere3D(5)
print("Sphere3D Area:", sphere3d.area())
print("Sphere3D Volume:", sphere3d.volume())

# This design adheres to ISP by separating 2D and 3D shapes into different interfaces.