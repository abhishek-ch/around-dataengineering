# Why Apache Iceberg for Change Data Capture

This doc contains the notes derived from the blog https://www.alibabacloud.com/blog/how-to-analyze-cdc-data-in-iceberg-data-lake-using-flink_597838
_Update Frequency expectations are High_

## Difference between copy-on-write vs merge-on-read

* __copy-on-write__ can efficiently rewrite some of the files and generate appended full data sets. It is also the fastest in data analysis
* __Merge-on-read__ directly appends the data and the CDC flag to Iceberg

> The incremental data is efficiently merged with previous full data based on a specific format. This enables the near-real-time import and real-time data read.


![image](https://user-images.githubusercontent.com/7579608/123259519-d5435300-d4f4-11eb-8e43-9f7c0db7420b.png)


## Apache Iceberg Basics

Iceberg contains two types of files: 
1. __Data Files__, such as Parquet files in the following figure. Each data file corresponds to a check file (.crc file). 
2. Table __metadata files__, including Snapshot files (snap-.avro), Manifest files (.avro), and TableMetadata files (*.json)

![image](https://user-images.githubusercontent.com/7579608/123260510-ef316580-d4f5-11eb-9805-b44a471377c7.png)

Iceberg is a unified data lake storage architecture that supports various computing models and engines for analysis, including Spark, Presto, and Hive. The generated files are stored in column storage mode for later analysis.  
Iceberg is designed for data lakes based on snapshots and supports incremental read. The Iceberg architecture is simple enough and has no online service nodes. Besides, Iceberg is a table-type middleware that allows the upstream platforms to customize their logic and services.
