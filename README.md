# hadoop-app
Setting up the Hadoop Docker and accessing Hadoop Distributed File System using CLI and Python apps

![Hadoop](https://hadoop.apache.org/hadoop-logo.jpg)
![Docker](https://avatars.githubusercontent.com/u/5429470?s=200&v=4)

### Install Docker
Download Docker Desktop for your OS. https://www.docker.com/

### Setup Hadoop pseudo distributed mode dockerized
```bash
$ git clone https://github.com/jmwarfe/docker-hadoop-spark
$ cd docker-hadoop-spark
```
For Windows: Change the docker-compose.yml line 15 to "2022:22". This will avoid weird port out of range errors
### Spin up dockerized Hadoop containers
```bash
$ docker-compose up -d
```
After successful run of hadoop docker containers, following urls should be accessible
1. NameNode information can be accessed at http://localhost:9870
2. Secondary NameNode information can be accessed at http://localhost:9868
3. DataNode information can be accessed at http://localhost:9864
4. The hadoop cluster can be accessed at http://localhost:8088/cluster
5. The NodeManager can be accessed at http://localhost:8042/node


Connect and access Hadoop Docker containers: 
```bash
docker exec -it <container_id> bash
```
#### Create data_files directory in the docker container
#### Copy the *.txt files from /data directory (in this repo) into the data 
```bash
docker cp input1.txt <container_id>:/data_files
docker cp input2.txt <container_id>:/data_files
docker cp input3.txt <container_id>:/data_files
```

### Within docker container bash
- Create user "hduser" in the group "hadoop"
- Create directory /user/hduser/data
- Copy the files [ input1.txt Download input1.txt, input2.txt] to /user/hduser/data on HDFS.
- Access the contents of /user/hduser/data directory on HDFS using read-from-hadoop.py

### Hadoop Streaming utility & MRJob class
#### Run the mapper and reducer python programs to read text from input*.txt files 
```bash
root@hadoop:/code# $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /user/hduser/input1.txt -output /user/hduser/output1

root@hadoop:/code# $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /user/hduser/input2.txt -output /user/hduser/output2

root@hadoop:/code# $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py -input /user/hduser/input3.txt -output /user/hduser/output3
```
#### Display the contents of the output generated
```bash
root@hadoop:/code# hdfs dfs -head /user/hduser/output1/part-00000
root@hadoop:/code# hdfs dfs -head /user/hduser/output2/part-00000
root@hadoop:/code# hdfs dfs -head /user/hduser/output3/part-00000
```
### Run MRWordCount program on a Hadoop cluster
```bash
root@hadoop:/code# $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -files MRWordCount.py -input /user/hduser/data/input1.txt -output /user/hduser/output4

root@hadoop:/code# $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -files MRWordCount.py -input /user/hduser/data/input2.txt -output /user/hduser/output5

root@hadoop:/code# $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -files MRWordCount.py -input /user/hduser/data/input3.txt -output /user/hduser/output6
```
### Generate the output
 ```bash
root@hadoop:/code# hdfs dfs -head /user/hduser/output4/part-00000
root@hadoop:/code# hdfs dfs -head /user/hduser/output5/part-00000
root@hadoop:/code# hdfs dfs -head /user/hduser/output6/part-00000
```

#### Find info about The CSV file provides information about top 10 popular products and the total sales 
```bash
root@hadoop:/code# python3 MRWordCount.py hdfs://localhost:9000/user/hduser/data/ord -r hadoop
```
