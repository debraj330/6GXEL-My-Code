from xapp_interface.interface import xAppInterface

import sys
import json


xAppInterface = xAppInterface()


#  Do 10 requests, waiting each time for a response
# # reading measurements
# while True:
#     msg = xAppInterface.read_msg()
#     print(msg)

val = 0
# sending commands
while (val != 'q'):
   val = input("Choose scheduling policy (0 or 1), m for metrics and q to quite): ")
   # if(val == '0'):
       # xAppInterface.send_command("{ \"count\": {0, 0.1523, 0.2344, 0.3770, 0.6016, 0.8770, 1.1758, 1.4766, 1.9141, 2.4063, 2.7305, 3.3223, 3.9023, 4.5234, 5.1152, 5.5547} }")
   # msg = {"data": 123}
   if val == '0':
      msg = {"node_type": "xApp", "node_id": 0, "msg_type": "register"}
      xAppInterface.send_command(msg)
      print(xAppInterface.read_msg())
   if val == '1':
      msg = {"node_type": "xApp", "node_id": 0, "msg_type": "pm_ctrl_req", 'e2_node_list': [0], 'list_of_pm': ["cqi"], 'list_of_ctrl': []}
      xAppInterface.send_command(msg)
      print(xAppInterface.read_msg())
   if val == '-1':
      msg = {"node_type": "xApp", "node_id": 0, "msg_type": "pm_ctrl_req", 'e2_node_list': [0], 'list_of_pm': ["cqq"], 'list_of_ctrl': []}
      xAppInterface.send_command(msg)
      print(xAppInterface.read_msg())

   # xAppInterface.send_command(b"Hello world!")
#    elif (val == '1'):
#        #xAppInterface.send_command("{ \"count\": {0, 0.1523, 0.2344, 0.3770, 0.6016, 0.1523, 0.2344, 0.3770, 0.6016, 0.1523, 0.2344, 0.3770, 0.6016, 0.3770, 0.6016, 0.6016} }")
#        xAppInterface.send_command("{ \"count\": {0, 0.1523, 0.1523, 0.1523, 0.1523, 0.2344, 0.2344, 0.2344, 0.2344, 0.2344, 0.2344, 0.2344, 0.2344, 0.2344, 0.2344, 0.2344} }")
#    elif (val == 'm'):
#        msg = xAppInterface.read_msg()
#        print(msg)
#    # 5.1152
