# STIDE

## What exactly is STIDE?
**S**equence **Ti**me **D**elay **E**mbedding describes an an algorithm for anomaly detection in data sets. 

The core idea in our implementation of **STIDE** is to first create a database of "normal" behaviour of a program using it's trace of *system calls*. 
Using [*strace*](https://en.wikipedia.org/wiki/Strace), we trace the system calls made by a certain process and insert them into an [*SQLite*](https://www.sqlite.org/index.html) database. 
Afterwards, and thats where the actual STIDE happens, traces are obtained during runtime and kept in windows of a certain predefined size. 
These windows are then slidden over the dataset of normal behaviour. If no match is found an **anomaly** is detected and reported as such. 
For debugging and monitoring purposes, these anomalies are stored in a [*InfluxDB*](https://www.influxdata.com/)

## How is STIDE implemented?
The actual STIDE algorithm is implemented in `stide.py.` 
The mechanisms to obtain the traces and refine them for more efficient use are implemented in `syscall_tracer.py` and `stide_syscall_formatter.py.`
The actual reporting mechanisms and storage in the corresponding InfluxDB are implemented in `influx_adapter.py`

## Things to note
As the author of the described code I suspect that it might be highly inefficient. 
I am always open for constructive criticism and will accept beneficial changes to the code after reviewing and testing them.

## References
<sup>1</sup> Stephanie Forrest, Steven A. Hofmeyr, Anil Somayaji, and Thomas A. Longstaff. A sense of self for Unix processes. In SP’96: Proceedings of the 1996 IEEE Symposium on Security and Privacy, page 120, Washington, DC, USA, 1996. IEEE Computer Society.

<sup>2</sup> Stephanie Forrest, Steven Hofmeyr, and Anil Somayaji. Computer immunology. Communications of the ACM, 40(10):88–96, October 1997.

<sup>3</sup> Steven A. Hofmeyr, Stephanie Forrest, and Anil Somayaji. Intrusion detection using sequences of system calls. Journal of Computer Security, 6(3), 1998

<sup>4</sup> Inoue Hajime and Anil Somayaji. Lookahead pairs and full sequences: a tale of two anomaly detection methods. Proceedings of the 2nd Annual Symposium on Information Assurance. 2007.

<sup>5</sup> SAP, AG. Standardized Technical Architecture Modeling: Conceptual and Design Level. Version 1.0. http://www.fmc-modeling.org/download/fmc-and-tam/SAP-TAM_Standard.pdf [accessed 10 April 2019], 2007