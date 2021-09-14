# Building a real-time data streaming application with Apache Kafka

## Project Description

Real-Time Meetup RSPV Data Processing from https://www.meetup.com/. Real-Time Analytics using Apache Kafka, Zookeeper, Py Spark. Analyzing the real time RSVP data of meetup.com to get real-time insights such as trending topics, cities etc. along with other business insights related to Meetups RSVPs. The data processing scripts are developed in Python.

## Technologies Used

* Python 3.6
* Kafka 2.8.0
* Spark 3.1.2
* Pyspark 2.4.8
* Git/GitHub
* kafka-python 2.0.2
* matplotlib 3.4.3  

## Features

List of features ready and TODOs for future development
* What are the current active cities in the US which are scheduling Meetup Events?
* What are the trending topics in US Meetup Events?
* How many Big data Meetup Events events scheduled in each country?

## Getting Started
   
Assuming Kafka, Zookeeper and Spark of appropriate version is installed, the following commands are used to run the application.

> Spark Streaming integeration with kafka 0.10.0.0 and above.

1. Run Zookeeper to maintain Kafka, command to be run from Zookeeper root dir
```
zookeeper/bin/zkServer.sh start zookeeper/conf/zoo.cfg
```

2. Set environment variables
```
JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
```

3. First time only before starting kafka server run in root dir of kafka
```
./gradlew jar -PscalaVersion=2.13.5
```

4. Start Kafka server, aditional servers can be added as per requirement.
```
kafka/bin/kafka-server-start.sh kafka/config/server.properties
```

5. Start Producer.py to start reading data from the meetup stream and store it in '''meetup''' kafka topic.

6. Start Consumer notebook to consume the processed stream from the spark streaming

7. Submit the spark job <spark_file>.py, to read the data into Spark Streaming from Kafka.
> Spark depends on a external package for kafka integeration
```
bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 /home/flash/Desktop/<spark_file.py>
```
8. Start <consumer>.ipynb file to visualize the data.

# License
- This project uses the following license: [MIT License](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt)

# References
- https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10_2.12/3.1.2
- https://stream.meetup.com/2/rsvps
- https://phoenixnap.com/kb/install-apache-zookeeper
- https://hevodata.com/blog/how-to-install-kafka-on-ubuntu/
