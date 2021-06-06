# Why Cluster Load Balancing is a big deal for Distributed Systems

![image](https://user-images.githubusercontent.com/7579608/120920394-d126d100-c6be-11eb-8594-caad1b3b16b9.png)



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

The ring follows clockwise allotment principle where each request can be served by the server node that first appears in this clockwise traversal ie  the first server node with an address greater than that of the request gets to serve it.


In consistent hashing when a Node is removed or added then the only key from that Node are relocated. For example, if  Node is removed then, all keys from Node N3 will be moved to server N3 but keys stored on server N1 and N2 are not relocated. But there is one problem when server N3 is removed then keys from N3 are not equally distributed among remaining servers S1 and S2. They were only assigned to server S1 which will increase the load on server S1.

To evenly distribute the load among Node when a Node is added or removed, it creates a fixed number of replicas ( known as virtual nodes) of each Node and distributed it along the circle. So instead of Node labels N1, N2 and N3, we will have N10 N11…N19, N20 N21…N29 and N30 N31…N39. The factor for a number of replicas is also known as weight, depends on the situation.


