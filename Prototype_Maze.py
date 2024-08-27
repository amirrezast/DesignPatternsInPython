from copy import deepcopy


class Maze:
    def clone(self):
        return deepcopy(self)


class Wall:
    def clone(self):
        return deepcopy(self)


class Room:
    def __init__(self, room_id):
        self.room_id = room_id

    def clone(self):
        return deepcopy(self)


class Door:
    def __init__(self, room1=None, room2=None):
        self.room1 = room1
        self.room2 = room2

    def initialize(self, room1, room2):
        self.room1 = room1
        self.room2 = room2

    def clone(self):
        return deepcopy(self)


class MazePrototypeFactory:
    def __init__(self, maze_prototype, wall_prototype, room_prototype, door_prototype):
        self._prototypeMaze = maze_prototype
        self._prototypeWall = wall_prototype
        self._prototypeRoom = room_prototype
        self._prototypeDoor = door_prototype

    def make_maze(self):
        return self._prototypeMaze.clone()

    def make_wall(self):
        return self._prototypeWall.clone()

    def make_room(self, room_id):
        room = self._prototypeRoom.clone()
        room.room_id = room_id
        return room

    def make_door(self, room1, room2):
        door = self._prototypeDoor.clone()
        door.initialize(room1, room2)
        return door


# Create prototypes
maze_prototype = Maze()
wall_prototype = Wall()
room_prototype = Room(room_id=1)
door_prototype = Door()

# Create a factory with these prototypes
factory = MazePrototypeFactory(maze_prototype, wall_prototype, room_prototype, door_prototype)

# Create a maze with the factory
maze = factory.make_maze()
room1 = factory.make_room(1)
room2 = factory.make_room(2)
door = factory.make_door(room1, room2)


class BombedWall(Wall):
    def __init__(self, has_bomb=False):
        self._bomb = has_bomb

    def clone(self):
        return deepcopy(self)


class RoomWithABomb(Room):
    def __init__(self, room_id, has_bomb=False):
        super().__init__(room_id)
        self._bomb = has_bomb


class PrototypeManager:
    def __init__(self):
        self._prototypes = {}

    def register_prototype(self, key, prototype):
        self._prototypes[key] = prototype

    def unregister_prototype(self, key):
        if key in self._prototypes:
            del self._prototypes[key]

    def get_prototype(self, key):
        return self._prototypes.get(key)


if __name__ == "__main__":
    # Create initial prototypes
    maze_prototype = Maze()
    wall_prototype = Wall()
    room_prototype = Room(room_id=1)
    door_prototype = Door()

    # Create a prototype manager and register the prototypes
    prototype_manager = PrototypeManager()
    prototype_manager.register_prototype("simple_maze", maze_prototype)
    prototype_manager.register_prototype("simple_wall", wall_prototype)
    prototype_manager.register_prototype("simple_room", room_prototype)
    prototype_manager.register_prototype("simple_door", door_prototype)

    # Retrieve prototypes from the manager
    maze_factory = MazePrototypeFactory(
        prototype_manager.get_prototype("simple_maze"),
        prototype_manager.get_prototype("simple_wall"),
        prototype_manager.get_prototype("simple_room"),
        prototype_manager.get_prototype("simple_door")
    )

    # Use the factory to create a maze
    maze = maze_factory.make_maze()
    room1 = maze_factory.make_room(1)
    room2 = maze_factory.make_room(2)
    door = maze_factory.make_door(room1, room2)

    # Print out the created objects
    print(f"Created maze: {maze}")
    print(f"Created room1: {room1.room_id}")
    print(f"Created room2: {room2.room_id}")
    print(f"Created door between rooms: {door.room1.room_id} and {door.room2.room_id}")

