#!/bin/bash

kubectl create -f ./kubernetes/spark-master-deployment.yaml
kubectl create -f ./kubernetes/spark-master-service.yaml

sleep 10

kubectl create -f ./kubernetes/spark-worker-deployment.yaml
kubectl apply -f ./kubernetes/minikube-ingress.yaml
