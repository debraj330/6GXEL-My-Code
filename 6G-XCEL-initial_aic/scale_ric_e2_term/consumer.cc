#include "consumer.h"
#include <string>
#include <iostream>



namespace scale_ric{

    Consumer::Consumer(std::string ip_address){
        context = zmq_ctx_new();
        socket = zmq_socket(context, ZMQ_SUB);
        ip_port = "tcp://";
        ip_port += ip_address;
        ip_port += ":5557";
        int rc = zmq_connect(socket, ip_port.c_str());
        zmq_setsockopt(socket, ZMQ_LINGER,"",0);
        zmq_setsockopt(socket, ZMQ_SUBSCRIBE,"",0);
        zmq_setsockopt(socket, ZMQ_CONFLATE,"",1);
    }

    void Consumer::receive_command(){
        char buffer[1000];
        zmq_recv(socket, buffer, 1000, 0);
        std::cout << buffer << "\n";
    }

    Consumer::~Consumer(){
        zmq_close(socket);
        zmq_ctx_destroy(context);
    }


    void Consumer::receive_scheduler_policy(float *arr, int arr_len){
        char buffer[1000];
        zmq_recv(socket, buffer, 1000, 0);
        std::cout << buffer << "\n";
        parse_json_array((const char *)buffer, arr, arr_len);
    }


    void Consumer::parse_json_array(const char *m_json, float *value_arr, int arr_len){
        int count_brackets = 0;
        bool end_flag = false;
        char c;
        float value;
        int val_i = 0;
        while((c=*m_json++) != '\0'){
            if (end_flag) break;
            if (c == '{'){
                count_brackets++;
                continue;
            }
            if (count_brackets == 2){
                char c_i[100];
                char c_ii;
                int i = 0;
                while ((c_ii=*m_json++) != ','){
                    if (c_ii == '}') {
                        end_flag = true;
                        break;
                    }
                    c_i[i++] = c_ii;
                }
                c_i[i++] = '\0';
                value_arr[val_i++] = std::atof(c_i);
            }
        }
        for (int i=0; i<16; i++){
            fprintf(stderr,"value_arr[%d]=%f\n",i,value_arr[i]);
        }

        //arr = value_arr;
    }


} // namespace scale_ric
