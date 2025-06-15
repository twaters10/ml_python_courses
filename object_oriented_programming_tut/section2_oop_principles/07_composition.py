# Composition involves creating complex objects by combining simpler objects.
# Recognized as a "has-a" relationship.
# Inheritance (Car is a Vehicle) vs Composition (Car has an Engine).

class Engine:
    def start(self):
        print("Engine starting")
        
class Wheels:
    def rotate(self):
        print("Wheels rotating")
    
class Chasis:
    def support(self):
        print("Chasis supporting the car")
        
class Seats:
    def sit(self):
        print("Sitting on seats")

class Car:
    def __init__(self):
        self._engine = Engine()  # Composition: Car has an Engine
        self._wheels = Wheels()  # Composition: Car has Wheels
        self._chasis = Chasis()  # Composition: Car has a Chasis  
        self._seats = Seats()

    def start(self):
        self._engine.start()
        self._wheels.rotate()
        self._chasis.support()
        self._seats.sit()
        print("Car is ready to drive")
        
car = Car()
car.start()  # Start the car, which uses its components

# When to use Composition vs Inheritance:
# Use Composition when you want to build complex objects from simpler ones.
# Use Inheritance when you want to create a specialized version of a base class.
# Composition allows for greater flexibility and easier maintenance.
# Composition is often preferred over inheritance for complex systems.
# It allows for easier changes and extensions without affecting the entire hierarchy.
# Use Inheritance when there is a clear "is-a" relationship.
# and when you want to promote code reuse through a base class.
# Composition is often more flexible than inheritance.