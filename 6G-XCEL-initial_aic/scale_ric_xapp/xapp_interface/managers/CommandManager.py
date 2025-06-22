from ..enums.CommandHandler import CommandHandler
import json


def set_cell_gain(gain):
    return json.dumps({"cell_gain": gain})

def submit_cqi_to_mcs_policy(policy):
    if type(policy) != list:
        raise RuntimeError("The policy is not a list.")
    if len(policy) != 16:
       raise RuntimeError("CQI to MCS mapping policy needs to be a list of length 16.")
    policy_cmd = {"cqi_to_mcs_policy": policy}
    return json.dumps(policy_cmd)

def default_cmd(cmd_input):
    raise RuntimeError("The chosen command is not supported by the RIC.")

command_dict = {CommandHandler.CELL_GAIN: set_cell_gain,
                CommandHandler.CQI_TO_MCS: submit_cqi_to_mcs_policy}
