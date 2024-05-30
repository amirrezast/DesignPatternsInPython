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

    def __repr__(self):
        return  f"Room number {self.room_number}"


class EnchantedRoom(Room):
    def __init__(self, room_no, spell):
        super().__init__(room_no)
        self.spell = spell
        print(f"EnchantedRoom {self.room_number} is created with spell '{self.spell}'")

    def enter(self):
        print(f"Entering enchanted room number {self.room_number} with spell {self.spell}")

    def __repr__(self):
        return  f"EnchantedRoom number {self.room_number}"


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
            print(f"entering room number {self.room_number}")

    def explode_bomb(self):
        if self.has_bomb and not self.bomb_exploded:
            self.bomb_exploded = True
            print(f"The bomb in room number {self.room_number} has exploded!")


class Wall(MapSite):
    def __init__(self):
        print("Wall is created.")

    def enter(self):
        print("You hit a wall.")


class BombedWall(Wall):
    def __init__(self):
        super().__init__()
        self.is_damaged = False

    def enter(self):
        if self.is_damaged:
            print("You hit a damaged wall.")
        else:
            print("You hit a wall.")

    def damage(self):
        self.is_damaged = True
        print("The wall is now damaged.")


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


class Maze:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.room_number] = room

    def room_no(self, room_number):
        return self.rooms.get(room_number, None)

    def __repr__(self):
        room_descriptions = [f"{key}: {value}" for key, value in self.rooms.items()]
        return "\n".join(room_descriptions)


class MazeBuilder(ABC):
    def __init__(self):
        self._currentMaze = None  # Initialize _maze in the base class

    @abstractmethod
    def build_maze(self):
        pass

    @abstractmethod
    def build_room(self, room_no):
        pass

    @abstractmethod
    def build_door(self, room_from, room_to):
        pass

    def get_maze(self):
        return self._currentMaze


class SimpleMazeBuilder(MazeBuilder):
    def __init__(self):
        super().__init__()

    def build_maze(self):
        self._currentMaze = Maze()

    def build_room(self, room_no):
        if self._currentMaze.room_no(room_no) is None:
            room = Room(room_no)
            self._currentMaze.add_room(room)
            room.set_side(Direction.North, Wall())
            room.set_side(Direction.South, Wall())
            room.set_side(Direction.East, Wall())
            room.set_side(Direction.West, Wall())

    def build_door(self, room_from, room_to):
        r1 = self._currentMaze.room_no(room_from)
        r2 = self._currentMaze.room_no(room_to)
        if r1 is not None and r2 is not None:
            door = Door(r1, r2)
            r1.set_side(self.common_wall(r1, r2), door)
            r2.set_side(self.common_wall(r2, r1), door)

    def common_wall(self, room1, room2):
        # Logic to determine the common wall direction
        # Assuming a grid layout with rooms being adjacent either horizontally or vertically
        if room1.room_number < room2.room_number:
            return Direction.East if room2.room_number - room1.room_number == 1 else Direction.South
        else:
            return Direction.West if room1.room_number - room2.room_number == 1 else Direction.North

    def get_maze(self) -> Maze:
        return self._currentMaze


class EnchantedMazeBuilder(SimpleMazeBuilder):
    def __init__(self):
        super().__init__()

    def build_room(self, room_no):
        if self._currentMaze.room_no(room_no) is None:
            room = EnchantedRoom(room_no, self.cast_spell())
            self._currentMaze.add_room(room)
            room.set_side(Direction.North, Wall())
            room.set_side(Direction.South, Wall())
            room.set_side(Direction.East, Wall())
            room.set_side(Direction.West, Wall())

    def build_door(self, room_from, room_to):
        r1 = self._currentMaze.room_no(room_from)
        r2 = self._currentMaze.room_no(room_to)
        if r1 is not None and r2 is not None:
            door = DoorNeedingSpell(r1, r2)
            r1.set_side(self.common_wall(r1, r2), door)
            r2.set_side(self.common_wall(r2, r1), door)

    def cast_spell(self, spell="A mysterious spell"):
        return spell


