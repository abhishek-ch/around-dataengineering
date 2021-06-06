# Why Cluster Load Balancing is a big deal for Distributed Systems

Reference https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf

## Foundation

__Hashing__ is the process to map data of arbitrary size to fixed-size values.
In Computer Science, hashing is used to evenly distribute in-memory datastructure load

![image](https://user-images.githubusercontent.com/7579608/120918937-58704680-c6b7-11eb-808d-9d66765e95fb.png)


Hashing is a computationally and storage space efficient form of data access which avoids the non-linear access time of ordered and unordered lists 
and structured trees, and the often exponential storage requirements of direct access of state spaces of large or variable-length keys

## Distributed System Hashing

### Problem

With normal hashing, for a small change in the size of cluster, will lead to shuffling of data accross all the nodes,
which __extremely expensive__ for Distributed System.


### Solution  - Minimize Shuffling

_Data distribution should not depend on the number of nodes in a cluster_

Consistent Hashing is a distributed hashing scheme that operates independently of the number of servers or objects in a distributed hash table 
by assigning them a position on an abstract circle, or hash ring. This allows servers and objects to scale without affecting the overall system.

### Naive Explaination

1. Hashring consists of infinite number of nodes.
2. There is no fixed location of a node.

