# A large scale analysis of hundreds of in-memory cache clusters at Twitter

In-memory caching is a mamaged service, and new clusters are provisioned semi-automatically to be used as look-aside cache upon request

## Gaps in understanding in-memory caching

* there has been a lack of comprehensive studies covering the
wide range of use cases in today’s production systems. 
* there have been new trends in in-memory caching
usage since the publication of previous work 
* some aspects of in-memory caching received little attention
in the existing studies, but are known as critical to practitioners

### Twitter Setup | Twemcache

![image](https://user-images.githubusercontent.com/7579608/119259308-ef280800-bbcd-11eb-9c94-7d86abac3703.png)

* Caching clusters are single-tenant based on the service team requesting them
* Deployed as a single-layer cache, which allows to analyze the requests directly from clients without being filtered by other caches
* Twemcache containers are highly homogeneous and typically small, and a single host can run many of them
* On-demand heap memory allocators can cause large and _unbounded external memory fragmentation_. To avoid this, Twemcache inherits the slab-based memory management from Memcached.

> Memory is allocated as fixed size chunks called slabs, which default to 1 MB. 
> Each slab is then evenly divided into smaller chunks called items. The class of each slab decides the size of its items

* Evcition in slab-based cache.  

_Memcached uses an approximateLRU queue per slab class to track and evict the least recently
used item. This works well as long as object size distribution
remains static_

### Slab Classification

![image](https://user-images.githubusercontent.com/7579608/119259567-2f3bba80-bbcf-11eb-8494-66f36031c4cc.png)


If all keys start with small values that grow over
time, new writes will eventually require objects to be stored
in a higher slab class. However, if all memory has been allocated
when this happens, there will be effectively no memory
to give out. 

To avoid slab calcification, Twemcache uses slab eviction
only. This allows the evicted slab to transition into
any other slab class. There are three approaches to choose the
slab to evict: 
- choosing a slab randomly (random slab), 
- choosing the least recently used slab (slabLRU)
- choosing the least recently created slab (slabLRC)


## Cache Use cases

* Storage , intesify computation ( data throughput)
* Computation, Blob like ML Models for real-time prediction. Non frequent update.
* Transient Data, Short time storage

## Analysis

### Miss Ratio

![image](https://user-images.githubusercontent.com/7579608/119259741-ecc6ad80-bbcf-11eb-86dc-56a0f5cb11fb.png)

Miss ratio is one of the key metrics that indicate the effectiveness
of a cache. Production in-memory caches usually
operate at a low miss ratio with small miss ratio variation

Low miss ratios and high stability in general illustrate the
effectiveness of production caches. However, extremely low
miss ratios tend to be less robust, which means the corresponding
backends have to be provisioned with more margins.
Moreover, cache maintenance and failures become a major
source of disruption for caches with extremely low miss ratios.
The combination of these factors indicate there’s typically a
limit to how much cache can reduce read traffic or how little
traffic backends need to provision for.

### Request Rate and Hot Keys

![image](https://user-images.githubusercontent.com/7579608/119259869-8beba500-bbd0-11eb-8337-5607df52bc93.png)

at times, when the request
rate (top blue curve) spikes, the number of objects accessed
in the same time interval (bottom red curve) also has a spike,
indicating that the spikes are triggered by factors other than
hot keys. Such factors include client retry requests, external
traffic surges, scan-like accesses, and periodic tasks.

### Correlations between Properties

![image](https://user-images.githubusercontent.com/7579608/119259972-00264880-bbd1-11eb-9021-b466eae40f30.png)

## Properties of Different Cache Use Cases

* Caching for Storage

Caches for storage usually serve ready-heavy workloads,
and their popularity distributions typically follow Zipfian distribution with a large parameter α in the range of 1.2 to 2.2.
While this type of workload is highly skewed, they are easier
to cache, and in production, 95% of these clusters have miss
ratios of around or less than 1%. 

* Caching for Computation

Caches under this category serve both read-heavy and writeheavy traffic depending on the workloads. For example, machine learning feature workloads are usually read-heavy showing a good fit of Zipfian popularity distribution. While intermediate computation workloads are normally write-heavy
and show deviations from Zipfian. Compared to caching for
storage, workloads under this category use shorter TTLs, usually determined by the application requirement. 

* Transient Data with No Backing Store

Caches under this category usually have short TTLs,
and the TTLs are often used to enforce implicit object deletion

## Eviction Algorithms

* Object LRU and object FIFO 
* slabLRU and slabLRC
* Random slab eviction
* Memcached-LRU 


## Miss Ratio Comparison

![image](https://user-images.githubusercontent.com/7579608/119260074-6b701a80-bbd1-11eb-9335-7c9bcf0e21fa.png)

## Summary

1. In-memory caching does not always serve read-heavy
workloads, write-heavy (defined as write ratio > 30%)
workloads are very common, occurring in more than
35% of the 153 cache clusters we studied.
2. TTL must be considered in in-memory caching because
it limits the effective (unexpired) working set size. Efficiently removing expired objects from cache needs to be
prioritized over cache eviction.
3. In-memory caching workloads follow approximate Zipfian popularity distribution, sometimes with very high
skew. The workloads that show the most deviations tend
to be write-heavy workloads.
4. The object size distribution is not static over time. Some
workloads show both diurnal patterns and experience
sudden, short-lived changes, which pose challenges for
slab-based caching systems such as Memcached.
5. Under reasonable cache sizes, FIFO often shows similar
performance as LRU, and LRU often exhibits advantages
only when the cache size is severely limited.
