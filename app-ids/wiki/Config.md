# The config.json

As depicted in our architecture overview below, the config.json is the central point to store configuration options for the App-IDS modules. If you want to deploy the modules in a distributed manner, you have to ensure that there a exists a version of config.json on each device/system. More on this can be found under [Known Limitations and Next Steps](Limitations.md).

![App-IDS architecture overview](https://i.imgur.com/rD6V7gP.png)

At the time of our writing, we assume the JSON encoded configuration is straightforward and provide a sample file in the src folder. Further information can be found in our Quick Start Guides ([here](QuickStart_Kuksa.md) and [here](QuickStart_Ubuntu.md)).
