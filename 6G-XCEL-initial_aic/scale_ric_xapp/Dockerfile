FROM ubuntu:focal as base

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt install -y \
     python3.9 \
     python3.9-dev \
     python3-pip \
     build-essential \
     cmake libfftw3-dev \
     libmbedtls-dev \
     libboost-program-options-dev \
     libconfig++-dev \
     libsctp-dev \
     curl \
     iputils-ping \
     iproute2 \
     iptables \
     unzip \
     git \
     libtool 

RUN rm -rf /var/lib/apt/lists/*


WORKDIR /zmq

RUN git clone https://github.com/zeromq/libzmq.git ./
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
RUN ldconfig


WORKDIR /czmq
RUN git clone https://github.com/zeromq/czmq.git ./
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
RUN ldconfig

RUN pip install pyzmq
RUN pip install tensorflow
RUN pip install Flask
RUN pip install streamlit
RUN pip install requests
#RUN pip install pandas
#RUN pip install numpy

WORKDIR /scale_ric_xapp
#ADD xapp_interface ./xapp_interface
##COPY xApp.py ./
#COPY xApp.conf ./
#COPY xApp_hello_world.py ./


#to run it run the following command:
# sudo docker build -t container-test .
# sudo docker run -p 172.16.25.20:5554:5554 -p 172.16.25.20:5555:5555 -p 172.16.25.20:5556:5556 -p 172.16.25.20:5557:5557 container-test ./databus`
