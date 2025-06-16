# SRP: A class should have only one reason to change, meaning it should have only one job or responsibility.
# This principle helps in reducing the complexity of the class and makes it easier to maintain and test.
# Break up classes into smaller, more focused classes that each handle a single responsibility.s
class EmailSender:
    def send(self, recipient, message):
        # Logic to send email
        print(f"Sending email to {recipient} with '{message}'")

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        
    # def register(self):
    #     print(f"Registering user: {self.username}")
        
    #     email_sender = EmailSender()
    #     email_sender.send(self.email, f"Welcome to our service! {self.username}")

# user = User("tawate", "taylor.waters@sas.com")
# user.register()

# Refactored code to separate concerns and adhere to SRP. This is more flexinle than using composition(creating an init method in the UserService class).
# Only negative is repeatable code, but this is a small price to pay for better separation of concerns. Passing user as an arguement is more common in industry.
class UserService:
    def register(self, user):
        print(f"Registering user: {user.username}")
        
        email_sender = EmailSender()
        email_sender.send(user.email, f"Welcome to our service! {user.username}")
        
    def update(self, user):
        print(f"Updating user: {user.username}")
        
    def delete(self, user):
        print(f"Deleting user: {user.username}")
        
user = User("tawate", "taylor.waters@sas.com")
user_service = UserService()
user_service.register(user)
user_service.update(user)

user2 = User("emily", "emilyjvansickle@aol.com")
user_service.delete(user2)
user_service.register(user2)
user_service.update(user2)