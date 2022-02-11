#!/bin/bash

. /common.sh

echo "$(hostname -i) spark-master" >> /etc/hosts

/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master --ip spark-master --port 7077 --webui-port 8080
