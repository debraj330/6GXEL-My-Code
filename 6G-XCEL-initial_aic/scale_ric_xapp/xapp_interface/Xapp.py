from .managers.XappManager import XappManager


class Xapp:
    time_interval = 1 # default time interval for the xApp to run the code is 1s
    read_measurements = []
    send_commands = [] # list of tuples where the first element is the CommandHandler and the second the payload
    cell_ids = []

    @classmethod
    def add_command(cls, command):
        cls.send_commands.append(command)

    @classmethod
    def process(cls, measurements):
        pass
