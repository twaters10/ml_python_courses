# Consenting adults philosophy:
# If you want to access the email directly, you can do so.
# However, it's not recommended as it bypasses the validation logic.
# This is a private attribute, but Python does not enforce strict access control.
# It's a convention to use a single underscore to indicate that this attribute is intended for internal use.
# Accessing the email directly
# If double underscore is used, it will be name mangled therefore error will be raised if accessed directly

# When to user protected vs private attributes:
# - Protected attributes (single underscore): Intended for internal use, but can be accessed by subclasses.
# - Private attributes (double underscore): Intended for internal use only, and should not be accessed outside the class.
# In most cases, you should use protected attributes unless you have a specific reason to use private attributes, because they are less verbose and 
# easier to work with.

# Accessing and Modyfing Data
# Traditional Approach: Using getters and setters. Java Style Approach. Verbose approach.
import datetime
class User:
    def __init__(self, username, email, password):
        self.username = username
        self._email = email # Protected attribute
        self.password = password
    
    def get_email(self):
        print(f"Email accessed at {datetime.datetime.now()}")
        return self._email
    
    def set_email(self, new_email):
        # Here you could add validation logic for the email
        if "@" not in new_email:
            raise ValueError("Invalid email address")
        self._email = new_email

        
    
user1 = User("tw", "tw@hotmail.com", "1234")
user2 = User("evs", "evs@hotmail.com", "5678")
print(user1.get_email())  # Accessing email using getter method
user1.set_email("tsw@hotmail.com")
print(user1.get_email())  # Accessing updated email using getter method