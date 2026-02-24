from core_entities import VendingMachine, Item, VMSystem


def main():
    vm_system = VMSystem()
    vm_system.add_item(quantity=10, id=1, name="Soda", price=10)
    vm_system.add_item(quantity=5, id=2, name="Chips", price=20)
    vm_system.add_item(quantity=20, id=3, name="Candy", price=10)

    print("Welcome to the Vending Machine!")
    while True:
        print("\nAvailable items:")
        vm_system.vending_machine.display_items()
        choice = input("Enter the item ID to purchase (or 'exit' to quit): ")
        if choice.lower() == 'exit':
            break
        try:
            item_id = int(choice)

            payment_method = input("Enter payment method (cash/card): ").lower()
            vm_system.take_order(item_id, payment_method=payment_method)
        except Exception as e:
            print(f"Error: {e}")
        

if __name__ == "__main__":
    main()