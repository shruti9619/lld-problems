class Item:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price

class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0

    def add_item(self, quantity: int, item: Item):
        self.inventory[item.id] = {
            'quantity': quantity,
            'item': item,
        }

    def insert_money(self, amount):
        self.balance += amount

    def vend_item(self, item_id):
        if item_id not in self.inventory:
            raise ValueError("Item not found")
        if self.inventory[item_id]['quantity'] <= 0:
            raise ValueError("Item out of stock")
        self.inventory[item_id]['quantity'] -= 1
        return self.inventory[item_id]['item']
    
    def display_items(self):
        for item_id, details in self.inventory.items():
            item = details['item']
            quantity = details['quantity']
            print(f"ID: {item_id}, Name: {item.name}, Price: {item.price}, Quantity: {quantity}")


class PaymentGateway:
    def process_payment(self, amount: float):
        print(f"Processing payment of amount: {amount}")
        return True
    
class CashPaymentGateway(PaymentGateway):
    def process_payment(self, amount: float):
        print(f"Processing cash payment of amount: {amount}")
        return True

class CardPaymentGateway(PaymentGateway):
    def process_payment(self, amount: float):
        print(f"Processing card payment of amount: {amount}")
        return True

class VMSystem:
    def __init__(self):
        self.vending_machine = VendingMachine()

    def add_item(self, quantity: int, id: int, name: str, price: float):
        item = Item(id, name, price, quantity)
        self.vending_machine.add_item(quantity, item)

    def _vend_item(self, item_id: int):
        return self.vending_machine.vend_item(item_id)

    def display_items(self):
        self.vending_machine.display_items()

    def get_item(self, item_id: int):
        if item_id not in self.vending_machine.inventory:
            raise ValueError("Item not found")
        return self.vending_machine.inventory[item_id]['item']

    def take_order(self, item_id: int, payment_method: str):
        item = self.get_item(item_id)
        print(f"Please pay price: {item.price} for item: {item.name}")

        if payment_method == "cash":
            payment_gateway = CashPaymentGateway()
        elif payment_method == "card":
            payment_gateway = CardPaymentGateway()
        else:
            print("Invalid payment method.")
            return

        if self._make_payment(item.price, payment_gateway):
            print(f"Payment successful. Dispensing item: {item.name}")
            item = self._vend_item(item_id)
            return item
        else:
            print("Payment failed. Please try again.")

    def _make_payment(self, amount: float, payment_gateway: PaymentGateway):
        payment_gateway.process_payment(amount)
        self.vending_machine.balance += amount

        return True

    
