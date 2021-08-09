# Zippy DB

ZippyDB is the largest strongly consistent, geographically distributed key-value store at Facebook
DIstributed key-value store is designed by combining a replication library called Data Shuttle with the storage engine, RocksDB and layering this on top of  Shard Manager and distributed configuration service (built on ZooKeeper), that together solves load balancing, shard placement, failure detection, and service discovery.

Data Shuttle uses Multi-Paxos to synchronously replicate data to all replicas in the global scope.

## Architecture
- ZippyDB is deployed in tiers which consists of compute and storage resources spread across several geographic areas, making it resilient to failures.
- Each tier hosts multiple use cases, usually hosted on widlcard tier which has better utilization of hardware and lower operational overhead
- Shards are basic unit of data management, data splits in a use case on a tier

## How replication work?
Each shard is replicated using Data Shuttle, which uses either Paxos or async replication to replicate data.
 
Within a shard, a subset of replicas are configured to be a part of the Paxos quorum group,  where data is synchronously replicated using Multi-Paxos to provide high durability and availability in case of failures. The remaining replicas, if any, are configured as followers

Followers allow application to have low latency read with relaxed consistency! 
Applications can provide 'hints' for assigning replicas in a region.

## Data Model
-Supports iterating over key prefixes and deleting a range of keys
- For ephemeral data, ZippyDB has native TTL support , adding expiry time for an object at the time of the write.
- Relies on RocksDB’s periodic compaction support to clean up all the expired keys efficiently while filtering out dead keys on the read side in between compaction runs. 
- ShardManager is responsible for monitoring servers for load imbalance, failures, and initiating shard movement between servers. 
- Shard can be partitioned their key space into smaller units of related data known as μshards 
- A physical shard can host several tens of thousands of μshards. This additional layer of abstraction allows ZippyDB to reshard the data transparently without any changes on the client.

## Shards Mapping
- Compact mapping is used when the assignment is fairly static and mapping is only changed when there is a need to split shards that have become too large or hot. 
- Akkio Mapping splits use cases’ key space into μshards and places these μshards in regions where the information is typically accessed. Akkio helps reduce data set duplication and provides a significantly more efficient solution for low latency access than having to place data in every region.

## Epoch & Quoram
Time is subdivided into units known as epochs. Each epoch has a unique leader, whose role is assigned using a ShardManager. Once a leader is assigned, it has a lease for the entire duration of the epoch. Periodic heartbeats used to keep a lease active until ShardManager bumps up the epoch on the shard . When a failure occurs, ShardManager detects the failure, assigns a new leader with a higher epoch and restores write availability.

 Within each epoch, the leader generates a total ordering of all writes to the shard, by assigning each write a monotonically increasing sequence number. The writes are then written to a replicated durable log using Multi-Paxos to achieve consensus on the ordering. Once the writes have reached consensus, they are drained in-order across all replicas.

## Write Consistency
A write involves persisting the data on a majority of replicas’ Paxos logs and writing the data to RocksDB on the primary before acknowledging the write to the client.
A read on primary will always see the most recent write

## Read Consistency

-  ZippyDB provides total ordering for all writes within a shard and ensures that reads aren’t served by replicas that are lagging behind primary/quorum beyond a certain configurable threshold, so eventual reads supported by ZippyDB are closer to bounded staleness consistency in literature.
-  For read-your-writes, the clients cache the latest sequence number returned by the server for writes and use the version to run at-or-later queries while reading. The cache of versions is within the same client process.
-  Linearizability implemented by routing the reads to the primary in order to avoid the need to speak to a quorum, mostly for performance reasonss.

## Transactions
All transactions are serializable by default on a shard, and we don’t support lower isolation levels.
Transactions use optimistic concurrency control to detect and resolve conflicts

Conditional write is implemented using “server-side transactions
”. 

## Reference
https://engineering.fb.com/2021/08/06/core-data/zippydb/
