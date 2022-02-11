#!/bin/bash

kubectl delete -f ./kubernetes/spark-master-deployment.yaml
kubectl delete -f ./kubernetes/spark-master-service.yaml
kubectl delete -f ./kubernetes/spark-worker-deployment.yaml
kubectl delete -f ./kubernetes/minikube-ingress.yaml
