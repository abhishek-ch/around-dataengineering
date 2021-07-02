# Distributed Tracing

Distributed Tracing

![image](https://user-images.githubusercontent.com/7579608/124244902-b873d480-db1f-11eb-8e02-9eb33065c4f2.png)

_Distributed Tracing engine uses UDP to exchange data, so there is no technically no performance impact._

* Span: are logical units of work in a #distributedysystem. Each Span captures important data points specific to the current process handling the request.
* Trace: a tree of spans that follows the course of a request or system from its source to its destination. It tells the requests story !
* Tags & Logs: Annotate the span with contextual information.

Uses:
* What services did a request pass through?
● What occured in each service for a given request?
● Where did the error happen?
● Where are the bottlenecks?
● What is the critical path for a request?
● Who should I page?

Problems:
Not much education, Vendor Lock in, Insconsistent APIs & Handoff woes

Solution:
![image](https://user-images.githubusercontent.com/7579608/124244821-a2feaa80-db1f-11eb-8d90-0f6ce7887bec.png)

OpenTelemtry: is made up of an integrated set of APIs and libraries as well as a collection mechanism via a agent
and collector. These components are used to generate, collect, and describe telemetry about distributed systems.


Single set of APIs for tracing and metrics collection.
● Standardized Context Propagation.
● Exporters for sending data to backend of choice.
● Collector for smart traces & metrics aggregation.
● Integrations with popular web, RPC and storage
frameworks.
