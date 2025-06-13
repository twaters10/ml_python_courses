# Static methods vs instance methods:
# Static methods are methods that belong to the class rather than any particular instance.
# They do not require an instance of the class to be called and do not have access to instance-specific data.
# Static methods are typically used for utility functions that do not need to access or modify instance-specific data.
# also useful for formatting data or performing calculations that are relevant to the class as a whole not to the instance.
# Static methods are defined using the @staticmethod decorator.
# Static and instance methods are stored in the class's __dict__ attribute, but they are accessed differently.

class BankAccount:
    MIN_BALANCE = 100  # Static attribute, shared across all instances
    
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self._balance = balance # Protected attribute, intended for internal use
        self.__log_transaction("account creation", balance)  # Private method, intended for internal use only
        
    def deposit(self, amount):
        if self._is_valid_amount(amount):
            self._balance += amount
            self.__log_transaction("deposit", amount)
        else:
            raise ValueError("Deposit amount must be positive")
    
    def withdraw(self, amount):
        if self._is_valid_amount(amount) and (self._balance - amount) >= BankAccount.MIN_BALANCE:
            self._balance -= amount
            self.__log_transaction("withdrawal", amount)
        else:
            raise ValueError("Withdrawal amount must be positive and cannot reduce balance below minimum")
    
    def _is_valid_amount(self, amount):
        # Protected method, intended for internal use only
        return amount > 0

    
    def __log_transaction(self, transaction_type, amount):
        # Private method, intended for internal use only
        print(f"Logging the {transaction_type} of {amount}. New balance: {self._balance} for {self.owner}")
    
    @staticmethod
    def is_valid_int_rate(rate):
        if 0 <= rate <= 5:
            return True
        else:
            return False
# __name__ is a special variable in Python that is set to "__main__" when the script is run directly.
if __name__ == "__main__":
    account1 = BankAccount("Alice", 500)
    account1.deposit(200)  # Deposit money into the account
    account1.deposit(100)
    account1.withdraw(150)  # Withdraw money from the account

print(BankAccount.is_valid_int_rate(3))
print(BankAccount.is_valid_int_rate(4))