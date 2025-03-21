class StateVariable:
    def get_value(self):
        return "StateVariable value"

class ConstraintVariable:
    def get_value(self):
        return "ConstraintVariable value"

class ConstraintStateVariable(StateVariable, ConstraintVariable):
    def get_value(self):
        return f"Adapted: {super().get_value()}"

csv = ConstraintStateVariable()
print(csv.get_value())  # Output depends on method resolution order (MRO)



class OldLogger:
    def log_message(self, msg):
        print(f"[Old Logger] {msg}")

class NewLogger:
    def write_log(self, msg):
        print(f"[New Logger] {msg}")



class LoggerAdapter(OldLogger, NewLogger):
    def log_message(self, msg):
        super().log_message(msg)  # Call OldLogger method

    def write_log(self, msg):
        super().write_log(msg)  # Call NewLogger method



# Create an instance of LoggerAdapter
logger = LoggerAdapter()

# Using the OldLogger interface
logger.log_message("Logging via OldLogger interface")

# Using the NewLogger interface
logger.write_log("Logging via NewLogger interface")
