# Attack demonstrator
This test is used for demonstration purposes, it consists of a **dockerizable** attack application, a **configuration** and a **training set of STIDE and BoSC** data.

## Preparations

### Preparing the machine to build the docker container on 

1. Install a fresh *Ubuntu 18.04* on your machine or VM. 
2. Execute `sudo usermod -a -G docker $USER`
3. put `{"experimental" : true}` into **/etc/docker/daemon.json**
4. `sudo service docker restart` (_or reboot_)
5. Execute `sudo apt install qemu-user-static`
6. Execute `cp /usr/bin/qemu-arm-static qemu-arm-static`
### Actually building the image 
In the folder of this README, execute:
`build --platform linux/arm32v6 -f docker/Dockerfile -t attack .`
### Extracting the image 
Use `docker save -o attack.tar attack` to store the container in a tar file.
### Deploying the image 
On your target Raspberry Pi 3 with AGL running, use:
`docker load -i attack.tar` 

## Running the image 
Start the docker container using
`docker run -it --network host -t attack /bin/ash`
then execute `python attack.py` in the container's shell.

## Running the attack
After you've started the IDS and configured it to watch the process in the docker container, use a [MQTT Publisher](https://mosquitto.org/man/mosquitto_pub-1.html) to publish a arbitrary message on the **"ATTACK"** topic of the correspondingly configured **MQTT** broker. 
You will notice that the `attack.py` starts to write a lot of files, generating a lot of file I/O and *therefore changing it's behaviour.* 

The IDS now should notice the anomaly.
