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


class EnchantedRoom(Room):
    def __init__(self, room_no, spell="ahura"):
        super().__init__(room_no)
        self.spell = spell
        print(f"EnchantedRoom {self.room_number} is created with spell '{self.spell}'")

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


class MazeFactory:
    def __init__(self):
        self.partCatalog = {}

    def add_part(self, part_class, name):
        self.partCatalog[name] = part_class

    def make(self, part_name, *args, **kwargs):
        part_class = self.partCatalog.get(part_name)
        if part_class:
            return part_class(*args, **kwargs)
        else:
            raise ValueError(f"Part {part_name} not found in catalog.")

    def make_maze(self):
        return Maze()

    def make_wall(self):
        return self.make("wall")

    def make_room(self, n):
        return self.make('room', n)

    def make_door(self, r1, r2):
        return self.make("door", r1, r2)


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


class MazeGame:
    def create_maze(self, factory: MazeFactory):
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

    def create_maze_factory(self, factory_type=None):
        factory = MazeFactory()
        if factory_type == 'enchanted':
            factory.add_part(EnchantedRoom, 'room')
            factory.add_part(DoorNeedingSpell, 'door')
            factory.add_part(Wall, 'wall')
        elif factory_type == 'bombed':
            factory.add_part(RoomWithABomb, 'room')
            factory.add_part(BombedWall, 'wall')
            factory.add_part(Door, 'door')
        else:
            factory.add_part(Room, 'room')
            factory.add_part(Wall, 'wall')
            factory.add_part(Door, 'door')
        return factory


# Example usage
if __name__ == "__main__":
    maze_game = MazeGame()

    factory = maze_game.create_maze_factory()
    maze = maze_game.create_maze(factory)

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

    enchanted_factory = maze_game.create_maze_factory('enchanted')
    enchanted_maze = maze_game.create_maze(enchanted_factory)

    enchanted_room1 = enchanted_maze.room_no(1)
    enchanted_room2 = enchanted_maze.room_no(2)

    # Entering rooms to demonstrate functionality
    enchanted_room1.enter()
    enchanted_door = enchanted_room1.get_side(Direction.East)
    if isinstance(enchanted_door, DoorNeedingSpell):
        enchanted_door.enter()
        enchanted_next_room = enchanted_door.other_side_from(enchanted_room1)
        enchanted_next_room.enter()

    print("\nCreating an bombed maze:")

    bombed_factory = maze_game.create_maze_factory('bombed')
    bombed_maze = maze_game.create_maze(bombed_factory)

    bombed_room1 = bombed_maze.room_no(1)
    bombed_room2 = bombed_maze.room_no(2)

    # Entering rooms to demonstrate functionality
    bombed_room1.enter()
    bombed_door = bombed_room1.get_side(Direction.East)
    if isinstance(bombed_door, Door):
        bombed_door.enter()
        bombed_next_room = bombed_door.other_side_from(bombed_room1)
        bombed_next_room.enter()

    # Simulating a bomb explosion
    bombed_room1.explode_bomb()
    bombed_room1.enter()
    bombed_room1_wall = bombed_room1.get_side(Direction.North)
    if isinstance(bombed_room1_wall, BombedWall):
        bombed_room1_wall.damage()
        bombed_room1_wall.enter()
