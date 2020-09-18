# Abhishek

## Data is Coming :partying_face:

And the Data arrives. Well I have no idea, what is that data all about but just heard it is around ~ 10 GB.
Well its gonna be structured, so it gonna be really easy to estimate, isn't it :relieved:

We all connected, and all of us were pretty much convinced on easy sql engine, maybe postgres and then we can simply run 
some basic query for data analysis.

![](images/postgres.png)

Then we finally decided to look into the data, it was CSV, yeah 10 GB of CSV ( gzipped) :hot_face: !

### Time for debate
Nothing is easy !
A huge file of csv, unzipped and we have now many things to consider
	
	* Is it really gonna be the only file ?
	* Is the data actually clean ??
	* Is postgres really a smart choice ?
	* If we already have bigdata platform setup, why not using it ?
	* Are we really gonna use all the fields in the data
	* ...

So the best choice was to really focus on data exploration!

## Data Exploration

Data Exploration is really not about loading the data, but here first we need to know the data!
To know more about data, we have the default choice - Apache Spark

![](images/spark.png)
	
	1. Store the data on any distributed file system, lets consider here S3.
	2. Load data in Apache Spark
	3. Run analysis, peace of cake :pancakes:

No, how can it be so easy ? Well its a single file of < 10 GB of size and Spark Driver gonna hurt very badly. So it is really not 
a logical way to just load this data on spark and do anything.

### Data Partition Plan

We need a way to make this process __scalable__!
We decided to split the data into multiple partitions of some reasonable size. As its spark, we are deciding on __~150 - 250 MB__.

Do we really wanna continue using CSV ? 
No, we need a more optimized columnar data format, so Parquet was an obvious choice for us.

![](images/parquet.png)

	1. Load the data in Spark
	2. Write the data back to S3 within partition range as Parquet Data Format.


### Data Exploration Visualization

We heard data is ready, can we explore the data! Suddenly Data Analysts & Data Scientists jumped into the discussion.
No, You cannot :rotating_light:

As a data engineer, I can imagine visualization over command line, but I am not sure my colleagues are really gonna hate me 
for that. So, we need to provide an interface.
So our data exploration platform should have the following -

	1. Open Sourced
	2. Support Large Scale data exploration
	3. Fancy Graphs
	4. Dashboarding
	5. Sharing
	6. Governance

So technically, it asked for almost everything as a __large scale project__.
Well after many hours of discussions -

![](images/presto.png)                     ![](images/metabase.png)

	 1. PRESTO, an open source distributed SQL query engine 
	 2. METABASE, open source way for everyone in your company to ask questions and learn from data.

_disclaimer: There are still discussions on why not apache superset or some other distributed sql engine & I am sure its never gonna end._

But for now we have an amazing interface which can be used by our Analysts & Scientists to explore the data and learn insights.
Hurray, we can now make Data Driven Decisions. Can we :cold_sweat:


## Big Data

Well we were expecting to calm down & then suddenly we got hit by data, a lot of data.
__The problem now shifted from data to BigData__

So what, we have spark cluster and partition, so we will transform everything to parquet and life is great	:sunglasses:.
Not that early, well there are many problems we never addressed when we started -

	1. Queries are too slow
	2. Infrastructure is burning too much money
	3. Even its structered data, its has too many Nulls, weird characters and what not
	4. Way too much data to explore

We realized we never optimized the job for faster query, but just to add partitions. There was not even a discussion on data cleaning as we were 
not aware what to expect. Big Data came too soon & we didn't had any pipeline managing that.

