from enum import Enum
from abc import ABC, abstractmethod


class Direction(Enum):
    North = 1
    South = 2
    East = 3
    West = 4


class MapSite(ABC):
    @abstractmethod
    def enter(self):
        pass


class Maze:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.room_number] = room

    def room_no(self, room_number):
        return self.rooms.get(room_number, None)


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
        print(f"EnchantedRoom {self.room_number} is created with spell '{self.spell}'")

    def enter(self):
        print(f"Entering enchanted room number {self.room_number} with spell {self.spell}")


class Wall(MapSite):
    def __init__(self):
        print("Wall is created.")

    def enter(self):
        print("You hit a wall.")


class Door(MapSite):
    def __init__(self, room_1=None, room_2=None):
        self.room_1 = room_1
        self.room_2 = room_2
        self.is_open = False
        print(f"Door created between Room \
{self.room_1.room_number if self.room_1 else 'None'} and \
Room {self.room_2.room_number if self.room_2 else 'None'}")

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
        else:
            return None


class DoorNeedingSpell(Door):
    def __init__(self, room_1=None, room_2=None):
        super().__init__(room_1, room_2)
        print(f"Door needing a spell created between Room \
        {self.room_1.room_number if self.room_1 else 'None'} and \
        Room {self.room_2.room_number if self.room_2 else 'None'}")

    def enter(self):
        if self.is_open:
            print("You pass through the enchanted door.")
        else:
            print("The enchanted door is closed.")


class MazeGame:
    def create_maze(self):
        a_maze = self.make_maze()
        r1 = self.make_room(1)
        r2 = self.make_room(2)
        the_door = self.make_door(r1, r2)
        a_maze.add_room(r1)
        a_maze.add_room(r2)
        r1.set_side(Direction.North, self.make_wall())
        r1.set_side(Direction.East, the_door)
        r1.set_side(Direction.South, self.make_wall())
        r1.set_side(Direction.West, self.make_wall())
        r2.set_side(Direction.North, self.make_wall())
        r2.set_side(Direction.East, self.make_wall())
        r2.set_side(Direction.South, self.make_wall())
        r2.set_side(Direction.West, the_door)
        return a_maze

    def make_maze(self):
        return Maze()

    def make_room(self, n):
        return Room(n)

    def make_wall(self):
        return Wall()

    def make_door(self, room1, room2):
        return Door(room1, room2)


class BombedWall(Wall):
    pass


class RoomWithABomb(Room):
    pass


class BombedMazeGame(MazeGame):
    def make_wall(self):
        return BombedWall()

    def make_room(self, n):
        return RoomWithABomb(n)


class Spell:
    pass


class EnchantedRoom(Room):
    def __init__(self, room_number, spell):
        super().__init__(room_number)
        self.spell = spell


class DoorNeedingSpell(Door):
    def __init__(self, room_1=None, room_2=None):
        super().__init__(room_1, room_2)
        print(f"Door needing a spell created between Room \
        {self.room_1.room_number if self.room_1 else 'None'} and \
        Room {self.room_2.room_number if self.room_2 else 'None'}")

    def enter(self):
        if self.is_open:
            print("You pass through the enchanted door.")
        else:
            print("The enchanted door is closed.")


class EnchantedMazeGame(MazeGame):
    def make_room(self, n):
        return EnchantedRoom(n, self.cast_spell())

    def make_door(self, room1, room2):
        return DoorNeedingSpell(room1, room2)

    def cast_spell(self):
        return Spell()


if __name__ == "__main__":
    maze_game = MazeGame()

    maze = maze_game.create_maze()

    room1 = maze.room_no(1)
    room2 = maze.room_no(2)

    # Entering rooms to demonstrate functionality
    room1.enter()
    door = room1.get_side(Direction.East)
    if isinstance(door, Door):
        door.enter()
        next_room = door.other_side_from(room1)
        next_room.enter()

    print("\nCreating an enchanted maze:")

    enchanted_game = EnchantedMazeGame()
    enchanted_maze = enchanted_game.create_maze()

    enchanted_room1 = enchanted_maze.room_no(1)
    enchanted_room2 = enchanted_maze.room_no(2)

    # Entering rooms to demonstrate functionality
    enchanted_room1.enter()
    enchanted_door = enchanted_room1.get_side(Direction.East)
    if isinstance(enchanted_door, DoorNeedingSpell):
        enchanted_door.enter()
        enchanted_next_room = enchanted_door.other_side_from(enchanted_room1)
        enchanted_next_room.enter()
