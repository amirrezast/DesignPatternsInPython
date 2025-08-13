from abc import ABC, abstractmethod


# Receiver
class Lamp:
    def __init__(self):
        self.is_on = False
        self.intensity = 50  # P

    def turn_on(self):
        self.is_on = True
        print('Lamp is ON.')

    def turn_off(self):
        self.is_on = False
        print('Lamp is OFF.')

    def dim_down(self):
        if self.intensity <= 10:
            self.is_on = False
        else:
            self.intensity -= 10

    def dim_up(self):
        if not self.is_on:
            self.is_on = True
        elif self.intensity == 100:
            pass
        else:
            self.intensity += 10

    def __repr__(self):
        return f"Lamp(is_on={self.is_on}, intensity={self.intensity})"


# Command Interface
class ICommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class TurnOnCommand(ICommand):
    def __init__(self, lamp: Lamp):
        self.lamp = lamp

    def execute(self):
        self.lamp.turn_on()

    def undo(self):
        self.lamp.turn_off()


class TurnOffCommand(ICommand):
    def __init__(self, lamp: Lamp):
        self.lamp = lamp

    def execute(self):
        self.lamp.turn_off()

    def undo(self):
        self.lamp.turn_on()


class DimUpCommand(ICommand):
    def __init__(self, lamp: Lamp):
        self.lamp = lamp

    def execute(self):
        self.lamp.dim_up()
    def undo(self):
        self.lamp.dim_down()


class DimDownCommand(ICommand):
    def __init__(self, lamp: Lamp):
        self.lamp = lamp

    def execute(self):
        self.lamp.dim_down()
    def undo(self):
        self.lamp.dim_up()




class CommandHistory:
    def __init__(self):
        self.history = []
    def push(self, command):
        self.history.append(command)
    def pop(self):
        if self.history:
            return self.history.pop()
        return None

    def __repr__(self):
        command_names = [cmd.__class__.__name__ for cmd in self.history]
        return f"CommandHistory(commands={command_names})"


# Invoker
class RemoteControl:
    def __init__(self, history: CommandHistory):
        self.history = history

    def execute_command(self, command: ICommand):
        command.execute()
        self.history.push(command)

    def undo_last(self):
        last_command = self.history.pop()
        if last_command:
            last_command.undo()
        else:
            print("No commands to undo.")




class LampCommandFactory:
    def __init__(self, lamp):
        self.lamp = lamp
    def create_up_command(self):
        return DimUpCommand(self.lamp)
    def create_down_command(self):
        return DimDownCommand(self.lamp)
    def create_on_command(self):
        return TurnOnCommand(self.lamp)
    def create_off_command(self):
        return TurnOffCommand(self.lamp)

    def create_all_commands(self):
        return {
            'on': self.create_on_command(),
            'off': self.create_off_command(),
            'down': self.create_down_command(),
            'up': self.create_up_command()
        }


lamp_1 = Lamp()
lamp_2 = Lamp()

lamp_1_commands_factory = LampCommandFactory(lamp_1)
lamp_1_commands = lamp_1_commands_factory.create_all_commands()
on1, off1, down1, up1 = lamp_1_commands['on'], lamp_1_commands['off'],lamp_1_commands['down'], lamp_1_commands['up']


history_1 = CommandHistory()
remote_1 = RemoteControl(history_1)
remote_1.execute_command(on1)
remote_1.execute_command(up1)
print(lamp_1)
remote_1.execute_command(up1)
print(lamp_1)
remote_1.execute_command(off1)
remote_1.execute_command(off1)
remote_1.undo_last()
remote_1.undo_last()
remote_1.undo_last()
remote_1.undo_last()

print(lamp_1)

print(history_1)


