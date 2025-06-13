name = "Danny"
age = 29

print(type(name.upper()))
print(type(age))


class Dog:
    # init allows us to setup data fields for the class
    # self is a reference to the instance of the class
    # self.name, self.breed, self.owner are instance variables
    def __init__(self, name, breed, owner):
        self.name = name
        self.breed = breed
        self.owner = owner # pass owner object to the Dog class

    def bark(self):
        print("Woof!")

class Owner:
    def __init__(self, name, address, phone_number):
        self.name = name
        self.address = address
        self.phone_number = phone_number
owner1 = Owner('Emily', '123 Main St', '555-1234')
owner2 = Owner('Taylor', '456 Elm St', '555-5678')
dog1 = Dog('Bruce', 'Scottie', owner1)
dog2 = Dog('Zoey', 'Westie', owner2)

# instance of a dog class is a dog object
dog1.owner.name  # Accessing the owner's name through the dog instance
print(dog1.owner.name)  # Output: Emily
print(dog2.owner.name)  # Output: Taylor