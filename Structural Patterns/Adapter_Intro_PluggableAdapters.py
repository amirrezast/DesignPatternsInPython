class Directory:
    def __init__(self, name, subdirectories=None):
        self.name = name
        self.subdirectories = subdirectories or []

    def get_subdirectories(self):
        return self.subdirectories

class ClassObject:
    def __init__(self, name, subclasses=None):
        self.name = name
        self.subclasses = subclasses or []

    def get_subclasses(self):
        return self.subclasses

class TreeAdapter:
    def __init__(self, tree_structure, get_children_method):
        self.tree_structure = tree_structure
        self.get_children_method = get_children_method  # Dynamic method mapping

    def get_children(self):
        method = getattr(self.tree_structure, self.get_children_method)
        return method()

# Create directory structure
dir_a = Directory("A", [Directory("B"), Directory("C")])
dir_adapter = TreeAdapter(dir_a, "get_subdirectories")
print([d.name for d in dir_adapter.get_children()])  # Output: ['B', 'C']

# Create class hierarchy
class_a = ClassObject("ClassA", [ClassObject("ClassB"), ClassObject("ClassC")])
class_adapter = TreeAdapter(class_a, "get_subclasses")
print([c.name for c in class_adapter.get_children()], '\n')  # Output: ['ClassB', 'ClassC']




class PayPal:
    def send_money(self, amount):
        print(f"PayPal: Sent ${amount}")

class Stripe:
    def charge_card(self, amount):
        print(f"Stripe: Charged ${amount}")

class Bitcoin:
    def transfer_crypto(self, amount):
        print(f"Bitcoin: Transferred ₿{amount}")



class PaymentAdapter:
    def __init__(self, payment_system, method_name):
        self.payment_system = payment_system
        self.method_name = method_name  # Pass the method name dynamically

    def process_payment(self, amount):
        method = getattr(self.payment_system, self.method_name)
        method(amount)


# Using PayPal
paypal = PaymentAdapter(PayPal(), "send_money")
paypal.process_payment(100)

# Using Stripe
stripe = PaymentAdapter(Stripe(), "charge_card")
stripe.process_payment(200)

# Using Bitcoin
bitcoin = PaymentAdapter(Bitcoin(), "transfer_crypto")
bitcoin.process_payment(0.005)

