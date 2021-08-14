# Azure Cosmos Database - Data modeling & Partitioning

_A NoSQL DB is Non-Relational & Horizontally Scalable_

<img src="https://user-images.githubusercontent.com/7579608/129447376-1a03736a-edc3-4850-8011-4f176bd82df3.png" alt="cosmos" width="600"/>

Establishing relation between entities in NoSQL DB is very different than a Relational System

## Should we embed data or to reference ?

* Embed is dumping multiple relational tables in a single json file
* Reference refers on keeping same number of document files as relational tables

<img src="https://user-images.githubusercontent.com/7579608/129447821-d05ac959-258b-4c23-b604-e56cc3ae4608.png" alt="cosmos" width="600"/>

### 
* __Embed When__ 1:1 / 1:Few relationship but 1:many / many:many relation for __Reference__
* __Embed When__ Related items are queried and updated together 


### What is Partition Key in a Cosmos DB Container

<img src="https://user-images.githubusercontent.com/7579608/129448180-f9188570-21da-463f-a189-c5e598507952.png" alt="cosmos" width="600"/>

Concepts of Partition is exactly same. There must be balance in partitions and avoiding hot partitions. Evenly distribution is the key, so choosing
the right partition key is very important.

_Partition is actually LOGICAL_




## Reference
* https://www.youtube.com/watch?v=utdxvAhIlcY

