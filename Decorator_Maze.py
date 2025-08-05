class Beverage:
    def __init__(self, name, cost):
        self.name = name
        self._cost = cost

    def cost(self):
        print("You must implement cost() in subclass.")
    def get_description(self):
        raise Not


class AddOnDecorator(Beverage):
    def __init__(self, beverage):
        self.beverage = beverage

    def cost(self):
        pass

class Espresso(Beverage):
    def cost(self):
        return 1

class Milk(AddOnDecorator):
    def cost(self):
        return self.beverage.cost() + 2