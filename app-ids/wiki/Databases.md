# Databases 


## Influx Database
### Uses
The IDS utilizes InfluxDB to save messages on the **"ATTACK"** topic published via MQTT. 
Besides that, InfluxDB is used to store all messages that are received on the
**"REFINED"** topic. 
To see the implementation, refer to lines 49 and upwards in the `influx_adapter.py`. 
The InfluxDB consists, in reference to it's use, of two measurements: `anomalies` and `traces`. 
### Why exactly Influx?
[InfluxDB](https://www.influxdata.com/) has easy to use bindings for [Grafana](https://grafana.com/), which is a software we are using for **virtualization** purposes. 
This eases building demonstrators and the likes *immensely*. 
Besides that, InfluxDB is a **time series database** and therefore allows us to store and access the exact time when a trace or an anomaly occurs. 
If you don't know about InfluxDB and need basic knowledge to maintain or develop this project, please refer to the [InfluxDB key concepts page](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/).

## SQLite 
### Uses
SQLite is used to store the **sliding windows** and **Bags of System Calls** during training of benign / normal behaviour.  If you're unfamiliar with either one of these concepts please refer to their corresponding pages in this wiki.
### Why exactly SQLite?
SQLite is an extremely *lightweight* database. 
We did not need any extended database management system features for this project but a rather small footprint which is why SQLite suits this job perfectly. 
Besides that, SQLite has existing Python bindings and a relatively well documented library ready to use.
### Database schemes
The table for the **Bags of System Calls approach** is called BoSC. 
It is placed in the preconfigured SQLite file. 
The table consists of just one text column called BAGS which is also the primary key. 
We are aware this might not be the best design choice but it seems to be an efficient one. 

The usage of SQLite for our **STIDE** approach is a bit different. 
As there are many window size we could use, it is necessary to create one for each window size. If a table for window size x does not exist yet, it is created. 
The traces are then inserted, where each position represents its own column. This is done by constructing a dynamic query, depending on window size. 
For further reference check `STIDE.py`.
This might not be the most efficient approach, maybe it's even a misuse of SQLite, but it works.
