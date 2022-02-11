# Deploying Spark on Kubernetes

## Want to learn how to build this?

Check out the [post](https://testdriven.io/deploying-spark-on-kubernetes).

## Want to use this project?

### Minikube Setup

Install and run [Minikube](https://kubernetes.io/docs/setup/minikube/):

1. Install a  [Hypervisor](https://kubernetes.io/docs/tasks/tools/install-minikube/#install-a-hypervisor) (like [VirtualBox](https://www.virtualbox.org/wiki/Downloads) or [HyperKit](https://github.com/moby/hyperkit)) to manage virtual machines
1. Install and Set Up [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to deploy and manage apps on Kubernetes
1. Install [Minikube](https://github.com/kubernetes/minikube/releases)

Start the cluster:

```sh
$ minikube start --memory 8192 --cpus 4
$ minikube dashboard
```

Build the Docker image:

```sh
$ eval $(minikube docker-env)
$ docker build -t spark-hadoop:2.2.1 -f ./docker/Dockerfile ./docker
```

Create the deployments and services:

```sh
$ kubectl create -f ./kubernetes/spark-master-deployment.yaml
$ kubectl create -f ./kubernetes/spark-master-service.yaml
$ kubectl create -f ./kubernetes/spark-worker-deployment.yaml
$ minikube addons enable ingress
$ kubectl apply -f ./kubernetes/minikube-ingress.yaml
```

Add an entry to /etc/hosts:

```sh
$ echo "$(minikube ip) spark-kubernetes" | sudo tee -a /etc/hosts
```

Test it out in the browser at [http://spark-kubernetes/](http://spark-kubernetes/).
