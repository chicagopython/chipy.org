## Create and prepare the cluster


## [A] Infrastructure Dependencies

### (1) Create the kind cluster with a given config

```bash
kind create cluster -n chipy --config cluster.yaml
```


### (2) Install the nginx ingress


```bash
helm install --namespace ingress-nginx ingress-nginx-release ingress-nginx \
    --version 4.9.1 \
    --namespace ingress-nginx \
    --create-namespace \
    --repo https://kubernetes.github.io/ingress-nginx \
    --set controller.hostPort.enabled=true \
    --set controller.service.type=NodePort \
    --set controller.service.nodePorts.http=30080 \
    --set controller.service.nodePorts.https=30443 
```

OR

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

## (3) Postgres

### Install Postgres Operator

Add repo for postgres-operator and postgres-operator-ui
```bash
helm repo add postgres-operator-charts https://opensource.zalando.com/postgres-operator/charts/postgres-operator
helm repo add postgres-operator-ui-charts https://opensource.zalando.com/postgres-operator/charts/postgres-operator-ui
```

#### Run the actual Install of the Postgres Operator
```bash
# install the postgres-operator
helm install postgres-operator postgres-operator-charts/postgres-operator --version 1.10.1

# install the postgres-operator-ui (optional)
helm install postgres-operator-ui postgres-operator-ui-charts/postgres-operator-ui --version 1.10.1
```

#### Port forward to UI (optional)

This will help you generate a Custom Resource Definition (CRD) for a postgres
database. (We already have one for this example... see next step.)

```bash
kubectl  port-forward postgres-operator-ui 8080:80
```

#### Apply the CRD cluster yaml 

The operator will create a db in the cluster defined in pg-cluster.

```bash
kubectl apply -f postgres/pg-cluster.yaml
```

This creates k8s secrets for authenticating to the master and standby
- postgres.chipydb.credentials.postgresql.acid.zalan.do
- standby.chipydb.credentials.postgresql.acid.zalan.do

The connection string would look like the following
```
"postgres://$(POSTGRES_USERNAME):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):$(POSTGRES_PORT)/$(POSTGRES_DB)"
```
Where...
- POSTGRES_USERNAME comes from the postgres master secret
- POSTGRES_PASSWORD comes from the postgres master secret
- POSTGRES_HOST - is the name of the k8s service for postgres (i.e. chipydb)
- POSTGRES_PORT - is the standard postgres port 5432
- POSTGRES_DB - is the name of the auto-created postgres logical db (i.e. chipy)


## [B] Build and load the docker image into Kind

```bash
docker build -f ../docker/Dockerfile -t chipy:v1 ../

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

```bash
kind delete  cluster -n chipy
```



