# Coupling is the degree of interdependence between software modules.
# High coupling means that modules are highly dependent on each other, making them harder to change.
# Low coupling means that modules are more independent, making them easier to change and maintain.


# High Coupling Example:
class EmailSenderBad:
    def send(self, message):
        print(f"Sending email: {message}")

class OrderBad:
    def create(self):
        # Perform order creation logic
        email = EmailSenderBad()
        email.send("Order created successfully.")
        # This is an example of high coupling because the Order class is directly dependent on the EmailSender class.
        # If we want to change the way emails are sent, we have to modify the Order class as well.
# order = OrderBad()
# order.create()  # Output: Sending email: Order created successfully.

# Low Coupling Example. Add an abstraction layer to decouple the classes.
from abc import ABC, abstractmethod # abstract base class module. abstractmethod is a decorator to define abstract methods.

class NotificationService(ABC): # Abstract base class for notification service classes
    @abstractmethod
    def send_notification(self, message: str):
        pass 

# If you inherit an abstract base class, you must implement all of its abstract methods. 
# This allows you to define a common interface for all notification services, making it easier to change or extend 
# functionality without affecting the dependent classes.
class EmailService(NotificationService):
    def send_notification(self, message):
        print(f"Sending email: {message}")
        
class SMSService(NotificationService):
    def send_notification(self, message):
        print(f"Sending SMS: {message}")
        
class Order:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service
    # Now the Order class is decoupled from the specific notification service implementation.
    # It can work with any class that implements the NotificationService interface.
    def create(self):
        # Perform order creation logic
        self.notification_service.send_notification("Order created successfully.")
        
# This allows you to change the notification service without modifying the Order class.
email_service = EmailService()
sms_service = SMSService()
order1 = Order(email_service)
order2 = Order(sms_service)
order1.create()  # Output: Sending email: Order created successfully.
order2.create()  # Output: Sending SMS: Order created successfully.
