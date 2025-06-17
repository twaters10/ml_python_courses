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

# The high level class in the example above (Car) is tightly coupled with the low level class (Engine). If we want to change the Engine class, 
# we have to change the Car class as well.

# Refactored Solution
from abc import ABC, abstractmethod
class EngineInterface(ABC):
    @abstractmethod
    def start(self):
        pass
    
class BasicEngine(EngineInterface):
    def start(self):
        print("Basic Engine started")

class ElectricEngine(EngineInterface):
    def start(self):
        print("Electric Engine started")
        
class DieselEngine(EngineInterface):
    def start(self):
        print("Diesel Engine started")

class Car:
    def __init__(self, engine: EngineInterface):
        self.engine = engine
        
    def start(self):
        self.engine.start()
        print("Car started")
        
# Dependency Injection
car_with_basic_engine = Car(BasicEngine())
car_with_basic_engine.start()
car_with_electric_engine = Car(ElectricEngine())
car_with_electric_engine.start()
car_with_diesel_engine = Car(DieselEngine())
car_with_diesel_engine.start()
# This design adheres to the Dependency Inversion Principle (DIP) because the high-level module (Car) depends on the abstraction 
# (EngineInterface)

# Dependency Injection offers several benefits:

# Decoupling
# Testability: By injecting dependencies, you can easily swap out implementations for testing purposes.
# Flexibility: You can change the behavior of a class without modifying its code by injecting different dependencies.
# Maintainability: You can easily manage dependencies and their configurations in one place, making the codebase cleaner and easier to maintain.
# Scalability: You can easily add new features or change existing ones without affecting the entire codebase, as long as you adhere to the abstractions defined by 
# interfaces.
# Reusability: You can reuse the same class with different dependencies, making it more versatile.