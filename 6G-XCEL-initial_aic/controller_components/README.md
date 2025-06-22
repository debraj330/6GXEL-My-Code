# scale_ric_databus
This repository contains the implementation of the databus for the scale-RIC. In order to run the databus, check the ip address of your local machine:

```shell
ifconfig
```

Once you know the ip address, update the ip address in the docker-compose file, replace the `172.16.25.20` ip address with your own. Once this is done, run the following command:

```shell
docker-compose up &
```

In order to stop the databus, run the following command:

```shell
docker-compose down
```


# Notes
The configuration of the databus can be found in the `databus.conf` file. It allows us to configure the ip address (since the setup is running in a container, we can use `0.0.0.0` and bind the ports to the host ports). The ports that we are exposing can also be changed in the `databus.conf` file. If those ports are changed, the same change has to be applied to the `docker-compose.yml` file.

The figure below shows the connection between the exposed ports.
![Architecture](https://github.com/merimdzaferagic/scale_ric_databus/blob/master/images/databus.png?raw=true)


# Installing Docker and docker-compose
To install Docker and docker-compose use the following shell script:
```shell
#!/bin/bash
apt-get remove docker docker-engine docker.io containerd runc
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y python3-pip
apt-get install -y docker-ce docker-ce-cli containerd.io
apt-cache madison docker-ce

systemctl enable docker.service
systemctl enable containerd.service


#install docker-compose
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
echo "step 3"
chmod +x ~/.docker/cli-plugins/docker-compose
chown $USER /var/run/docker.sock


cp ~/.docker/cli-plugins/docker-compose /usr/local/bin/docker-compose

docker-compose version


systemctl enable docker.service
systemctl enable containerd.service
```