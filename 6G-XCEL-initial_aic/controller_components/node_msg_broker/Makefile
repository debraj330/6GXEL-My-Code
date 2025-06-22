#g++ zmq_broker.cpp -o th_zmq_broker -lzmq -pthread
CXX= g++
LIBS= -lzmq -pthread

SRC_FILES= node_msg_broker.cc parse_config.cc
OBJ_FILES= node_msg_broker.o parse_config.o

all: $(OBJ_FILES) 
	$(CXX) $(OBJ_FILES) -o node_msg_broker $(LIBS)

%.o : %.cc 
	$(CXX) -c $< -o $@

clean: 
	rm -f $(OBJ_FILES) node_msg_broker
