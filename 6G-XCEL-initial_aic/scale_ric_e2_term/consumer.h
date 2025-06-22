#ifndef SCALE_RIC_CONSUMER_H
#define SCALE_RIC_CONSUMER_H

#include <zmq.h>
#include <string>

namespace scale_ric {

class Consumer{
    private:
    	void *context;
        void* socket;
        std::string ip_port;
    public:
        Consumer(std::string);
        void receive_command();
        virtual ~Consumer();
        void parse_json_array(const char *m_json, float *arr, int arr_len);
        // TODO refactor so that only one function is needed to consume message
        void receive_scheduler_policy(float *arr, int arr_len);
};
} // namespace scale_ric
#endif // SCALE_RIC_CONSUMER_H
