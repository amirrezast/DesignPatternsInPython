import os
from abc import ABC, abstractmethod
from enum import Enum

class Direction(Enum):
    North = 1
    South = 2
    East = 3
    West = 4


class MapSite(ABC):
    @abstractmethod
    def enter(self):
        pass

# Concrete classes for rooms
class Room(MapSite):
    def __init__(self, room_no):
        self.room_number = room_no
        self._sides = [None] * 4

    def get_side(self, direction: Direction):
        return self._sides[direction.value - 1]

    def set_side(self, direction: Direction, map_site: MapSite):
        self._sides[direction.value - 1] = map_site

    def enter(self):
        print(f"Entering room number {self.room_number}")

class EnchantedRoom(Room):
    def __init__(self, room_no, spell):
        super().__init__(room_no)
        self.spell = spell

    def enter(self):
        print(f"Entering enchanted room number {self.room_number} with spell {self.spell}")

class RoomWithABomb(Room):
    def __init__(self, room_no):
        super().__init__(room_no)
        self.has_bomb = True
        self.bomb_exploded = False

    def enter(self):
        if self.has_bomb and not self.bomb_exploded:
            print(f"Entering room number {self.room_number} with a bomb!")
        elif self.bomb_exploded:
            print(f"Entering room number {self.room_number}.\n!!!The bomb has exploded!!!")
        else:
            print(f"Entering room number {self.room_number}")

    def explode_bomb(self):
        if self.has_bomb and not self.bomb_exploded:
            self.bomb_exploded = True
            print(f"The bomb in room number {self.room_number} has exploded!")

# Concrete classes for walls
class Wall(MapSite):
    def enter(self):
        print("You hit a wall.")

class BombedWall(Wall):
    def __init__(self):
        self.is_damaged = False

    def enter(self):
        if self.is_damaged:
            print("You hit a damaged wall.")
        else:
            print("You hit a wall.")

    def damage(self):
        self.is_damaged = True
        print("The wall is now damaged.")

# Concrete classes for doors
class Door(MapSite):
    def __init__(self, room_1=None, room_2=None):
        self.room_1 = room_1
        self.room_2 = room_2
        self.is_open = False

    def enter(self):
        if self.is_open:
            print("You pass through the door")
        else:
            print("The door is closed.")

    def other_side_from(self, room):
        if room == self.room_1:
            return self.room_2
        elif room == self.room_2:
            return self.room_1
        return None

class DoorNeedingSpell(Door):
    def enter(self):
        if self.is_open:
            print("You pass through the enchanted door.")
        else:
            print("The enchanted door is closed.")

# Maze and factory classes
class Maze:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.room_number] = room

    def room_no(self, room_number):
        return self.rooms.get(room_number, None)

class MazeFactory:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            maze_style = os.getenv("MAZESTYLE", "default")
            if maze_style == "bombed":
                cls._instance = BombedMazeFactory()
            elif maze_style == "enchanted":
                cls._instance = EnchantedMazeFactory()
            else:
                cls._instance = MazeFactory()
        return cls._instance

    def make_maze(self):
        return Maze()

    def make_wall(self):
        return Wall()

    def make_room(self, n):
        return Room(n)

    def make_door(self, r1, r2):
        return Door(r1, r2)

class EnchantedMazeFactory(MazeFactory):
    def make_room(self, n):
        return EnchantedRoom(n, self.cast_spell())

    def make_door(self, r1, r2):
        return DoorNeedingSpell(r1, r2)

    def cast_spell(self, spell="A mysterious spell"):
        return spell

class BombedMazeFactory(MazeFactory):
    def make_room(self, n):
        return RoomWithABomb(n)

    def make_wall(self):
        return BombedWall()

# Maze game that uses the factory
class MazeGame:
    def create_maze(self):
        factory = MazeFactory.instance()
        a_maze = factory.make_maze()
        r1 = factory.make_room(1)
        r2 = factory.make_room(2)
        a_door = factory.make_door(r1, r2)

        a_maze.add_room(r1)
        a_maze.add_room(r2)

        r1.set_side(Direction.North, factory.make_wall())
        r1.set_side(Direction.East, a_door)
        r1.set_side(Direction.South, factory.make_wall())
        r1.set_side(Direction.West, factory.make_wall())

        r2.set_side(Direction.North, factory.make_wall())
        r2.set_side(Direction.East, factory.make_wall())
        r2.set_side(Direction.South, factory.make_wall())
        r2.set_side(Direction.West, a_door)

        return a_maze

# Example usage
if __name__ == "__main__":
    maze_game = MazeGame()
    os.environ["MAZESTYLE"] = "enchanted"
    maze = maze_game.create_maze()
    room1 = maze.room_no(1)
    room2 = maze.room_no(2)

    room1.enter()
    door = room1.get_side(Direction.East)
    if isinstance(door, Door):
        door.enter()
        next_room = door.other_side_from(room1)
        next_room.enter()
