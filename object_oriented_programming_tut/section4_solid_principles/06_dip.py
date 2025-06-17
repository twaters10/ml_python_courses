# Dependency Inversion Principle (DIP)
# The Dependency Inversion Principle (DIP) states that high-level modules should not depend on low-level modules. Both should depend on abstractions.

class Engine:
    def start(self):
        print("Engine started")

# # High-level module (Car) depends on the abstraction (Engine) therefore it violate DIP b/c you have to change the Car class if you change the 
# Engine class.
class Car:
    def __init__(self):
        self.engine = Engine()
    
    def start(self):
        self.engine.start()
        print("Car started")

car = Car()
car.start()