class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    def say_hi_to_user(self, user):
        # access username of the user class input into this method
        print(f"Sending message to {user.username}: Hi {user.username} it is {self.username}!")
        
user1 = User("tw", "tw@hotmail.com", "1234")
user2 = User("evs", "evs@hotmail.com", "5678")

user1.say_hi_to_user(user2)  # Sending message to evs: Hi evs it is tw!

# modifying the email attribute of user1
# but need to ensure that the email is valid. 
user1.email = "tsw@gmail.com"
print(user1.email)
    
    