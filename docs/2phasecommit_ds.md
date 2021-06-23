# Two-Phase Commit - Distributed System Transactions

![image](https://user-images.githubusercontent.com/7579608/123090036-f8540100-d427-11eb-8637-5d1a852f4c03.png)


In Distributed Systems, to achieve ACID, we need _Distributed Transactions_

## Atomicity Focus

Either all nodes must commit or all must abort!

A distributed transaction system mainly consists of two subsystems,
which are also called the participant and the coordinator based on their roles in transaction execution.

![image](https://user-images.githubusercontent.com/7579608/123088946-a5c61500-d426-11eb-80eb-01016c301955.png)



## Steps

### Prepare Phase

* Once each database worker locally completes its transaction, it reponses to the coordinator with __DONE__ message.
* Once the coordinator receives the message from all the workers, it sends back __PREPARE__
* Each worker responds to the __PREPARE__ with __READY__
* If any workers responds __NOT READY__, the coordinator broadcasts __ABORT__

### Commit Phase

* Once the coordinator receives __READY__ from all workers, it broadcasts __COMMIT__ ( holds te details of the transaction)
* Each worker applies the transaction and acknowledges with __DONE__

_Coordinator confirms the transaction completed once it receives acknowledgements from all the workers_


## Difference between Consensus & Atomic Commit

![image](https://user-images.githubusercontent.com/7579608/123086709-0bfd6880-d424-11eb-96ef-d2ef72003a58.png)


## Slides 

https://www.cs.princeton.edu/courses/archive/fall16/cos418/docs/L6-2pc.pdf

## Blog 

https://alibaba-cloud.medium.com/tech-insights-two-phase-commit-protocol-for-distributed-transactions-ff7080eefe00

## Video

https://www.youtube.com/watch?v=-_rdWB9hN1c
