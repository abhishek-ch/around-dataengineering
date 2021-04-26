## Real-time Data Infrastructure @ Uber

![image](https://user-images.githubusercontent.com/7579608/116062917-a8092e80-a684-11eb-9855-54874defc35c.png)


3 fundamentals #realtime processing needs
* Messaging platform that allows communication between asynchronous producers and subscribers 
* Stream processing that allows applying computational logic on top of such streams of messages
* OnLine Analytical Processing (OLAP) that enables analytical queries over all this data in near real time.

## Data Dilema
real-time workflow involving multi-stage ML based stream processing pipelines which favors freshness
& availability over data consistency. On the other hand, monitoring realtime business metrics around orders and sales requires a SQL like interface used by data scientists with more emphasis given to data completeness.

_Open source software adoption has many advantages such as the development velocity, cost effectiveness as well as the power of the crowd!_

The minimum requirements from OLAP includes at least once semantics while ingesting data from the different sources. Exactly once data ingestion based on a primary key is a must have for a small set of critical use cases.

## Work
Most of the streams are incrementally archived in batch processing systems and ingested in the data warehouse. This is then made available for machine learning and other data science use cases.

## Core Requirements
Consistency, Availability ( a dynamic pricing won’t survive without), Data Freshness, Query Latency, Scalability, Cost, Flexibility


![image](https://user-images.githubusercontent.com/7579608/116063122-e1419e80-a684-11eb-9697-f9266ecf3f7f.png)


## System 

__Apache Kafka__
* Federated cluster setup
* Dead letter queue is a separate queue to manage message failures, which shouldn’t block live traffic 
* Consumer proxy, ( Kafka includes a consumer library which packages sophisticated logic of batching and compression)proxy layer that consumes messages from Kafka and dispatches them to a user-registered gRPC service endpoint for all the pub/sub use cases. The complexities of the consumer library are encapsulated in the proxy layer, and applications only need to adopt a very thin, machine-generated gRPC client. In particular, the consumer proxy provides sophisticated error handling
* Cross Cluster replication

__Apache Flink__

### Why?
Robust, easier to scale & large OSS presence. Memory footprint is way less than Spark
* Streaming analytical applications with SQL, ability to transform an input Apache Calcite SQL query into an efficient Flink Job.(Internally, it converts the input SQL query into a logical plan, runs it through the query optimizer and creates a physical plan which can be translated into a Flink job using the corresponding Flink API)

__Apache Pinot__

_Pinot employs the lambda architecture to present a federated view between real-time and historical (offline) data._

## Comparison with pinot:
ElasticSearch: Higher memory with poor query latency compared to pinot
Apache Druid: Pinot is similar in architecture to Apache Druid but has incorporated optimized data structures such as bit compressed forward indices, for lowering the data footprint. Starter indices is excellent

* Apache Pinot is the only open-source real-time OLAP store that supports upsert. The key technical challenge for upsert is tracking the locations of the records with the same primary key. To overcome this challenge, we organize the input stream into multiple partitions by the primary key, and distribute each partition to a node for processing. As a result, all the records with the same primary key are assigned to the same node. A new routing strategy that dispatches subqueries over the segments of the same partition to the same node to ensure the integrity of the query result. Together they lead to a shared-nothing solution to this problem in Pinot.
* Full SQL Support by integration Presto with Pinot









