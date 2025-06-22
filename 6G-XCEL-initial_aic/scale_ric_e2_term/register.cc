// to compile g++ zmq_broker.cpp -o th_zmq_broker -lzmq -pthread
// g++ databus.cc parse_config.cc -o databus -lzmq -pthread
#include "parse_config.h"
#include <map>
#include <sstream>
#include <string>
#include <thread>
#include <zmq.h>

std::string msg;

std::map<std::string, std::string> read_json(std::string inputString) {
  std::map<std::string, std::string> dataMap;

  std::istringstream inputStream(inputString.substr(1, inputString.length()));

  // Parse the input stream and extract key-value pairs
  std::string token;
  while (getline(inputStream, token, ',')) {
    // Split the token into key and value
    std::string key, value;
    size_t delimiterPos = token.find(':');
    if (delimiterPos != std::string::npos) {
      key = token.substr(0, delimiterPos);
      value = token.substr(delimiterPos + 1);

      // Remove whitespace and {} from key and value
      key.erase(std::remove_if(key.begin(), key.end(), isspace), key.end());
      value.erase(std::remove_if(value.begin(), value.end(), isspace),
                  value.end());
      key.erase(std::remove_if(key.begin(), key.end(),
                               [](char c) { return c == '{'; }),
                key.end());
      key.erase(std::remove_if(key.begin(), key.end(),
                               [](char c) { return c == '}'; }),
                key.end());
      key.erase(std::remove_if(key.begin(), key.end(),
                               [](char c) { return c == '"'; }),
                key.end());
      value.erase(std::remove_if(value.begin(), value.end(),
                                 [](char c) { return c == '{'; }),
                  value.end());
      value.erase(std::remove_if(value.begin(), value.end(),
                                 [](char c) { return c == '}'; }),
                  value.end());
      value.erase(std::remove_if(value.begin(), value.end(),
                                 [](char c) { return c == '"'; }),
                  value.end());

      // Handle different data types for values
      // if (value.find('[') != std::string::npos &&
      //    value.find(']') != std::string::npos) {
      //  // Value is an array
      //  // Extract individual array elements
      //  std::string arrayString = value.substr(1, value.length() - 2);
      //  std::istringstream iS(arrayString);
      //  std::vector<int> arrayElements;
      //  std::cout << arrayString;
      //  while (getline(iS, token, ',')) {
      //    arrayElements.push_back(std::stoi(token));
      //  }

      //  std::cout << "Mesa mesic";
      //  // Convert array elements to a string representation
      //  std::stringstream arrayStream;
      //  for (int element : arrayElements) {
      //    std::cout << element;
      //    arrayStream << element << ',';
      //  }
      //  arrayStream.seekp(-1, std::ios::end);
      //  value = arrayStream.str();
      //} else if (value.find("\"") == std::string::npos) {
      //  // Value is an integer
      //  // value = std::to_string(std::stoi(value));
      //  // std::cout << value;
      //}

      // Insert the key-value pair into the map
      dataMap[key] = std::string(value);
    }
  }

  // Print the parsed data
  // for (const auto &[key, value] : dataMap) {
  //  std::cout << key << ": " << value << std::endl;
  //}

  return dataMap;
}

void send_msg_to_topic(void *socket) {
  if (!msg.empty()) {
    const char *buffer = msg.c_str();
    zmq_send(socket, buffer, msg.length(), 0);
    // Producer::msg = "";
    msg.clear();
  }
}

void add_key_value_to_msg(std::string key_t, std::string value_t) {
  if (msg.empty()) {
    msg = "{";
    msg += "\"" + key_t + "\": " + "\"" + value_t + "\"";
    msg += "}";
  } else {
    msg = msg.substr(0, msg.size() - 1);
    msg += ", \"" + key_t + "\": " + "\"" + value_t + "\"";
    msg += "}";
  }
}

void add_key_array_to_msg(std::string key_t, std::string value_array) {
  if (msg.empty()) {
    msg = "{";
    msg += "\"" + key_t + "\": " + value_array;
    msg += "}";
  } else {
    msg = msg.substr(0, msg.size() - 1);
    msg += ", \"" + key_t + "\": " + value_array;
    msg += "}";
  }
}

std::map<std::string, std::string> receive_command(void *socket) {
  char buffer[1000];
  zmq_recv(socket, buffer, 1000, 0);
  std::cout << buffer << "\n";
  std::map<std::string, std::string> msg_recv = read_json(buffer);
  return msg_recv;
}

int main() {
  std::map<std::string, std::string> config = read_config("databus.conf");

  std::string ip_address = config["registration_ip_address"];

  std::string recv_measurements_port = config["recv_measurements"];
  std::string pub_measurements_port = config["pub_measurements"];

  void *context;
  void *socket;
  std::string ip_port;
  context = zmq_ctx_new();
  socket = zmq_socket(context, ZMQ_REQ);
  ip_port = "tcp://";
  ip_port += ip_address;
  ip_port += ":5558";
  std::cout << "Conencting to ip address: " << ip_port;
  int rc = zmq_connect(socket, ip_port.c_str());

  // Send request
  add_key_value_to_msg("node_type", "e2");
  add_key_value_to_msg("node_id", "10");
  add_key_value_to_msg("msg_type", "register");
  std::cout << msg;

  send_msg_to_topic(socket);
  std::cout << "New msg: " << msg;

  receive_command(socket);

  // send information about the available measurements
  add_key_value_to_msg("node_type", "e2");
  add_key_value_to_msg("node_id", "10");
  add_key_value_to_msg("msg_type", "pm_availability");
  // add_key_value_to_msg("available_pms", "[\"cqi\",\"rsrp\"]");
  add_key_array_to_msg("available_pms", "[\"cqi\",\"rsrp\"]");
  std::cout << msg;

  send_msg_to_topic(socket);
  std::cout << "New msg: " << msg;

  auto recv_msg = receive_command(socket);

  for (const auto &[key, value] : recv_msg) {
    std::cout << key << ": " << value << std::endl;
  }

  if (std::string(recv_msg["msg_type"]) == "err_msg") {
    std::cout << recv_msg["msg_content"];
  } else {
    std::cout << "Received msg: " << std::string(recv_msg["databus_ip"]) << ":"
              << std::string(recv_msg["send_pm_port"]) << "\n\n\n";
  }
  //
  //
  //
  //
  //
  //
  //  std::string request = "Hello";

  // zmq_send(socket, buffer, msg.length(), 0);
  // rc.send(zmq::message_t(request.begin(), request.end()));
  // std::cout << "Sent request: " << request << std::endl;

  //// Receive reply
  // zmq::message_t reply;
  // socket.recv(reply);
  // std::cout << "Received reply: " << std::string(reply.begin(),
  // reply.end())
  //           << std::endl;

  return 0;
}
