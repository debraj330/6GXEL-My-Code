from ..managers.XappManager import XappManager


def xApp(name):
    def wrapper(cls):

        # @classmethod
        # def add_command(cls, command):
        #     cls.send_commands.append(command)

        cls.u_name = name
        XappManager.add_xApp(name, cls)
        return cls


    return wrapper
