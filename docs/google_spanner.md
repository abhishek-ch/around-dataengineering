# Breaking Down Google Spanner

## Top Features
* Lock-Free Distributed Transactions & ACID
* SQL Query Language
* Schematized Table
* Semi-relational Data Model
* Integration of concurrency control, replication & 2-Phase commit


> Distributed Transactions are externally Consistent, Commit order of the transaction is the same as the order in which it actually appears in
which users actually see the transactions wrt Global Clock (True Time)

### Logical & Physical Data Layout

#### Logical Data Layout

![image](https://user-images.githubusercontent.com/7579608/126864956-59bca8d5-9411-4582-9525-55dd449bb9ec.png)


#### Physical

![image](https://user-images.githubusercontent.com/7579608/126864975-beb7d3a2-b6e3-4f0f-bf38-3a008b3c3ca2.png)

_Precomputed One Join makes it easy_

## Data Sharding

![image](https://user-images.githubusercontent.com/7579608/126865018-a7afb75d-d929-45dd-8d16-9bc57d85aa33.png)

* Spanner supports Transaction across Shards & Consistent Snapshot read( range scan) across shards
* Shards are replicated and Data Locality
* Replication based on __Paxos__ (Election Model)
* Long Lived leader is used for Transaction Management
* Each Server holds multiple Tablets, which is an individual replica of a Shard
* Zonemaster is used for Load balancer and runs hot standby for zonemaster. Client never talks directly with zonemaster


## Transaction & Concurrency

_Based on Synchronized Logical Snapshot of databases/shards and have a consistent view across all the clients_

* Based on __Strict 2-Phase Locking__, to guarentee serializability of the writes to the Database. In 2P locking, every data write is attached with _Timestamp_ 

## Global Wall Clock Time - Synchronizing Snapshots

This is designed for 


### Why Read Only Transaction
