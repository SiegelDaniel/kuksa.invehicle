
  

# Running on AGL with agl-kuksa

In this Quick Start Guide we will monitor the HomeScreen process of Automotive Grade Linux (AGL).

  

## Building the Image

App-IDS is part of the Kuksa Layer for yocto. Following the instructions for [agl-kuksa](https://github.com/eclipse/kuksa.invehicle/tree/master/agl-kuksa  "agl-kuksa") results in an AGL image for Raspberry Pi 3 that encompasses the App-IDS modules and systemd service units to start and stop the modules.

  

## Filling the database

Configuration of App-IDS is done via a central configuration file. You can ssh to your Raspberry and update the configuration file using, e.g., ```vi```

  

```

vi /usr/bin/app-ids/src/config.json

```

  

To monitor the HomeScreen your ```config.json``` should contain the following part:

```

{

"stide": {

"DB_USER": "",

"DB_PW": "",

"DB_HOST": "../Traces.sqlite",

"BROKER_IP": "localhost",

"STORAGE_MODE": "True",

"WINDOW_SIZE": 3

},

"syscall_tracer": {

"BROKER_IP": "localhost",

"PID": ,

"PNAMES": ["HomeScreen"],

"QOS": 1

},

"stide_syscall_formatter": {

"BROKER_IP": "localhost"

},

"influx_adapter": {

"BROKER_IP": "localhost",

"INFLUX_HOST": "",

"INFLUX_PORT": "",

"INFLUX_MSRMNT": ""

}

}

```

In comparison to the sample `config.json` we defined HomeScreen as the name of the process we want to monitor. The remaining relevant fields for this quick start guide are:

-  `WINDOW_SIZE` is the size of the system call windows used by STIDE

-  `DB_HOST` is the location of the sqlite database file

-  `BROKER_IP` the ip of the mqtt broker. As the image is build with mosquitto, localhost works just fine here.

**Note that this mechanism also works when the traced application is ran from within docker when a few prerequisites are met**

-  `STORAGE_MODE`

-  `True` indicates that we want to fill the database with system call sequences representing benign behavior

-  `False` indicates that we want to compare monitored systems calls with the database to find anomalies

  

To start filling up your database simply start the **stide** service using:

```

systemctl start stide

```

This also starts the **__systemcall_tracer__** and **__stide_syscall_formatter__** modules. Correspondingly, you can use

```

systemctl stop stide

```

These services are located in ```/lib/systemd/system ```.  

to stop the services and finish filling your database.

  In order to use BoSC, you will also need to train the BoSC module. 
  The BoSC module will need a Lookup-Table to work properly. 
  For further information on that, please refer to the BoSC wiki page.

To start filling up your BoSC database you can use  
```

systemctl start BoSC

```
after you have configured BoSC to start in learning mode.
This will start the BoSC service and all of it's dependencies.



## Detecting anomalies

Detected anomalies are published on the `ANOMALY` mqtt topic. So, it is a good idea to subscribe to this topic on your **local machine**. The simplest way to do this is using the ```mosquitto-clients``` package. After you installed the package you can simply subscribe with:

```

mosquitto_sub -h <ip_of_your_raspberry> -t "ANOMALY"

```

  

Now, we have to configure the **stide** module to detect anomalies. Thus, `config.json` should look as follows:

```

{

"stide": {

"DB_USER": "",

"DB_PW": "",

"DB_HOST": "../Traces.sqlite",

"BROKER_IP": "localhost",

"STORAGE_MODE": "True",

"WINDOW_SIZE": 3

},

"syscall_tracer": {

"BROKER_IP": "localhost",

"PID": 1,

"PNAMES": ["HomeScreen"],

"QOS": 1

},

"stide_syscall_formatter": {

"BROKER_IP": "localhost"

},

"influx_adapter": {

"BROKER_IP": "localhost",

"INFLUX_HOST": "",

"INFLUX_PORT": "",

"INFLUX_MSRMNT": ""

}

}

```
If you want to use the BoSC approach too, please configure it accordingly. 
Instructions on how to that are provided on the BoSC wiki page.
  

Then, restart the service:

```

systemctl start stide

```
If you are using the BoSC approach, remember to restart it too:
```

systemctl start BoSC

```

If you already filled your database extensively, meaning it covers the benign behavior to a large extend, you will obviously not see any anomalies, unless somebody starts tampering with the process. However, for testing purposes you can simply try to only fill the database for a short time or even use an empty one.
