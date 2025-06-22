from xapp_interface.decorators.xApp import xApp
from xapp_interface.Xapp import Xapp
from xapp_interface.XappController import XappController
from xapp_interface.enums import *

@xApp(name="ByeWorld")
class ByeWorld(Xapp):
    node_id = 11
    time_interval = 1
    # read_measurements = [MeasurementsHandler.ALL_MEASUREMENTS]
    # read_measurements = [MeasurementsHandler.CQI]
    read_measurements = ["ue_cqi", "ue_dl_brate_kbps", "ue_ul_mcs"]
    send_commands = []
    cell_ids = [0]

    @classmethod
    def process(cls, measurements):
        if measurements:
            print(measurements)

# @xApp(name="HelloWorld")
# class HelloWorld(Xapp):
#     node_id = 1
#     time_interval = 2 # Define the time_interval for the xApp to run in a loop
#     read_measurements = [MeasurementsHandler.CQI] #measurements of interest (all defined in MeasurementsHandler)
#     # read_measurements = [MeasurementsHandler.CQI, MeasurementsHandler.MAC_DL_MCS, MeasurementsHandler.MAC_DL_BRATE] #measurements of interest (all defined in MeasurementsHandler)
#     send_commands = [] # list of tuples where the first element is the CommandHandler and the second the payload
#     cell_ids = [0]

#     @classmethod
#     def process(cls, measurements):
#         print("hello world processing")
#         if measurements:
#             print("HelloWorld")
#             print(measurements)
#         # gain = 1000
#         # cls.add_command(tuple((CommandHandler.CELL_GAIN, gain)))

#         # policy = [0, 0.1523, 0.2344, 0.3770, 0.6016, 0.1523, 0.2344, 0.3770, 0.6016, 0.1523, 0.2344, 0.3770, 0.6016, 0.3770, 0.6016, 0.6016]
#         # cls.add_command(tuple((CommandHandler.CQI_TO_MCS, policy)))

XappController().run()
