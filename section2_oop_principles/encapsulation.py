# Encapsulation is a fundamental principle of object-oriented programming (OOP) that restricts direct access to an 
# object's data and methods. It helps to protect the internal state of an object and ensures that it can only be 
# modified through well-defined interfaces. Helps to hide interal details of the class.

# Bad Example with no end ecapsulation:
class BadBankAccount:
    def __init__(self, balance):
        self.balance = balance
    
# account1 = BadBankAccount(0.0)
# account1.balance = -1000.0  # Directly modifying the balance attribute, which is not safe
# print(account1.balance)  # Output: -1000.0, which is not a valid state for a bank account

# Good Example with encapsulation:
class BankAccount:
    def __init__(self):
        self._balance = 0
        
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError("Deposit amount must be positive")
        
    def withdrawl(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance < amount:
            raise ValueError("Insufficient funds for withdrawal")
        self._balance -= amount
        
account2 = BankAccount()
account2.balance

        
    