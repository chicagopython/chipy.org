## Create and prepare the cluster

### Create the kind cluster with a given config

```bash
kind create cluster -n chipy --config cluster.yaml
```

### Install the nginx ingress

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

## Build and load the docker image into Kind

```bash
docker build -f ../docker/Dockerfile -t  chipy:v1 ../

kind load -n chipy docker-image chipy:v1
```

## Two ways to install

### Install raw yaml version

```bash
kubectl apply -f ./yaml 
```

### Install with Helm

TBD

### Find the connection info for the ingress

```bash
docker container inspect chipy-control-plane \
  --format '{{ .NetworkSettings.Networks.kind.IPAddress }}'
```

OR

```bash
kubectl get node -o wide
```

```bash
NAME                  STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
chipy-control-plane   Ready    control-plane   22m   v1.25.3   172.18.0.4    <none>        Ubuntu 22.04.1 LTS   5.15.0-94-generic   containerd://1.6.9
```

kubectl  get svc -n ingress-nginx ingress-nginx-controller -o yaml

```yaml
  ports:
  - appProtocol: http
    name: http
    nodePort: 32715   # <<<---- this
    port: 80
    protocol: TCP
    targetPort: http
```

Make a request in a browser

```bash
curl  -k -v http://172.18.0.4:32715
```

Edit /etc/hosts
```bash
172.18.0.4 chipy-k8s.org
```


## Delete the cluster when done

kind delete  cluster -n chipy

