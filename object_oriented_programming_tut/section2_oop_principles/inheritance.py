# Inheritance: the mechanism of deriving a new class from an existing class.
# A fundamental concept in object-oriented programming (OOP) that allows a class to inherit attributes and 
# methods from another class. (Subclasses: derived classes, Parent class: base class, superclass)
# Reduces verboseness and redundancy in code by allowing the reuse of existing code.

# Car is a vehicle, so it inherits from the Vehicle class.
# Bike is a vehicle, so it inherits from the Vehicle class.
# Vehicle is superclass, Car and Bike are subclasses.
# Those are is-a relationships.

class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        
    def start(self):
        print(f"{self.year} {self.brand} {self.model} is starting.")
        
    def stop(self):
        print(f"{self.year} {self.brand} {self.model} is stopping.")
        
class Car(Vehicle): # Inherits from Vehicle
    def __init__(self, brand, model, year, num_doors, num_wheels):
        super().__init__(brand, model, year)  # Call the constructor of the parent class Vehicle (super())
        self.num_doors = num_doors
        self.num_wheels = num_wheels
        
class Bike(Vehicle): # Inherits from Vehicle
    def __init__(self, brand, model, year, num_wheels):
        super().__init__(brand, model, year)  # Call the constructor of the parent class Vehicle (super())
        self.num_wheels = num_wheels
        
car = Car("Toyota", "Camry", 2020, 4, 4)
bike = Bike("Yamaha", "MT-07", 2021, 2)
print(car.__dict__) # Print the attributes of the car instance in dictionary format
print(bike.__dict__) # Print the attributes of the bike instance in dictionary format
car.start()  # Output: 2020 Toyota Camry is starting.
bike.start()  # Output: 2021 Yamaha MT-07 is starting.
car.stop()  # Output: 2020 Toyota Camry is stopping.
bike.stop()  # Output: 2021 Yamaha MT-07 is stopping.
        