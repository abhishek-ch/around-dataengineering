# DBLog, Change-Data-Capture by Netflix


_Change-Data-Capture (CDC) allows capturing committed changes from a database in real-time and propagating those changes to downstream consumers_

DBLog is a Java based framework can capture changes in real-time & take dumps.Dumps are taken in chunks so that they interleave with real-time events and don’t stall real-time event processing for an extended period of time.It utilizes a watermark based approach that allows us to interleave transaction log events with rows that we directly select from tables to capture
the full state.

Transaction logs are the source of CDC events. As transaction logs typically have limited retention, they aren’t guaranteed to contain the full history of changes. Therefore, dumps are needed to capture the full state of a source.

## DBLog Features:
* Processing captured log events
* Dumps can be taken any time
* Taking log dumps in chunks
* No table locking
* Different kinds of output
* High Availability

![image](https://user-images.githubusercontent.com/7579608/116541512-d472b400-a8eb-11eb-9d18-2fba9addc88b.png)

## CDC core requirements:
* Derived stores (like ElasticSearch) must eventually store the full state of the source
* Real-time and dump events to be interleaved so that both make progress.
* Minimizing database impacts

### Notables:
_DBLog processes selects in chunks and tracks progress in a state
store (currently Zookeeper) allowing them to pause and resume
from the last completed chunk_


## Transaction Log Capture:
For each event we assume a Log-Sequence-Number (LSN) which is the offset of the event on the transaction log and is
encoded as an 8-byte monotonically increasing number!

## Full State Capture:
As transaction logs typically have limited retention they can not be used to reconstruct the full source dataset.

### Solution:
only uses commonly available database features and impacts the source database as little as possible. Instead of actually writing the latest state of rows into
the transaction log, we are selecting rows from tables in chunks and position the chunks in-memory next to events that we capture
from the transaction log. This is done in a way that does preserves
the history of log events

## Dump Processing:

By using watermarks, dumps are taken using the following steps:
1. Briefly pause log event processing.
1. Generate a low watermark by updating the watermark table.
1. Run SELECT statement for the next chunk and store result-set in-memory, indexed by primary key.
1. Generate a high watermark by updating the watermark table.
1. Resume sending received log events to the output. Watch for the low and high watermark events in the log.
1. Once the low watermark event is received, start removing entries from the result-set for all log event primary keys that are received after the low watermark.
1. Once the high watermark event is received, send all remaining result-set entries to the output before processing new log events.
1. Go to step 1 if more chunks present.


### References:
https://netflixtechblog.com/dblog-a-generic-change-data-capture-framework-69351fb9099b
https://arxiv.org/abs/2010.12597
