#include "producer.h"
#include <string>
#include <iostream>

namespace scale_ric {

Producer::Producer(std::string ip_address) {
    msg = "";
	context = zmq_ctx_new();
	socket = zmq_socket(context, ZMQ_PUSH);
    ip_port = "tcp://";
    ip_port += ip_address;
    ip_port += ":5555";
	int rc = zmq_connect(socket, ip_port.c_str());
}

void Producer::send_msg_to_topic() {
    if (!Producer::msg.empty()){
        const char* buffer = msg.c_str();
        zmq_send(socket, buffer, msg.length(), 0);
        // Producer::msg = "";
        Producer::msg.clear();
    }
}

void Producer::add_key_value_to_msg(std::string key_t, std::string value_t){
    if (Producer::msg.empty()){
        Producer::msg = "0;{";
        Producer::msg += "\"" + key_t + "\": " + value_t;
        Producer::msg += "}";
    } else{
        Producer::msg = Producer::msg.substr(0, Producer::msg.size()-1);
        Producer::msg += ", \"" + key_t + "\": " + value_t;
        Producer::msg += "}";
    }
}

// void Producer::flush() { rd_kafka_flush(rk, 15 * 1000); }

Producer::~Producer() {
	zmq_close (socket);
	zmq_ctx_destroy(context);
}

}
