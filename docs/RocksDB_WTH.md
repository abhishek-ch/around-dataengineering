# RocksDB - Its a World in itself

##### Every database has a storage engine. The storage engine is the low-level data structure that manages the data in the database. 
RocksDB is widely used in database applications where a log-structured merge tree is preferable to a b-tree. These tend to be write-heavy workloads.

- RocksDB is High Performance Key Value store based on Google's Level DB
- It is optimized for the specific characteristics of Solid State Drives (SSDs), targets large-scale (distributed) applications
- It is designed as a library component that is embedded in higher-level applications
- each RocksDB instance manages data on storage devices of just a single server node; 

> It does not handle any inter-host operations, such as replication and load balancing, and it does not perform high-level operations, such as checkpoints

## Usages
• Stream processing: RocksDB is used to store staging data in Apache Flink
* Logging/queuing services: RocksDB is used by Facebook’s LogDevice
* Index services & Stoage Services
* Caching

## Architecture:
In a nutshell, RocksDB is an LSM-tree (Log-Structured Merge tree) key-value storage

RocksDB may be tuned for high write throughput or high read throughput, for space efficiency, or something in between.
Due to its configurability, RocksDB is used by many applications, representing a wide range of use cases

#### Writes 
* Whenever data is written to RocksDB, it is added to an in-memory write buffer called MemTable, as well as an
on-disk Write Ahead Log (WAL). 
* Memtable is implemented as a skiplist so keep the data ordered with O(log n) insert and search overhead
* The WAL is used for recovery after a failure, but is not mandatory.

Once the size of the MemTable reaches a configured size 
*  the MemTable and WAL become immutable,  
*  a new MemTable and WAL are allocated for subsequent writes. 
*  the contents of the MemTable are flushed to a “Sorted String Table” (SSTable) data file on disk,  
*  the flushed MemTable and associated WAL are discarded.  

* Each SSTable stores data in sorted order, divided into uniformly-sized blocks. Each SSTable also has an index block 
with one index entry per SSTable block for binary search.

#### Compaction

![image](https://user-images.githubusercontent.com/7579608/126607408-be0c5018-a7ce-4a94-8bed-9a9d22365778.png)

* The LSM tree has multiple levels of SSTables
* The newest SSTables are created by MemTable flushes and placed in Level-0. Levels higher
than Level-0 are created by a process called compaction
* The size of SSTables on a given level are limited by configuration parameters. When level-L’s size target is exceeded, some SSTables in level-L are selected and merged with the overlapping SSTables in level-(L+1). In doing so, deleted and overwritten data is removed, and the table is optimized for read performance and space efficiency. This process gradually migrates written data from Level-0 to the last level.
* Compaction I/O is efficient as it can be parallelized and only involves bulk reads and writes of entire files.

##### Compaction Type
- Leveled Compaction was adapted from LevelDB and then improved. In this compaction style, levels are assigned exponentially increasing size targets 
- Tiered Compaction (called Universal Compaction in RocksDB) is similar to what is used by Apache Cassandra or HBase. Multiple sorted runs are lazily
compacted together, either when there are too many sorted runs, or the ratio between total DB size over the size of the largest sorted run
exceeds a configurable threshold. Finally,
- FIFO Compaction simply discards old files once the DB hits a size limit and only performs lightweight compactions. It targets in-memory caching applications.


#### Read
* A key lookup occurs at each successive level until the key is found or it is determined that the key is not present in the last level. 
* It begins by searching all MemTables, followed by all Level-0 SSTables, and then the SSTables in successively higher levels. 
* At each of these levels, binary search is used. 
* Bloom filters are used to eliminate an unnecessary search within an SSTable file. Scans require that all levels be searched.

Reference https://www.usenix.org/system/files/fast21-dong.pdf

