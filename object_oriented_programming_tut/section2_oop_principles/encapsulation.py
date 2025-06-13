# Encapsulation is a fundamental principle of object-oriented programming (OOP) that restricts direct access to an 
# object's data and methods. It helps to protect the internal state of an object and ensures that it can only be 
# modified through well-defined interfaces. Helps to hide interal details of the class.

# Bad Example with no end ecapsulation:
class BadBankAccount:
    def __init__(self, balance):
        self.balance = balance
    
# account1 = BadBankAccount(0.0)
# account1.balance = -1000.0  # Directly modifying the balance attribute, which is not safe. 
                              # You want a method to update balance
# print(account1.balance)  # Output: -1000.0, which is not a valid state for a bank account

# Good Example with encapsulation:
# BankAccount encapsulates the account balance and uses the deposit and withdraw methods to modify it.
# This prevents direct access to the balance attribute, ensuring that it can only be modified through these methods.
class BankAccount:
    def __init__(self):
        self._balance = 0.0 # Protected attribute, intended for internal use
        self.__log_transaction("account creation", self._balance)  # Private method, intended for internal use only
    @property
    def balance(self):
        return self._balance 
    
    def deposit(self, amount):
        if amount > 0.0:
            self._balance += amount
        else:
            raise ValueError("Deposit amount must be positive")
        self.__log_transaction("deposit", amount)
        
    def withdrawl(self, amount):
        if amount <= 0.0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance < amount:
            raise ValueError("Insufficient funds for withdrawal")
        self._balance -= amount
        self.__log_transaction("withdrawal", amount)
        
    def __log_transaction(self, transaction_type, amount):
        # Private method, intended for internal use only
        print(f"Logging the {transaction_type} of {amount}. New balance: {self._balance}")
        
account2 = BankAccount()
account2.deposit(1000)
account2.withdrawl(500)
account2.withdrawl(100)

        
    