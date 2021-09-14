# Riak Database - Key Value 

__Riak KV stores data as a combination of keys and values, and is a
fundamentally content-agnostic database__


![image](https://user-images.githubusercontent.com/7579608/133268274-36b5e1d6-0716-4757-9868-eae994ffb57a.png)


Riak is a masterless system designed to favor availability, even in the event of node failures and/or
network partitions. Any server (“node” in Riak parlance) can serve any incoming request, regardless of data
locality, and all data is replicated across multiple nodes. If a node experiences an outage, other nodes will
continue to service write and read requests

## The Ring
The Ring State is a data structure that gets communicated and
stays in sync between all the nodes, so each node knows the
state of the entire cluster. If a node gets a request for an object
managed by another node, it consults the Ring State and
forwards the request to the proper nodes, effectively proxying
the request as the coordinating node. 

## VNode:
Each vnode is a separate process which is assigned a partition of the Ring.

"This uniformity of Riak KV vnode responsibility provides the basis
for Riak KV’s fault tolerance and scalability. If your cluster has 64
partitions and you are running three nodes, two of your nodes
will have 21 vnodes, while the third node holds 22 vnodes"

> No single vnode is responsible for more than one
replica of an object.

## The CAP
In Riak, data is automatically distributed evenly across nodes using consistent hashing. Consistent hashing
ensures data is evenly distributed around the cluster and new nodes can be added with automatic, minimal
reshuffling of data. This significantly decreases risky “hot spots” in the database and lowers the operational
burden of scaling.

_Hashing and shared responsibility for keys across nodes ensures that data in Riak is evenly distributed. When
machines are added, data is rebalanced automatically with no downtime. New machines take responsibility for
their share of data by assuming ownership of some of the partitions; existing cluster members hand off the
relevant partitions and the associated data_

## Replication
Riak KV chooses one vnode to exclusively host a range of keys,
and the other vnodes host the remaining non-overlapping
ranges. With partitioning, the total capacity can increase by
simply adding commodity servers.
Since replication improves availability and partitions allow us to
increase capacity, Riak KV combines both partitions and replication to work together

_Relaxed consistency, also known as eventual consistency, means that
not all of the assigned nodes for a transaction in a distributed
system need to have that transaction confirmed before the
distributed system considers that transaction to be complete.
This allows for a higher degree of workload concurrency and
data availability_

* Riak KV stores data as a combination of keys and values in buckets 
* Buckets in Riak KV provide logical namespaces so that identical keys in different buckets will not conflict.
* A unique key in Riak KV is defined by bucket/key. 

## Data Consistency
Riak KV addresses any inconsistencies
by returning the most recently updated version, determined by
looking at the object’s Dotted Version Vector, or DVV. DVVs are
metadata attached to each data replica when it is created. They
are extended each time a data replica is updated in order to
keep track of data versions.

_"A more advanced
capability, called Active Anti Entropy, addresses colder data, AAE is a background process which continually
compares merkle trees across replica sets to determine
discrepancies. Both are key to preventing the need for manual
operator intervention under failure scenarios."_

## The Quorum:
To provide high availability, Riak KV defaults to what is known as a
sloppy quorum, meaning that if any primary node
is unavailable, the next available node in the cluster will accept
requests. That node will then update the primary node when it
comes back online. This ability to easily handle node failures is
known as a hinted handoff.

## References
* https://docs.huihoo.com/riak/from-relational-to-riak.pdf
* https://riak.com/content/uploads/2016/05/RiakKV-Enterprise-Technical-Overview-6page.pdf
