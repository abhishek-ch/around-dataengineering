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

* Caching clusters are single-tenant based on the service team requesting them
* Deployed as a single-layer cache, which allows to analyze the requests directly from clients without being filtered by other caches
* Twemcache containers are highly homogeneous and typically small, and a single host can run many of them
