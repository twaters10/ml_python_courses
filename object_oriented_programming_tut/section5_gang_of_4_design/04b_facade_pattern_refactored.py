""" 
Structural Design Patterns

Focus on the composition of classes and objects to form structures and systems
Help to achieve the following in software development:
    Promote code reusability and modularity
    Enhance flexibility and extensibility. Loose coupling.
    Improve performance and resource utilization

Facade Pattern:
    provides a simplified interface to a complex system, encapsulating the complexities of multiple subsystems into a single unified interface for
    clients
"""

# Naive Solution

class OrderRequest:
    def __init__(self):
        self.name = "danny"
        self.card_number = "1234"
        self.amount = 20.99
        self.address = "102 Parkway Drive"
        self.item_ids = ["123", "456"] # list of ids the user wants to order
        
class Authentication:
    def authenticate(self) -> bool:
        return True # for example simplicity
    
class Inventory:
    def check_inv(self, item_id: str) -> bool:
        return True # for example simplicity

    def reduce_inv(self, item_id:str, amount:int):
        print(f"Reducing inventory of {item_id} by {amount}")
        
class Payment:
    def __init__(self, name:str, card_number:str, amount:float):
        self.name = name
        self.card_number = card_number
        self.amount = amount
        
    def pay(self):
        print(f"Charging card with name {self.name}")
        
class OrderFulfillment:
    def __init__(self, inventory: Inventory):
        self._inventory = inventory
        
    def fulfill(self, name:str, address:str, items:list[str]):
        print("inserting order into database")
        for item in items:
            self._inventory.reduce_inv(item, 1)

# Add interface class for refactored solution. This can be very useful for ML related classes to abstract all the complexity away here rather 
# than in the main script.
class OrderService:
    def create(self, order_request):
        auth = Authentication()
        auth.authenticate()
        inventory = Inventory()
        for item_id in order_req.item_ids:
            inventory.check_inv(item_id)

        payment = Payment(order_request.name, order_request.card_number, order_request.amount)
        payment.pay()

        order_fulfillment = OrderFulfillment(inventory)
        order_fulfillment.fulfill(order_request.name, order_request.address, order_request.item_ids)        
                   
order_req = OrderRequest()
order_service = OrderService()
order_service.create(order_req)


