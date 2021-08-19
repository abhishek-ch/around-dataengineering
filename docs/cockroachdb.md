# CockroachDB: Deep Dive

![image](https://user-images.githubusercontent.com/7579608/130077031-a4b55f01-aa90-408f-8c6c-38d3a96816db.png)


CockroachDB is a geo-distributed Replicated, Transaction Key-value Store Database
- Offer consistency, even on massively scaled deployments. No eventual consistency issues and stale reads.
- Create an always-on database that accepts reads and writes on all nodes without generating conflicts.
- Support familiar tools for working with relational data (i.e., SQL).
- MVCC, uses a hybrid logical clock scheme for KV versioning. Values are never overwritten but written with a new version! (Better Concurrency, similar to HBase, BigTable etc).

## Ranges
- Data is stored as ranges
- range-partitioning on the keys to divide the data into contiguous ordered chunks of size ~64 MiB, that is stored across the cluster
- Ranges are ~64 MiB because it is a size small enough to allow Ranges to quickly move between nodes but large enough to store a contiguous set of data likely to be accessed together
- Ranges start empty, grow, split when they get too large, and merge when they get too small. Ranges also split based on the load to reduce hotspots and imbalances in CPU usage


Data is placed in range using order-preserving data distribution. This is designed for better SQL performance. Range Scan is heavily efficient due to this design choice.
Within a Range, keys are ordered in Physical Machine using a per node embedded KV store using RocksDB
> Range Indexing Structure (similar B-Tree) is designed to maintain ordering between ranges.

## Replica
Replication is done in the level of Ranges not Nodes
Each Range is a part of Raft (distributed consensus) Group. Required for replication.
Every single range runs its draft consensus protocol to keep its portion of the keyspace in sync across multiple replicas
Raft provides Atomic Replication
Range-level leases, where a single replica in the Raft group acts as the leaseholder. It is the only replica allowed to serve authoritative up-to-date reads or propose writes to the Raft group leader.
To ensure that only one replica holds a lease at a time, lease acquisitions piggyback on Raft; replicas attempting to acquire a lease do so by committing a special lease acquisition log entry

### Reads without Consensus
 Because all writes go through the leaseholder, reads can bypass networking round trips required by Raft without sacrificing consistency.
One replica is chosen as the leader. A leader always aware of the latest committed write.

## Replica Placement
4 Principles ie Space, Diversity, Load & Latency

### Diversity
Diversity improves Availability when there is replicas are spread across failure domains (disk, node, rack, datacenter, region).
CRDB replicates data across many failure domains possible 

### Load
- Leaseholder needs special attention due to write and read. There's actually an imbalance between leaseholder and follower replicas. The leaseholder, by performing all the coordination for writes and performing all the reads, has significantly higher network traffic, as well as CPU usage than the follower replicas. 
- Ranges are not created equal and some ranges can have much higher load than other.

CockroachDB notices this, it measures per range load, and by measuring that per range load, it can spread ranges and spread the load across the cluster. In this case, the blue range ends up on nodes by itself

### Geo-Distributed database
 Over short distances, geographic latencies can be tens of milliseconds and over longer distances, they can be hundreds of milliseconds. CRDB considers this during replica placement. It wants to place data so that it's close to where the users are and move data around where it's close to being accessed.

Approaches are Manual, where the user may decide on keeping the replica range or leaseholder in a particular locality.
Another is Automatic (Adapt to changes), where the Database tries to place the leaseholders & replicas close to where they are being accessed, follow the workload.


## Transactions
Cockroach DB transactions can span the entire keyspace, touching data residents across a distributed cluster while providing ACID guarantees.
Transactions in CockroachDB are serializable. 
Transactions in CockroachDB can span arbitrary ranges. The full set of operations for the transaction is not required upfront (Conversational).

Transactions provide a unit of atomicity using Raft
- Raft provides atomic writes to individual ranges
- Bootstrap transaction atomicity using Raft
- Every Transaction has a Transaction Record(KV). Transaction record atomically flipped from PENDING to COMMIT
- Technically it follows Consensus for writing and replicating new records. It used RAFT and needs a Quorum of replicas to write a record. It supports full isolation, until a key is COMMITTED, it's not available to read.
- 
> Pipelined Transaction is a new generation


## SQL Data Mapping
CockroachDB SQL is full SQL, uses PostgreSQL dialect, and also implements the PostgreSQL SQL wire protocol.

How do cockroach DB store typed and columnar data in a distributed, replicated, transactional key-value store? 
• The SQL data model needs to be mapped to KV data 
• Reminder: keys and values are lexicographically sorted
- Inside Cockroach DB, every table has a primary key
- Non index columns are encoded into the value
- Each row in the primary key maps directly to a single KV pair
- Key is encoded as a string which is same like an integer
- Key is not just a single element but encoded with table , index id

## SQL Execution
TODO

## References
* https://dl.acm.org/doi/pdf/10.1145/3318464.3386134
* https://www.youtube.com/watch?v=OJySfiMKXLs&list=PLFvZ-npsoTPLSmk3dze42oRe8kC-sjEfl
* https://www.infoq.com/presentations/cockroachdb-distributed-sql
