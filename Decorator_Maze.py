class Beverage:
    def __init__(self, name, cost):
        self.name = name
        self._cost = cost

    def cost(self):
        raise NotImplementedError
    def get_description(self):
        raise NotImplementedError


class AddOnDecorator(Beverage):
    def __init__(self, beverage):
        self.beverage = beverage

    def cost(self):
        raise NotImplementedError

    def get_description(self):
        raise NotImplementedError



class Espresso(Beverage):
    def __init__(self):
        super().__init__("Espresso", 1)
    def cost(self):
        return self.cost()
    def get_description(self):
        return self.name



class Milk(AddOnDecorator):
    def __init__(self, beverage):
        super().__init__(beverage)


