## Create and prepare the cluster


## [A] Infrastructure Dependencies

### (1) Create the kind cluster with a given config

```bash
kind create cluster -n chipy --config cluster.yaml
```

### (2) Install the nginx ingress

```bash
helm install ingress-nginx-release ingress-nginx \
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

### (3) Postgres

#### Add the Postgres Helm repos

Add repo for postgres-operator and postgres-operator-ui
```bash
helm repo add postgres-operator-charts \
    https://opensource.zalando.com/postgres-operator/charts/postgres-operator
helm repo add postgres-operator-ui-charts \
    https://opensource.zalando.com/postgres-operator/charts/postgres-operator-ui
```

#### Run the actual Install of the Postgres Operator

```bash
# install the postgres-operator
helm install postgres-operator \
    --namespace postgres \
    --create-namespace \
    postgres-operator-charts/postgres-operator \
    --version 1.10.1

# (optional) install the postgres-operator-ui 
helm install postgres-operator-ui \
    --namespace postgres \
    --create-namespace \
    postgres-operator-ui-charts/postgres-operator-ui \
    --version 1.10.1
```

#### (optional) Port forward to UI 

This will help you generate a Custom Resource Definition (CRD) yaml for a postgres
database. (We already have one for this example... see next step.)

```bash
kubectl port-forward svc/postgres-operator-ui 8080:80

Browse to http://localhost:8080
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


### (4) Metrics Server (optional)


Add repo for metrics-server 

```bash
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
```

Install the metrics server helm chart

```bash
helm upgrade --install metrics-server metrics-server/metrics-server \
    --version 3.12.0 \
    --set apiService.insecureSkipTLSVerify=true \
    --set-json='args=["--kubelet-insecure-tls=true", "--requestheader-client-ca-file="]' \
    --namespace kube-system
```

## [B] Build and load the docker image into Kind

```bash
docker build -f ../docker/Dockerfile -t chipy:v1 ../

kind load -n chipy docker-image chipy:v1
```

## [C] Two ways to install

### [1] Install raw yaml version

```bash
kubectl apply -f ./yaml 
```

### [2] Install with Helm

```bash
helm upgrade --install chipy-deploy  helm/chipy-k8s/ 

```

### Find the connection info for the ingress


#### Find the IP that you need to connect to

```bash
kubectl  get node -l node-role.kubernetes.io/control-plane \
    -o "jsonpath={.items[0].status.addresses[?(@.type=='InternalIP')].address}"

172.18.0.3
```

OR

```bash
docker container inspect chipy-control-plane \
  --format '{{ .NetworkSettings.Networks.kind.IPAddress }}'

172.18.0.3
```

OR

```bash
kubectl get node -o wide
```

```bash
NAME                  STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
chipy-control-plane   Ready    control-plane   22m   v1.25.3   172.18.0.4    <none>        Ubuntu 22.04.1 LTS   5.15.0-94-generic   containerd://1.6.9
```

#### Find the ports that you need to connect to


```yaml
kubectl  get svc -n ingress-nginx ingress-nginx-controller -o yaml
```

```yaml
  ...
  ...
  ports:
  - appProtocol: http
    name: http
    nodePort: 30080   # <<<---- this
    port: 80
    protocol: TCP
    targetPort: http
```

OR 

```bash
kubectl get service \
    -n ingress-nginx ingress-nginx-release-controller \
    -o "jsonpath={.spec.ports[0].nodePort}"

30080

kubectl get service \
    -n ingress-nginx ingress-nginx-release-controller \
    -o "jsonpath={.spec.ports[1].nodePort}"

30443
```

#### Make a request in a browser

Edit /etc/hosts to map the domain name

```bash
172.18.0.3 chipy-k8s.org
```

Browse to 
```
http://chipy-k8s.org:30080 
```

OR

```bash
curl  -k -v http://chipy-k8s.org:30080
```


## Delete the cluster when done

```bash
kind delete  cluster -n chipy
```



