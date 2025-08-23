from abc import ABC, abstractmethod

class IQuackBehavior(ABC):
    @abstractmethod
    def quack(self):
        pass


class IFlyBehavior(ABC):
    @abstractmethod
    def fly(self):
        pass


class SimpleQuacking(IQuackBehavior):
    def quack(self):
        print("Quack! Quack!")


class NoQuacking(IQuackBehavior):
    def quack(self):
        print("... ")


class SimpleFlying(IFlyBehavior):
    def fly(self):
        print("Fly High !!!")


class NoFlying(IFlyBehavior):
    def fly(self):
        print("I Can't Fly :(")


class Duck:
    def __init__(self, quack_behavior: IQuackBehavior, fly_behavior: IFlyBehavior, name:str):
        self.quack_behavior = quack_behavior
        self.fly_behavior = fly_behavior
        self.name = name

    def perform_quack(self):
        self.quack_behavior.quack()


    def perform_fly(self):
        self.fly_behavior.fly()

    def display(self):
        print(f"I'm a {self.name} Duck")
        self.perform_quack()
        self.perform_fly()


    def set_quack_behavior(self, quack_behavior: IQuackBehavior):
        self.quack_behavior = quack_behavior
        print(f"bibidi babidi du "
              f"{self.name} quacking now is like:")
        self.perform_quack()


    def set_fly_behavior(self, fly_behavior: IFlyBehavior):
        self.fly_behavior = fly_behavior
        print(f"bibidi babidi du "
              f"{self.name} quacking now is like:")
        self.perform_fly()
        





simple_quack = SimpleQuacking()
simple_fly = SimpleFlying()
no_quack = NoQuacking()
no_fly = NoFlying()

normal_duck = Duck(quack_behavior=simple_quack, fly_behavior=simple_fly, name="Normal")
rubber_duck = Duck(quack_behavior=simple_quack, fly_behavior=no_fly, name="Rubber")

normal_duck.display()
rubber_duck.display()