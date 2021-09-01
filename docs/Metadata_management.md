# Large Scale Metadata Management System without any Trade-Offs


<img src="https://user-images.githubusercontent.com/7579608/131548292-2db0febc-b2b8-4423-a027-2182c1655ff3.png" alt="drawing" width="600"/>


Big Data systems have tried to reduce the amount of metadata to scale the system, often compromising query performance.
Used the same distributed query processing and data management
techniques that we use for managing data to handle Big metadata.

_"most data warehouses rely on scan
optimizing techniques using compiled code execution and block
skipping based on storing min/max values of clustering/sorting
columns defined on the table"_

## Problem
The co-location of block-level metadata with the data itself affects
the efficiency of subsequent queries, because the distributed metadata
aren’t readily accessible without opening and scanning the
footer (or header) of each block, typically stored on disk.

The cost of opening the block is often equivalent to scanning some columns in it.
To avoid this cost during query execution, a different approach
used by systems such as Redshift and DB2 BLU is to store a
small amount of summarized metadata in the centralized state. This
approach achieves low latency, but its centralized nature fundamentally
limits the scalability of the amount of metadata that can be
stored.

DB2 BLU creates internal in-memory tables called synopsis tables
that store some column-level metadata about the tables. 
Metadata System is inspired by the synopsis but ignores in-memory & 
works for large amounts of metadata needed to support arbitrarily large tables. 

## Hive Metastore:
 a metadata repository for Hive tables and partitions, can be configured to
run on various relational databases. Varying scalability limits exist
around the number of partitions that can be queried in a single
query to prevent overload

## Delta Lake
Based on Transaction Log compacted Into Parquet Format.
_Google’s Metadata management system is like Delta Lake’s Columnar Metadata Layout._

## Query Execution Engine

- Query plan can be described as a DAG (directed acyclic graph) of
stages, where each stage is replicated across a number of workers
which run the same set of operators over different pieces of data.
The number of workers running for the given stage is the stage’s
degree of parallelism

- Physical query plans in BigQuery are dynamic. The Query Coordinator
builds an initial plan, but as the query starts execution, the
query plan starts changing based on the actual data statistics observed
during the execution	

## Metadata Structure
*	Logical metadata is information
about the table that is generally directly visible to the user. Some
examples of such metadata are Table schema, Partitioning and Clustering
specifications, column and row level ACLs. This information
is generally small and lends itself to quick access. P
*	Physical metadata is information about the table’s storage that BigQuery
maintains internally in order to map a table name to its actual data. Examples of such information are Locations of the blocks in the file system, row counts, lineage of data in the blocks, MVCC information,
statistics and properties of column values within each block

Physical metadata, while being extremely valuable for query execution, is not easily accessible

### Accessing Physical Metadata
*	Orgainizing the physical metadata of each table
as a set of system tables that are derived from the original table.
*	Storing column level information about the min/max values (called range constraints),
hash bucket and modulus values (called hash constraints)
and a dictionary of column values. 
*	Other variants of system tables include those that store posting lists of column values. Query optimizer
chooses one or more such system tables for planning and
executing the query

Most of the data in a table is stored in columnar blocks on
Colossus. DML and other write operations such as bulk import
and streaming lead to the creation and deletion of rows in these
blocks. A block is considered active at a snapshot timestamp if it
contains at least one row that is visible at that timestamp. Blocks
with no visible rows remain in the system for a configurable amount of time in order to support a feature known as “time travel” that allows
reading the table as of any given timestamp within the history
window. A query that reads this table needs to find the locations of
the blocks that are currently active in the table. Inside the blocks, it
is possible to have rows that are not visible at the timestamp. They
are filtered out when reading the block.

## Incremental Generation

Every DML operation leads to update of Column Metadata

* When a new block is created,  gathers the properties of the block, assign a creation timestamp and write an entry to the metadata change log. 
 * When a block needs to be deleted, we write a log entry with the deletion timestamp to the log.

__This change log is written to a highly available, durable replicated storage system. Operations on table may create and/or mutate millions of blocks, and the metadata change log guarantees ACID properties for these mutations__
 
LSM style merges on the change log to produce baselines and deltas of changes.
_At any given read timestamp, the table’s metadata can be constructed by reading the baseline available at that timestamp and any deltas from the baseline up to the read timestamp_

## Query Planning:
Loading table metadata before query planning of 10GB+ tables are huge so it defers the reading of physical metadata for the tables until the actual dispatch of partitions to the workers. 
To facilitate this, 
* The query planner first uses only the logical metadata to generate a query plan with constants folded and filters pushed down. 
* it rewrites the query plan as a semi-join of the original .



# Reference

http://vldb.org/pvldb/vol14/p3083-edara.pdf
