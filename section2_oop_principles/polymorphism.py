# Polymorphism is a core concept in OOP that allows objects of different classes to be treated as objects of a 
# common superclass. It enables a single interface to represent different underlying forms (data types).
# In Python, polymorphism is often achieved through method overriding and duck typing.


# No polymorphism example:
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        
    def start(self):
        print(f"{self.year} {self.brand} {self.model} is starting.")
        
    def stop(self):
        print(f"{self.year} {self.brand} {self.model} is stopping.")    
        
        
class MotorBike:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        
    def start_bike(self):
        print(f"{self.year} {self.brand} {self.model} is starting.")
        
    def stop_bike(self):
        print(f"{self.year} {self.brand} {self.model} is stopping.")

# List of vehicles to inspect
vehicles = [
    Car("Toyota", "Camry", 2020),
    MotorBike("Yamaha", "MT-07", 2021,)
]

# Loop through vehicles and inspect. But there are two different classes, so we have to call the methods for 
# each class separately since they dont have common methods and if logic is used to check the type of each vehicle.
# This gets ugly and verbose as you add more class of Vehicles
# for vehicle in vehicles:
#     if isinstance(vehicle, Car):
#         vehicle.start()
#         vehicle.stop()
#         print({type(vehicle).__name__})
#     elif isinstance(vehicle, MotorBike):
#         vehicle.start_bike()
#         vehicle.stop_bike()
#         print({type(vehicle).__name__})
#     else:
#         raise Exception("Unknown vehicle type")


# Example with Polymorphism:
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
        
    def start(self): # Overriding the start method to provide specific behavior for Car
        print(f"{self.year} {self.brand} {self.model} with {self.num_doors} doors and {self.num_wheels} wheels is starting.")
        
class MotorBike(Vehicle): # Inherits from Vehicle
    def __init__(self, brand, model, year, num_wheels):
        super().__init__(brand, model, year)  # Call the constructor of the parent class Vehicle (super())
        self.num_wheels = num_wheels
        
    def start(self): # Overriding the start method to provide specific behavior for MotorBike
        print(f"{self.year} {self.brand} {self.model} with {self.num_wheels} wheels is starting.")
        
class Plane(Vehicle):
    def __init__(self, brand, model, year, num_engines):
        super().__init__(brand, model, year)
        self.num_engines = num_engines
        
    def start(self): # Overriding the start method to provide specific behavior for Plane
        print(f"{self.year} {self.brand} {self.model} with {self.num_engines} engines is starting.")
        
        
# List of vehicles to inspect
# Type hinting with Vehicle superclass (vehicles: list[Vehicle]) and therefore you do not need to check if isinstance of Vehicle.
vehicles: list[Vehicle] = [
    Car("Toyota", "Camry", 2020, 4, 4),
    MotorBike("Yamaha", "MT-07", 2021, 2),
    Plane("Boeing", "747", 2019, 4),
    Plane("Airbus", "A32neo", 2020, 2)
]

# Loop through vehicles and inspect.
for vehicle in vehicles:
    vehicle.start()
    vehicle.stop()
    print({type(vehicle).__name__})