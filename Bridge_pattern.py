from abc import ABC, abstractmethod

class Color(ABC):
    @abstractmethod
    def apply_color(self) -> str:
        pass

class Green(Color):
    def apply_color(self) -> str:
        return "Green"

class Red(Color):
    def apply_color(self) -> str:
        return "Red"

class Yellow(Color):
    def apply_color(self) -> str:
        return "Green"


class Shape(ABC):
    def __init__(self, color: Color):
        self.color = color

    @abstractmethod
    def draw(self) -> None:
        pass

class Circle(Shape):
    def draw(self) -> None:
        print(f"Drawing Circle in {self.color.apply_color()}")

class Square(Shape):
    def draw(self) -> None:
        print(f"Drawing Square in {self.color.apply_color()}")


red_square = Square(Red())
red_square.draw()