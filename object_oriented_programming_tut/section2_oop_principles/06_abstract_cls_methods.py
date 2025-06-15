from abc import ABC, abstractmethod # abstract base class module. abstractmethod is a decorator to define abstract methods.

class NotificationService(ABC): # Abstract base class for notification service classes (Pass ABC)
    @abstractmethod
    def send_notification(self, message: str):
        pass # has no implementation, must be implemented by subclasses, which is why we use pass
    
# If you inherit an abstract base class, you must implement all of its abstract methods.
# This allows you to define a common interface for all notification services, making it easier to change or extend
# functionality without affecting the dependent classes.
# Also allows for polymorphism, where you can use different notification services interchangeably of differet types.
class EmailService(NotificationService):
    def send_notification(self, message):
        print(f"Sending email: {message}")
        
class SMSService(NotificationService):
    def send_notification(self, message):
        print(f"Sending SMS: {message}")
        
class Order:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service
    def create(self):
        # Perform order creation logic
        self.notification_service.send_notification("Order created successfully.")
