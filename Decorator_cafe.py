class Beverage:
    def __init__(self, name, cost):
        self.name = name
        self._cost = cost

    def cost(self):
        return self._cost

    def get_description(self):
        return self.name


class AddOnDecorator(Beverage):
    def __init__(self, addon_name, addon_cost):
        super().__init__(addon_name, addon_cost)
        self.beverage = None

    def __call__(self, beverage):
        self.beverage = beverage
        return self

    def cost(self):
        if not self.beverage:
            raise ValueError("No beverage attached yet")
        return self.beverage.cost() + self._cost

    def get_description(self):
        if not self.beverage:
            raise ValueError("No beverage attached yet")
        return self.beverage.get_description() + ", " + self.name


# Base drink
espresso = Beverage('Espresso', 2)

# Add-ons
milk = AddOnDecorator("Milk", 0.5)

# Apply decorator
ord1 = milk(espresso)

print(ord1.get_description())  # Espresso, Milk
print(ord1.cost())              # 2.5