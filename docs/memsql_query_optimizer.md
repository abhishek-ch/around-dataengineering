# The MemSQL Query Optimizer: A modern optimizer for real-time analytics in a distributed database

MemSQL is a distributed SQL database designed to exploit memory-optimized, scale-out architecture to enable real-time transactional and analytical workloads which are fast, highly concurrent, and extremely scalable
Supports 2 formats - an in-memory row-oriented store and a disk-backed column-oriented store
* Supports MVCC & memory-optimized lock-free #datastructures
* Shared nothing architecture 

## Discussion Points-
-How query rewrite decisions oblivious of distribution cost can lead to poorly distributed execution plans
-To choose high-quality plans in a distributed database, the optimizer needs to be distribution-aware in choosing join plans, applying query rewrites, and costing plans. 
-methods to make join enumeration faster and more effective, such as a rewrite-based approach to exploit bushy joins in queries involving multiple star schemas without sacrificing optimization time. 
-Query plan is based on SQL which makes it very easy to read and understand the plan

🔥 _Aggregator nodes serve as mediators between the client and the cluster, while leaf nodes provide the data storage and query processing backbone of the system_
* For Distributed tables, rows are hash-partitioned, or sharded, on a given set of columns, called the shard key, across the leaf nodes.
* For Reference tables, the table data is replicated across all nodes. 
* Query plans are compiled to machine code and cached to expedite subsequent executions. Rather than cache the results of the query, MemSQL caches a compiled query plan to provide the most efficient execution path

## Query Optimizer Framework
* __Rewriter__: Applies SQL-to-SQL rewrites. 
* __heuristics vs cost__: the cost being the distributed cost of running the query. 

## Enumerator: determines the distributed join order and data movement. 

### BUSHY JOIN 
![image](https://user-images.githubusercontent.com/7579608/130971563-66cbd4b3-76a2-469f-8662-c4b23f76a3f0.png)

The problem of finding the optimal join permutation is extremely costly and time-consuming. It performs great with multiple star or snowflake schemas

## Planner: Converts the chosen logical execution plan to a sequence of distributed query and data movement operations. SQL extensions RemoteTables and ResultTables to represent a series of Data Movement Operations and local SQL Operations using a SQL-like syntax 
generates the distributed query execution plan (DQEP)

## Rewriter:
Converting a given SQL query to another semantically equivalent SQL query, which may correspond to a better performing plan
Rewriter locates opportunities to apply a query transformation, decides based on heuristics or cost estimates whether the rewrite is beneficial, and if so applies the transformation to yield a new query operator tree.
Heuristic and Cost-Based Rewrites, Pushdown, column elimination , schema merging and others
Interleaving of Rewrites, ordering transformations
Costing Rewrites, properly estimating the cost of new query transformation

## Reference
https://www.vldb.org/pvldb/vol9/p1401-chen.pdf
