# Algorithms behind Modern Storage Systems

![image](https://user-images.githubusercontent.com/7579608/126768611-d6454503-c444-462e-8148-57a238546b1c.png)


Database Access Pattern, Sequential Read & Write, -Its Harder

1. Sequential Accesses,  reading contiguous memory segments without seeks in between. 
Example, playing favorite album where tracks are perfectly laid down by artists and exactly in the way that you would enjoy listening to them

2. Random access doesn't read contiguous memory segments. So, it has to perform seeks in order to find the locations for the next read. These seeks are hard to predict. 
Example, listening to an album by randoming shuffling the songs and skipping and moving to other artists.


## About Sequential Write
- Sequential writes do not always result into the Sequential reads. Data that is written closely is not necessarily going to be read together.
- In order to achieve sequential writes, use either in-memory buffering or append-only storage. To ensure sequential read in Append-Only storage, use log storage like #apachekafka
- Write data to be read together can be done by collecting and buffering the records in memory, then sorting them, and then writing them down on disk.

> we can achieve sequential reads by either random writes or sequential writes. But with trade-off, locating write point or buffering when sorting the records.

> SSD can eliminate the cost of random IO reads but SSD relies on Block Read/Writes. So range scans can be only effectively implemented in the storage where data is laid out and prepared for sequential reads.

__Sequential Writes is bad with HDD or SSD__
* hard disk drives random IO is bad because the arm has to seek to the correct track, in order to navigate from one position to another to perform a write. 
* As SSDs are built using NAND gates and AND gates, the smallest erasable entity is a series of blocks. So a write operation can only set the single bits, but erase operations can unset  entire units like several blocks at a time.

### In-Short

Sequential IO is generally good, since it's more predictable and it gives you just more material to work with, to optimize, to make it faster and better. But because we cannot avoid random IO altogether

## Mutable vs Immutable Data Structure

![image](https://user-images.githubusercontent.com/7579608/126768716-87bfb55b-f785-4279-b5f2-d6800ee31293.png)

### Mutable data structures
- Mutable data structures usually pre-allocate the memory and do in-place updates. 
- To find the thing on the disk and update it in place wherever it was, in order to amortize the cost of writes for the data that is stored together. 
- This usually results into random IO; in order to perform a write, a bunch of reads have to be done in order to locate the destination. 
- Finally actual write, and the writes which are close to each other in time, will not most likely be written together. Since updates are made in place, all the data is read from a single source and reads will not have to merge and reconcile data from different sources, 
because we basically have a single source of truth. So, single file we just read from it.

### Immutable data structures
- The immutable data structures on other hand, require no memory overhead for the subsequent updates, since files are pretty much written on disk just once 
and will never be changed anymore
- However, in order to perform a read, since all the files are immutable, multiple versions of the same record of data for the 
same key located in the several different files. We will have to read all of the files, reconcile, merge the data together and only then we'll be
able to return it to the user. 
- Writes here are sequential. So data is batched up in memory and sorted and written out sequentially. And since files are not modified on disk and updates would effectively mean pretty much rewriting the whole file, immutable data structure require merge from different sources before 
- returning the data to different clients


## LSM Tree
ref https://arxiv.org/abs/1503.00075#:~:text=We%20introduce%20the%20Tree%2DLSTM,classification%20(Stanford%20Sentiment%20Treebank).

- LSM Trees is an immutable disk resident, write-optimized data structure
- Insert, update, and delete operations, and even for their sorted variants, do not require random IO
- __Flush__: For sequential writes, LSM Trees batch up writes and updates in memory resident table using sorted data structures such as a binary search tree or a skip list. So anything that would allow you quickly searching; logarithmic look-up time would be pretty good. And when the size of this table, memory-based table is reaching a certain threshold, its contents are written on disk.
- After a few flushes are performed and data ends up being split between multiple on-disk tables.
- To retrieve the data, needs to search old disk resident parts of the tree, check in memory table and their contents before returning the result itself.
- Writes are only addressing the memory resident table, while reads have to reconcile the data from everywhere, from memory and disk.

### LSM Tree Merge

- Disk resident and table files are immutable. They are written only once and never modified and can only be deleted on later stage.
- if two tables hold the same value for the same key, meaning that an update has occurred, only the record with the latter or later timestamp will be picked and the previous one will be discarded. Since the read operation cannot physically remove the data from immutable data structure, we have to use something called dormant certificates, sometimes also called tombstones. It indicates that a record for a certain key has to be removed starting with a certain timestamp, and during the merge process records shadowed by these tombstones are going to be discarded.


### Sorted String Table (SS Table)

> Many modern LSM implementations such as RocksDB, Apache Cassandra, choose sorted string tables as their file format because of its simplicity. 

- SS tables are persistent maps from keys to values ordered by the key. 
- Structurally, SS tables are split in two parts. It's an index and the data block. The index block contains keys mapped to the block offsets, pointing to where the actual record is stored or located
- Index is implemented using a format also with good look-up guarantees such as B-Tree, which is good for range scans, or if you just need point queries, you can use something like a hash table.

> for the point queries, in order to find the value by the key, it can be done quickly by simply looking up the index and locating the data than following offset and reading the data from the data file

#### Compaction
- SS tables are immutable and are written sequentially and hold no reserved space for in-place modifications, if we had a single SS table, any insert, update, or delete operation would probably mean that we have to re-write the entire file.
- In order to reduce the cost of reads, reconcile disk space caused by these shadowed records and reduce the amount of these tables that have to merged, the LSM Trees propose a process that reads complete SS tables from disk, merges them, and then writes them back. This process is called __Compaction__.


Reference https://www.youtube.com/watch?v=wxcCHvQeZ-U
