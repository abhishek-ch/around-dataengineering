# Paxos vs Raft - 

Paper by Heidi Howard & Richard Mortier

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
