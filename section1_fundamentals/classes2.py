class Person:
    def __init__(self, name, age):
        self.name = name # attribute
        self.age = age # attribute
    
    def greet(self): # method
        # must use the f modifier and {} around the name and age variables to format output
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

person1 = Person("Alice", 30)
person1.greet()

person2 = Person("Taylor", 30)
person2.greet()