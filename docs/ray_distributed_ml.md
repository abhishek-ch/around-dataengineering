# Ray - Towards General Purpose Machine Learning System aka OS

Ray provides simple API for distributed applications.
Task can consists of DAG of stateless functions, can handle ETL workload & designed for parallel computation.
Actor(Stateful) is designed for #microservices & more complex computations.
* Ray is Python native with core part written Cython Binding & scheduler is C++
* Decentralized architecture gives better scheduling performance
* Efficient Shared memory with Zero-copy read

## Highlights
- Feature processing in ETL clusters but Training data & Model Tuning in different clusters, leads to a system consist of different clusters 
- Job Composition across multiple systems is a hard problem. Communication between heteregenous systems are usually in-efficient



![image](https://user-images.githubusercontent.com/7579608/126032216-4492d3f9-4612-46e0-a5ba-44308840e22f.png)

__machinelearning jobs needs many complicated steps before doing any ML specific jobs__


## Why
* Removing complex job dependencies by logically grouping jobs
* Single system, less maintenance
* Optimized Resource Sharing

## Highlights:
Ray now supports MODIN, DASK, #apachespark etc for data processing support

>> How Robust distributed memort management, Processing data beyond memory capacity.

## Problems:
* No out of core processing support
* Memory unaware scheduling
* No locality aware scheduling
* No admission control respecting hard memory limit

## How distributed shuffle work ?

_A shuffle is any operation over a dataset that requires redistributing data across its partition_
Its essential requirement because Distributed shuffle is the key factor for Distributed Memory Management &

## Improvement 
![image](https://user-images.githubusercontent.com/7579608/126032207-77e08356-a3c2-42fb-96d4-9e3aaefa48ae.png)


- Locality Aware Scheduling, schedule task on the machine which already holds the object in memory & Memory Aware Scheduling, Memory per machine awareness
- Object spilling to external storage.
- Tolerant to more memory usage than maximum memory capacity. 
- Respecting hard limit for distributed object store, along with guaranteeng progress when applications run out of memory by evicting unnecessary ojects or spilling objects.
- Admission control for scheduling tasks, dont schedule if not possible!

## Optimization Internals:
![image](https://user-images.githubusercontent.com/7579608/126032201-06b589b5-5135-4318-8423-aaf5e8a21f1c.png)


* Inside Map: When new Ray tasks needed to be schedule on a fully capacity node, ray automatically spills the objects from Shared-memory to external object store to make space for new objects.
* Inside Reduce: If ray tasks needed to access an external objects from external store, then Ray replaces LRU objects from Shared-memory with desired objects from external storage
* End of the World, no Memory left situtation: If there is no memory left in shared-memory object store for task scheduling, Ray doesn’t schedule tasks if the task inputs require more memory than its capacity after it’s scheduled


Reference https://www.youtube.com/watch?v=DNLqvdov_J4
