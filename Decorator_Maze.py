class Beverage:
    def __init__(self, name, cost):
        self.name = name
        self._cost = cost

    def cost(self):
        raise NotImplementedError
    def get_description(self):
        raise NotImplementedError


class AddOnDecorator(Beverage):
    def __init__(self, beverage, addon_name, addon_cost):
        self.beverage = beverage
        self.addon_name = addon_name
        self.addon_cost = addon_cost

    def cost(self):
        return self.beverage.cost() + self.addon_cost

    def get_description(self):
        return self.beverage.get_description() + ", " + self.addon_name




class Espresso(Beverage):
    def __init__(self):
        super().__init__("Espresso", 1)
    def cost(self):
        return self._cost()
    def get_description(self):
        return self.name



class Milk(AddOnDecorator):
    def __init__(self, beverage):
        super().__init__(beverage, "Milk", .5)
        



    def cost(self):
        return self.beverage.cost()

