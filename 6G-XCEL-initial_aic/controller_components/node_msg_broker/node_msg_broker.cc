// to compile g++ zmq_broker.cpp -o th_zmq_broker -lzmq -pthread
#include "parse_config.h"
#include <thread>
#include <zmq.h>

void expose_measurements(std::string ip_address,
                         std::string recv_measurements_port,
                         std::string pub_measurements_port) {
  std::cout << "Measurements exposure broker started\n";
  void *context = zmq_ctx_new();
  //  Socket to listen to enbs
  void *sub_BS = zmq_socket(context, ZMQ_PULL);
  std::string sub_socket = "tcp://" + ip_address + ":" + recv_measurements_port;
  zmq_bind(sub_BS, sub_socket.c_str());
  //  Socket to share with xApps
  std::string pub_socket = "tcp://" + ip_address + ":" + pub_measurements_port;
  void *pub_xapps = zmq_socket(context, ZMQ_PUB);
  zmq_bind(pub_xapps, pub_socket.c_str());

  zmq_proxy(sub_BS, pub_xapps, NULL);
}

void expose_commands(std::string ip_address, std::string recv_commands_port,
                     std::string pub_commands_port) {
  std::cout << "Comands exposure broker started\n";
  void *context = zmq_ctx_new();
  //  Socket to listen to xApps
  void *sub_xapps = zmq_socket(context, ZMQ_PULL);
  std::string sub_socket = "tcp://" + ip_address + ":" + recv_commands_port;
  zmq_bind(sub_xapps, sub_socket.c_str());
  //  Socket to share with enbs
  void *pub_BS = zmq_socket(context, ZMQ_PUB);
  std::string pub_socket = "tcp://" + ip_address + ":" + pub_commands_port;
  zmq_bind(pub_BS, pub_socket.c_str());

  zmq_proxy(sub_xapps, pub_BS, NULL);
}

int main() {
  std::map<std::string, std::string> config =
      read_config("node_msg_broker.conf");

  std::string ip_address = config["ip_address"];

  std::string recv_measurements_port = config["recv_measurements"];
  std::string pub_measurements_port = config["pub_measurements"];

  std::string recv_commands_port = config["recv_commands"];
  std::string pub_commands_port = config["pub_commands"];

  std::thread th_expose_measurements(expose_measurements, ip_address,
                                     recv_measurements_port,
                                     pub_measurements_port);
  std::thread th_expose_commands(expose_commands, ip_address,
                                 recv_commands_port, pub_commands_port);

  th_expose_measurements.join();
  th_expose_commands.join();

  return 0;
}
