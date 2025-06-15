# Abstraction is used to reduce complexity by hiding unnecessary details and showing only the essential features 
# of an object.

class EmailService:
    """
        Connects to an email server and sends emails. 
    """
    # This class abstracts the details of connecting to an email server, authenicating, and disconnecting.
    # The user is not interested in those details, they just want to send an email.
    def _connect(self):
        print("Connecting to email server...")
        
    def _authenticate(self):
        print("Authenticating with email server...")
        
    def _disconnect(self): 
        print("Disconnecting from email server...")
    
    # Sending an email is a public method that uses the private methods to connect, disconnect, and authenticate.
    def send_email(self, recipient, subject, body):
        self._connect()
        self._authenticate()
        print(f"Sending email to {recipient} subject: '{subject}' body: '{body}'")
        self._disconnect()

email = EmailService()
email.send_email("Taylor", "Hello!", "This is a test email.")