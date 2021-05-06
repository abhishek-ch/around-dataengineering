# Distributed Tracing

#### Dapper, Google’s production distributed systems tracing infrastructure, and describe how our design goals of low overhead, 
application-level transparency, and ubiquitous deployment on a very large scale system were met.

> Distributed Tracing System is for information about the behavior of complex #distributedsystems like Root Cause Analysis

![image](https://user-images.githubusercontent.com/7579608/117311727-c04b2b80-ae84-11eb-9190-9255b5c5651a.png)


_Dapper’s foremost measure of success has been its usefulness to developer and operations teams. 
Dapper began as a self-contained tracing tool but evolved into a monitoring platform which has enabled the creation of many different tools, 
some of which were not anticipated by its designers_

## Without the system
- Hard to identify the exact service & any change made
-  engineer will not be an expert on the internals of every service; each one is built and maintained by a different team
- services and machines may be shared simultaneously by many different clients, so a performance artifact may be due to the behavior of another application

## Design Goals
- Low overhead
- Application-level transparency: programmers should not need to be aware of the tracing system
- Scalabilty

2 classes of solutions to aggregate multilayer information-
- _black-box_ , assumes  there is no additional information other than the message record described, and use statistical regression techniques
to infer that association
- _annotation-based_ , rely on applications or middleware to explicitly tag every record with a global identifier that
links the message records back to the originating request

__While black-box schemes are more portable than annotation-based methods, they need more data in order 
to gain sufficient accuracy due to their reliance on statistical inference__

[Paper Link](https://research.google/pubs/pub36356.pdf)

Dapper is able to follow distributed control paths with
near-zero intervention from application developers by relying almost entirely on instrumentation of a few common libraries!

Dapper Stages:
1. Span data is written to a local log file
1. Dapper collectors reading the traces from daemon on production machines
1. Collectors writing the trace to a single Bigtable repository


