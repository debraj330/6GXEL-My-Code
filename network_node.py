import zmq
import threading
import configparser

def expose_measurements(ip_address, recv_measurements_port, pub_measurements_port):
    print("Measurements exposure broker started")

    context = zmq.Context()

    # PULL from base stations
    sub_BS = context.socket(zmq.PULL)
    sub_BS.bind(f"tcp://{ip_address}:{recv_measurements_port}")

    # PUB to xApps
    pub_xapps = context.socket(zmq.PUB)
    pub_xapps.bind(f"tcp://{ip_address}:{pub_measurements_port}")

    zmq.proxy(sub_BS, pub_xapps)


def expose_commands(ip_address, recv_commands_port, pub_commands_port):
    print("Commands exposure broker started")

    context = zmq.Context()

    # PULL from xApps
    sub_xapps = context.socket(zmq.PULL)
    sub_xapps.bind(f"tcp://{ip_address}:{recv_commands_port}")

    # PUB to base stations
    pub_BS = context.socket(zmq.PUB)
    pub_BS.bind(f"tcp://{ip_address}:{pub_commands_port}")

    zmq.proxy(sub_xapps, pub_BS)


def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    # Assume config is under a section called 'broker'
    cfg = config['broker']
    return {
        'ip_address': cfg.get('ip_address'),
        'recv_measurements': cfg.get('recv_measurements'),
        'pub_measurements': cfg.get('pub_measurements'),
        'recv_commands': cfg.get('recv_commands'),
        'pub_commands': cfg.get('pub_commands'),
    }


if __name__ == "__main__":
    config = read_config("node_msg_broker.conf")

    ip_address = config['ip_address']
    recv_measurements_port = config['recv_measurements']
    pub_measurements_port = config['pub_measurements']
    recv_commands_port = config['recv_commands']
    pub_commands_port = config['pub_commands']

    # Start threads
    th_measurements = threading.Thread(
        target=expose_measurements,
        args=(ip_address, recv_measurements_port, pub_measurements_port),
        daemon=True
    )

    th_commands = threading.Thread(
        target=expose_commands,
        args=(ip_address, recv_commands_port, pub_commands_port),
        daemon=True
    )

    th_measurements.start()
    th_commands.start()

    th_measurements.join()
    th_commands.join()