class BombedMazeBuilder(SimpleMazeBuilder):
    def __init__(self):
        super().__init__()

    def build_room(self, room_no):
        if self._currentMaze.room_no(room_no) is None:
            room = RoomWithABomb(room_no)
            self._currentMaze.add_room(room)
            room.set_side(Direction.North, BombedWall())
            room.set_side(Direction.South, BombedWall())
            room.set_side(Direction.East, BombedWall())
            room.set_side(Direction.West, BombedWall())


class CountingMazeBuilder(MazeBuilder):
    def __init__(self):
        super().__init__()
        self._rooms = 0
        self._doors = 0

    def build_maze(self):
        self._currentMaze = Maze()

    def build_room(self, room_no):
        self._rooms += 1

    def build_door(self, room_from, room_to):
        self._doors += 1

    def get_counts(self):
        return self._rooms, self._doors


class MazeGame:
    def create_maze(self, builder: MazeBuilder):
        builder.build_maze()
        builder.build_room(1)
        builder.build_room(2)
        builder.build_door(builder._currentMaze.room_no(1), builder._currentMaze.room_no(2))
        return builder.get_maze()

    def create_complex_maze(self, builder: MazeBuilder, n=1001):
        builder.build_maze()
        for i in range(1, n+1):
            builder.build_room(i)
        builder.build_door(1, 2)
        # Add more complex connections and rooms
        return builder.get_maze()


# Example usage
if __name__ == "__main__":
    maze_game = MazeGame()

    print("\nCreating a simple maze:")
    simple_builder = SimpleMazeBuilder()
    simple_maze = maze_game.create_maze(simple_builder)
    simple_room1 = simple_maze.room_no(1)
    simple_room2 = simple_maze.room_no(2)

    simple_room1.enter()
    simple_door = simple_room1.get_side(Direction.East)
    if isinstance(simple_door, Door):
        simple_door.enter()
        next_room = simple_door.other_side_from(simple_room1)
        next_room.enter()

    print("\nCreating an enchanted maze:")
    enchanted_builder = EnchantedMazeBuilder()
    enchanted_maze = maze_game.create_maze(enchanted_builder)
    enchanted_room1 = enchanted_maze.room_no(1)
    enchanted_room2 = enchanted_maze.room_no(2)

    enchanted_room1.enter()
    enchanted_door = enchanted_room1.get_side(Direction.East)
    if isinstance(enchanted_door, DoorNeedingSpell):
        enchanted_door.enter()
        enchanted_next_room = enchanted_door.other_side_from(enchanted_room1)
        enchanted_next_room.enter()

    print("\nCreating a bombed maze:")
    bombed_builder = BombedMazeBuilder()
    bombed_maze = maze_game.create_maze(bombed_builder)
    bombed_room1 = bombed_maze.room_no(1)
    bombed_room2 = bombed_maze.room_no(2)

    bombed_room1.enter()
    bombed_door = bombed_room1.get_side(Direction.East)
    if isinstance(bombed_door, Door):
        bombed_door.enter()
        bombed_next_room = bombed_door.other_side_from(bombed_room1)
        bombed_next_room.enter()

    bombed_room1.explode_bomb()
    bombed_room1.enter()
    bombed_room1_wall = bombed_room1.get_side(Direction.North)
    if isinstance(bombed_room1_wall, BombedWall):
        bombed_room1_wall.damage()
        bombed_room1_wall.enter()

    print("\nCreating a complex maze:")
    complex_builder = BombedMazeBuilder()
    complex_maze = maze_game.create_complex_maze(complex_builder, 5)
    complex_room1 = complex_maze.room_no(1)
    complex_room5 = complex_maze.room_no(5)

    complex_room1.enter()
    complex_room5.enter()
