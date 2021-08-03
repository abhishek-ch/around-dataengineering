# Foundation DB

![image](https://user-images.githubusercontent.com/7579608/127642075-02fcc50f-789f-457d-8f4d-1abb450bb394.png)


FoundationDB is an open source transactional key value store which combines the felxibilty of flexibility and scalability of NoSQL architectures with the 
power of __ACID transactions__. It offers a minimal and carefully chosen feature set, which has enabled a range of disparate systems to be built as layers on top
FoundationDB adopts an unbundled architecture that decouples an
- _in-memory transaction management system_
-  _distributed storage system_ , (SS) is used for storing data and servicing reads
- _built-in distributed configuration system_ 

Each sub-system can be independently scaled. FoundationDB uniquely integrates a deterministic simulation framework, used to test every new feature of the system.
FoundationDB’s focus on the “lower half” of a database, leaving the rest to its “layers”—stateless applications developed on top to provide various data models and other capabilities

## Architecture

Core Stateful Components -
1. __Coordinators__, to hold metatdata. Based on Paxos
2. __Transaction Logs__, Distributed WAL responsible for accepting commits and writes to the system. Write Once Read Never datastructure & mutations are only being held
 transeantly. As data comes in, its appended into the file and TTL is once the Storage Server have the data
3. __Storage Server__, Individual unit of KV system which can coordinate with eachother and becomes a single big Key Value Store. Each KV holds data for long term coming from Transaction Logs and serving read requests. _Each Storage Server is linked with designated set of Transaction Logs to add __Efficiency__ in the system_

![image](https://user-images.githubusercontent.com/7579608/127644956-561f3a66-fdfe-4f3b-8493-dee97a39495d.png)

## The main design principles 
- FDB decouples the transaction management system (write path) from
the distributed storage (read path) and scales them independently
- Instead of fixing all possible failure scenarios, the transaction system proactively shuts down when it detects a failure, Such an error handling strategy is desirable as long as the recovery is quick, and pays dividends
by simplifying the normal transaction processing
- Mean-Time-To-Recovery (MTTR), In our production clusters, the total time is usually less than five seconds
- Simulation Testing Framework: FDB relies on a randomized, deterministic simulation framework for testing the correctness of its distributed database.


### Cluster Controller

![image](https://user-images.githubusercontent.com/7579608/127984422-64c85d56-88ac-4586-97ee-18a281b4a1f2.png)


Cluster Controller is a leader elected by the Coordinators, to organize all the processes in the cluster. The work and communication is similar to Quoram.
- The ClusterController monitors all servers in the cluster and recruits three singleton processes ie _Sequencer, DataDistributor,
and Ratekeeper_ , which are re-recruited if they fail or crash. 
- _Sequencer_ assigns read and commit versions to transactions. 
- _DataDistributor_ is responsible for monitoring failures and balancing data among StorageServers. 
- _Ratekeeper_ provides overload protection for the cluster

When any process starts up, it first interact with the Coordinator to find the Cluster Controller and then the process updates all its info to the controller. Then the cluster controller interacts with all of the Workers and start assigning different roles like become a log server or SS etc. CC as well responsible for __Failure Monitoring__

### Data Plan

Transaction Management provides transaction processing and consists of a stateless processes, designed to provide the __Consistency Model__
* _Sequencer_, assigns a read version and a commit version to each transaction
* _Proxies_, MVCC read versions to clients and orchestrate transaction commits.
* _Resolvers_, check for conflicts between transactions 

__LogServers__ act as replicated, sharded, distributed persistent queues, where each queue stores WAL data for a StorageServer.  

The SS consists of a number of __StorageServers__(SS) for serving client reads, where each StorageServer stores a set of data shards, i.e., contiguous key ranges. StorageServers are the majority of processes in the system, and together they form a _distributed B-tree_

#### Read

> FoundationDB has a 5 Second Transaction Limit

* Reads are directly going to the SS, responsible for the desired range of Key. Reads are vesioned, so client will have to pass a Version along with the desired key.
* SS holds recent commits along with Version in _Memory_
* To abide the 5 sec rule, SS limits the in-memory history !


- Key location metadata is cached by the client and if that is not available, the client can ask for key location from proxy
- if the shards are refreshed or key location changes, the SS will intimate the client about cache invalidation, and the client can redirect to proxy
- Load balancing/ data distribution is automated which reshuffles shards internally, based on  2 phase commit protocol.

### Commit
- Writes are cached upon the clients, commit bundles everything done in a transaction, and send as a single unit to one of the proxies 
- Proxy assigns a new commit version to the transaction
- Proxy aware of SS and transaction log mapping

> Master only job is to return incremental commit versions to the users

#### Resolvers
_After a commit version, the resolver detects the differences between reading and the new  commit version_

⭐ When one starts a transaction, the client can see all commits ever made in the system
To get the latest version of reading, proxies sync versioning in-between and return the latest version to the client. 
This technique is batched for scaling reason 


## When Transaction Log Dies:Failure Handling - Explicit
- Cluster Controller tries to find the failing TL and will replicate the entire Transaction Subsystem (Master, Proxies, Resolvers & Transactions Logs) using Paxos
- The new master will look for the old TL logs for the last committed version. During this process, the master will block all transactions


## Notes
- Transaction size is limited to 10 MB, including the size of all written keys and values as well as the size of all keys in read or write conflict ranges that
are explicitly specified.
- FDB targets OLTP workloads that are read-mostly, read and write a small set of keys, have low contention, and require scalability
- Reads scale linearly with the number of __StorageServers__. Similarly, writes are scaled by adding more processes to __Proxies, Resolvers, and LogServers__ in TS and LS.

## References

- Paper https://www.foundationdb.org/files/fdb-paper.pdf
- Technical Overview https://www.youtube.com/watch?v=EMwhsGsxfPU
- Paper Overview https://www.youtube.com/watch?v=A6Ob1lebIzQ
