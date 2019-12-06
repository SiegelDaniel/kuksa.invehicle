# Testing and demonstrating
In order to test the IDS we need to build a test docker image and trace it using the IDS. We dockerized the attack in order to be sure to get the exact same traces everytime no matter what host system or hardware we are on.


# Prerequisites

 1. `sudo usermod -aG docker $USER` 
 2. `{"experimental" : true}` in `/etc/docker/daemon.json`
 3. `sudo -servicedocker restart` (or reboot) 
 4. `sudo apt install qemu-user-static`
 
Afterwards reboot to be safe.
Now we can try to build the docker image:

 1. Navigate to app-ids/test/src 
 2. Execute: `cp /usr/bin/qemu-arm-static qemu-arm-static`
 3. Reboot to be safe
 4. `docker build --platform linux/arm32v6 -f Dockerfile -t Test .`
 5. Make sure you did not forget the dot in line 4.


