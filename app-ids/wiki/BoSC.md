# BoSC

## What exactly is BoSC
**B**ags **o**f **S**ystem **C**alls is a technique used for anomaly detection with system calls as reference data. 

The core idea is to count the occurence of each type of System Call in a certain interval or window, capture these windows in a database of benign behaviour and then compare real-time data to the benign behaviour in order to identify anomalies.

A typical Bag of System Calls looks like this: {13,4,8,10,3} where each number represents how often a certain System Call occured in the training period. 
In order to know which number a type of System Call belongs to, we need to establish a lookup-table first.

## How is BoSC implemented?
BoSC requires a bit more preparation than STIDE in order to run flawlessly.
It features the module `create_LUT.py` which is ran during a training period with guaranteed non-anomalous behaviour to create the needed LookUp-Table as described in the section above.

The module implemented in `BoSC.py` itself features a **learning mode** which can be run *after* a LookUp-Table is created. 

During detection mode, which is enabled by setting the configuration key **"LEARNING_MODE"** to **False**, Bags of System Calls are constructed from the stream of system calls delivered via MQTT by the `stide_syscall_formatter.py`. These bags are then checked against the *SQLite* database of benign behaviour. 

If no match is found, an anomaly is reported using similar mechanisms to those used in **`STIDE.py`**

## Things to note
As the author of the described code I suspect that it might be highly inefficient. 
I am always open for constructive criticism and will accept beneficial changes to the code after reviewing and testing them.

## References
<sup>1</sup> https://arxiv.org/pdf/1611.03053.pdf
