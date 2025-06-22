#ifndef SCALER_RIC_PRODUCER_H
#define SCALER_RIC_PRODUCER_H


#include <zmq.h>
#include <string>

namespace scale_ric {

class Producer{
    private:
    	void *context;
        void* socket;
        std::string ip_port;
        std::string msg;

       public:
        Producer(std::string);
        virtual ~Producer();
        void send_msg_to_topic();
        void add_key_value_to_msg(std::string, std::string);
};

} // namespace scale_ric
#endif // SCALER_RIC_PRODUCER_H
