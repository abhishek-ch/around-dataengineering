# Paxos vs Raft - 

[Paper](https://arxiv.org/pdf/2004.05074.pdf) by Heidi Howard & Richard Mortier

### Distributed Consensus

_Distributed consensus is a fundamental primitive for constructing fault-tolerant, strongly-consistent distributed systems_

Distributed consensus, in short, is to make all processes in a system to agree on a single value after one or more processes propose this value.

Distributed consensus allows multiple machines to share the same state and run the same deterministic state machine, 
so that the entire machine can continue working normally when a few machines fail.

[reference](https://www.alibabacloud.com/blog/paxos-raft-epaxos-how-has-distributed-consensus-technology-evolved_597127)

![image](https://user-images.githubusercontent.com/7579608/118272252-a59b3700-b4c2-11eb-9ad5-3bc6102bdaac.png)


#### Multi Paxos

Multi-Paxos elects a leader, and the proposal is initiated by the leader. Due to zero competitions, the livelock problem is eliminated. 
If all proposals are initiated by the leader, the preparation phase can be skipped to change the two-phase process to a one-phase process, 
which improves the efficiency. Multi-Paxos does not assume a unique leader. Instead, it allows multiple leaders to propose requests concurrently 
without affecting safety. 

_Multi-Paxos can be optimized to skip the preparation phase and directly enter the acceptance phase when the same proposer makes continuous proposals_


#### Raft
 Raft is proposed from the multi-replicated state machine. Raft assumes that the system has at most one leader at any time, and proposals can only be sent by a leader (strong leader). Otherwise, the correctness is affected.


### Similarities

##### State Machine Safety 
If a server has applied
a log entry at a given index to its state machine, no other server
will ever apply a different log entry for the same index.

##### Leader Completeness
If an operation op is
committed at index i by a leader in term t then all leaders of
terms > t will also have operation op at index i.


### Differences 
![image](https://user-images.githubusercontent.com/7579608/118272961-a54f6b80-b4c3-11eb-93c5-d620e40aaf46.png)


### Summary
![image](https://user-images.githubusercontent.com/7579608/118272871-881a9d00-b4c3-11eb-99ad-16fbb448f851.png)

### Conclusion
Paper concluded that both Paxos and Raft take a very similar approach to distributed consensus, differing only in their approach to leader election. Most notably, Raft only allows servers with up-to-date logs to become leaders, whereas Paxos allows any server to be leader provided it then updates its log to ensure it is up-to-date.

Much of the understandability of Raft comes from the paper’s clear presentation rather than being fundamental to the underlying algorithm being presented
