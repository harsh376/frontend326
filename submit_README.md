PUBLIC IP: 52.5.94.6:8080 (Server runs on Port 8080)
PUBLIC DNS: http://ec2-52-5-94-6.compute-1.amazonaws.com:8080/

Enabled Google APIs: 

Benchmark Setup:

Performance Benchmarking:
We benchmarked our server using the Apache Benchmarking Tool ab.

To Install ab on Ubuntu / Linux, run the following in command line:
	sudo apt-get install apache2-utils

The command to run a benchmark against our server is as follows:
	ab -k -n #{num_requests} -c #{num_connections} http://52.5.94.6:8080/?keywords=hello+hi

	-n: Number of requests to provide the server
	-c: Number of connections to the server
	-k: Keep alive flag

The above command connects 'num_connections' instances simultaneously and proceeds to make 'num_requests' number of mistakes

System Monitoring:
In order to monitor the system utilization of our server, we used 2 tools, namely dstat and pidstat.

If you are running our server on another instance on ec2, please make sure the following commands are executed:
	sudo apt-get install sysstat dstat pidstat

However, before monitoring our server for system usage, we have to ensure it is being run and maximum capacity.
To do so, run the following command first
	python benchmark_server.py

 This will run the Apache Benchmark 10 times in a loop and thereby, will provide a replication of a server being run at maximum capacity at steady state.

To Monitor our server for CPU Usage, Disk IO and Memory Utilization, run the following 'on the instance'
	pidstat -p $PID_OF_SERVER -d -r -u -l 1 
	-p: PID of server
	-d:	Memory Utilization
	-r: Disk Performance
	-u: CPU Usage
	-l: Full Path of command
	1: Provide input after every 1 second

To Monitor for Network usage, run the following,
	dstat
	This will provide you with all the statistics of above + network statistics for the whole system

