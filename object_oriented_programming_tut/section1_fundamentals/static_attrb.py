# Static attributes aew attributes that are shared across all instances of a class.
# They are defined at the class level and can be accessed using the class name or an instance of the class.
# Static attributes should be used when you want to maintain a value that is common to all instances of the class, 
# such as a count of instances created or a configuration setting.
class User:
    # Static attribute
    user_count = 0  # This will be shared across all instances of the User class

    def __init__(self, username, email, password):
        self.username = username
        self._email = email  # Protected attribute
        self.password = password
        User.user_count += 1  # Increment the user count whenever a new instance is created


    def display_user(self):
        print(f"Username: {self.username}, Email: {self._email}")
        
    # @classmethod
    # def get_user_count(cls):
    #     return cls.user_count
    
user1 = User("tw", "tw@hotmail.com", "1234")
user2 = User("evs", "evs@hotmail.com", "5678")

print(User.user_count)  # Accessing static attribute using class name
print(user1.user_count)  # Accessing static attribute using instance of the class
print(user2.user_count)  # Accessing static attribute using another instance of the class
