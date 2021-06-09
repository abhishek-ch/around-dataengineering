# How data engineering get complicated over time

![image](https://user-images.githubusercontent.com/7579608/121359933-44854880-c934-11eb-8116-7d75f031eece.png)


* When a data platform/data access available, users grow exponentially. With growing users, 
existing stable running systems becomes unstable. Now the platform demands lot more energy, pager duty & postmortems to keep it always consistent.

> This needs highly skilled, infrastructure centric data software engineers. Needs 24*7 attention, so multiple-geographic localted team is good


* With quickly growing data volume, data engineering promotes from a scalable system to a very complicated hard-to-scale system

> Simply adding nodes to growing data size will hit the wall. Distributed Systems behave very differently with data shuffling. More nodes lead to more network issues

* With time, many more data products pop up. With more products, needs more sophisticated data infrastructure & platforms. 
All Data Products have very different scopes & which brings a lot more work to the data engineers.

> Different products results in many more data pipelines with conflicts & dependencies. Managing them needs understanding all the running pipelines

* Managing 50 Nodes cluster is entirely different from managing 500 nodes clusters. Distributed Systems’ problems are very real and more 
complex with growing nodes.

> More nodes lead to more cost & bringing the cost down, or efficiently running the nodes are a different dimension. As a dataengineer, writing an efficient data pipeline becomes a 
necessity than Good to have! 

* The trend of `every data is important \ data is gold` makes data management a nightmare. Data Governance and security for various kinds of data needs many full-time engineers.
