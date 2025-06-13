# Access Modifiers
# This file contains the implementation of properties in Python. (rather than getter/setter methods)

import datetime
class User:
    def __init__(self, username, email, password):
        self.username = username
        self._email = email # Protected attribute
        self.password = password
        
    @property #this is a decorator that turns the method into a property
    def email(self):
        print(f"Email accessed at {datetime.datetime.now()}")
        return self._email
    
    @email.setter #this is a decorator that turns the method into a setter for the email property
    def email(self, new_email):
        # Here you could add validation logic for the email
        if "@" not in new_email:
            raise ValueError("Invalid email address: must contain '@'")
        self._email = new_email
        
user1 = User("tw", "tw@hotmail.com", "1234")
user2 = User("evs", "evs@hotmail.com", "5678")
print(user1.email)  # Accessing email using property. (this is okay!) and doesn't require calling a getter method.
user1.email = "new_email@sas.com"
print(user1.email)