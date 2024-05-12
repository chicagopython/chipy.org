# Demo of ChiPy Website on Kubernetes

The following demonstrates several ways that you can deploy the ChiPy website on
Kubernetes.

1) Install the ChiPy into the cluster piece-by-piece

    - using raw Kubernetes yaml (see ./yaml/ directory)
    - using local Helm charts (see ./helm/ directory)

2) Install the everything into the cluster in one shot using Helmfile
   (see helmfile.yaml)

This portion of the codebase was created in support of the following talk:

    Shipping ChiPy: Running ChiPy.org on a Kubernetes Cluster
    By: Joe Jasinski 
    https://www.chipy.org/meetings/248/

The companion Slide Deck for this is here:
https://docs.google.com/presentation/d/1bRXCyvZkoG3J5aahS6osK3tAJ3FHp3NGxHqvpITjoFQ/edit#slide=id.g2d0d1017bd1_0_237

## Requirements

You will need:

- A recent copy of kubectl from the [Kubernetes website](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/). This is the official kubernetes
  client, which we will use to run various kubernetes commands.
  I'm using kubectl version 1.25, but newer versions should work.
- Docker running on your machine. The cluster will run inside of Docker using
  the Kind Kubernetes distribution.
- A recent version of "Kind" from [the Kind website](https://kind.sigs.k8s.io/docs/user/quick-start/#installation).
  This is a simple Kubernetes distribution useful for development and testing.
  I'm using v0.17.0.
- A recent copy of Helm from [the Helm website](https://helm.sh/docs/intro/install/).
  Helm is a package manager for Kubernetes applications that helps you group,
  package and install Kubernetes applications.
  I'm using v3.14.3, though anything greater than v3 should work.

This tutorial works best on Linux, though you can run it on OSX. I need to
figure out some of the routing for Docker Desktop on OSX to get to the UI, but
you can get to the UI using kubernetes port-forwarding [see APPENDIX B]

## INSTALL THE CLUSTER PIECE-BY-PIECE

### [A] INFRASTRUCTURE DEPENDENCIES

#### (1) Create the kind cluster with a given config

[Kind](https://kind.sigs.k8s.io/) is a project that lest you run Kubernetes inside of Docker. It will be used for this tutorial, so you will need to install it.

```bash
kind create cluster -n chipy --config cluster.yaml
```

#### (2) Install the Nginx ingress

You can install the Nginx Ingress server via Helm as below. Here, we customize
some of the variable inputs using the `--set` flags, so we can tune it for kind.

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

OR - you could install it by applying the following yaml as documented on
their website. However, it's much harder to customize (you have to edit the yaml), and I recommend just using the above Helm approach.

~~kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml~~

#### (3) Postgres

##### Add the Postgres Helm repos

Add repo for postgres-operator and postgres-operator-ui. This makes the Postgres
Operator Helm Charts available for install (but does not install anything.)

```bash
helm repo add postgres-operator-charts \
    https://opensource.zalando.com/postgres-operator/charts/postgres-operator
helm repo add postgres-operator-ui-charts \
    https://opensource.zalando.com/postgres-operator/charts/postgres-operator-ui
```

##### Run the actual Install of the Postgres Operator

This installs the Postgres Operator, which is basically a factory for creating
and managing Postgresql databases. This step does not actually install a Postgres 
database, but installs the service that will eventually create a database.

```bash
# install the postgres-operator
helm install postgres-operator \
    --namespace postgres \
    --create-namespace \
    postgres-operator-charts/postgres-operator \
    --version 1.10.1
```

Optionally install a UI for the Postgres operator.

```bash
# (optional) install the postgres-operator-ui
helm install postgres-operator-ui \
    --namespace postgres \
    --create-namespace \
    postgres-operator-ui-charts/postgres-operator-ui \
    --version 1.10.1
```

##### (optional) Port forward to UI

This will help you generate a Custom Resource Definition (CRD) yaml for a postgres
database. (We already have one for this example, so you do not have to do this... but it could be useful to view for learning purposes.)

If you want to access the UI simply, you can run the following port-forward
and browse to localhost in a browser.

```bash
kubectl port-forward svc/postgres-operator-ui 8080:80

Browse to http://localhost:8080
```

##### Apply the CRD cluster yaml

When the Postgres Operator was installed it also installed a Custom Resource Definition (CRD), which defines a new kubernetes resource type. The resource type
that it defined is for defining and creating Postgres database instances.

Below is a Custom Resource (CR) that makes use of the Postgres Custom Resource
Definition to define a Postgres database that will run in-cluster. When the following CR yaml is applied, the Postgres Operator will create a Postgres
database instance that will run in-cluster and match the specification given.

```bash
kubectl apply -f helm/postgres/templates/pg-cluster.yaml
```

When the Postgres instance is created, it also creates a k8s secret for the
admin user for the master and standby.

- postgres.chipydb.credentials.postgresql.acid.zalan.do
- standby.chipydb.credentials.postgresql.acid.zalan.do

The connection string would look like the following

```bash
"postgres://$(POSTGRES_USERNAME):$(POSTGRES_PASSWORD)@$(POSTGRES_HOST):$(POSTGRES_PORT)/$(POSTGRES_DB)"
```

Where...

- POSTGRES_USERNAME comes from the postgres master secret
- POSTGRES_PASSWORD comes from the postgres master secret
- POSTGRES_HOST - is the name of the k8s service for postgres (i.e. chipydb)
- POSTGRES_PORT - is the standard postgres port 5432
- POSTGRES_DB - is the name of the auto-created postgres logical db (i.e. chipy)

#### (4) Metrics Server (optional)

This installs the kubernetes metrics server, which monitors the CPU/RAM for 
pods and nodes in a k8s cluster. The metrics that this generates can be used
by the `kubectl top` command, by metrics collector/aggregators like Prometheus,
and can be used by the pod autoscaler.

Add repo for metrics-server. This does not actually install the metrics server,
but makes it available for installing via Helm.

```bash
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
```

Install the Metrics Server Helm Chart

```bash
helm upgrade --install metrics-server metrics-server/metrics-server \
    --version 3.12.0 \
    --set apiService.insecureSkipTLSVerify=true \
    --set-json='args=["--kubelet-insecure-tls=true", "--requestheader-client-ca-file="]' \
    --namespace kube-system
```

After a few minutes, the metrics-server will be running and the following
commands will be available.

```bash
kubectl top nodes
kubectl top pods -A
```

Debug:

```bash
kubectl get apiservices | grep metrics
```

### [B] INSTALL THE CHIPY WEBSITE INTO KUBERNETES

#### Build and load the docker image into Kind

This builds the Docker image for ChiPy on your local machine, but does not
push it to a Docker remote.

```bash
docker build -f ../docker/Dockerfile -t chipy:v1 ../
```

This is a special "kind" command that lets you "side-load" the Docker image
into a Kind cluster. This is useful for local development so you do not have
to publish your Docker image to a remote in order to use it.

```bash
kind load -n chipy docker-image chipy:v1
```

#### Install ChiPy via RAW YAML or via Helm

##### [Option 1] Install raw yaml version

This is a simple implementation of the ChiPy deployment for ease of understanding.
This for demonstration purposes only.

```bash
kubectl apply -f ./yaml
```

##### [Option 2] Install with Helm (RECOMMENDED)

This is a second copy of the ChiPy deployment in the form of a local Helm Chart.
This copy has received more attention than the raw yaml copy (so it will probably
work better).

```bash
helm upgrade --install release01  helm/chipy-k8s/
```

### [C] VIEW THE CHIPY WEBSITE IN A BROWSER

To connect to the cluster in a browser, see the section below
"Connect to the Cluster in a Browser"

### [D] DELETE THE CLUSTER WHEN DONE

The following will destroy the entire kind cluster.

```bash
kind delete cluster -n chipy
```

## INSTALL EVERYTHING IN ONE SHOT USING HELMFILE

The second approach to deploying ChiPy on K8s is to use the `helmfile.yaml`,
which defines all of the Helm charts needed to deploy all of the above services.
Therefore, the installation is much simpler. More info about [Helmfile](https://helmfile.readthedocs.io/en/latest/) is available at
[https://helmfile.readthedocs.io](https://helmfile.readthedocs.io).

### [A] CREATE THE CLUSTER

Create a kind cluster, providing the `cluster.yaml`.

```bash
kind create cluster -n chipy --config cluster.yaml
```

### [B] BUILD AND INSTALL CHIPY AND OTHER SERVICES

#### Build and load the ChiPy Docker image

This builds the Docker image for ChiPy on your local machine, but does not
push it to a Docker remote.

```bash
docker build -f ../docker/Dockerfile -t chipy:v1 ../
```

This is a special "Kind" command that lets you "side-load" the Docker image
into a Kind cluster. This is useful for local development so you do not have
to publish your Docker image to a remote in order to use it.

```bash
kind load -n chipy docker-image chipy:v1
```

#### Deploy everything

To install all the Helm charts needed for this application, which includes the
chipy.org and all of its dependencies, run the following.

Note: There are a number of ways to install the Helmfile command, which typically comes
as a static binary that you can download from the Helmfile github repo. However,
to make things easier, I have created a "./helmfile" script, which runs Helmfile
via a Docker container. That way, you do not have to install Helmfile locally.

```bash
./helmfile sync
```

### [C] VIEW THE CHIPY WEBSITE IN A BROWSER

To connect to the cluster in a browser, see the section below
"Connect to the Cluster in a Browser"

### [D] DELETE EVERYTHING TO CLEAN UP

The following will uninstall all of the Helm Charts.

```bash
./helmfile destroy
```

OR you can destroy the entire cluster.

```bash
kind delete cluster -n chipy
```

## CONNECT TO THE CLUSTER IN A BROWSER

### Find the connection info for the ingress

In order to connect to the cluster as though we were connecting to it externally,
we need to find the IP address of one of the nodes. Here are 3 ways to do that.

Note: the below steps identify the IP node address to use to connect to the ingress. This should work for Linux users. However, for OSX users, there is an
additional networking layer involved. You can port-forward to the chipy webserver service instead to view the site. See APPENDIX B

#### Find the IP that you need to connect to

Approach 1) Find the control plane node and lookup its external IP address

```bash
kubectl  get node -l node-role.kubernetes.io/control-plane \
    -o "jsonpath={.items[0].status.addresses[?(@.type=='InternalIP')].address}"

172.18.0.3
```

OR Approach 2) Inspect the docker container IP address of the control plane node using Docker.

```bash
docker container inspect chipy-control-plane \
  --format '{{ .NetworkSettings.Networks.kind.IPAddress }}'

172.18.0.3
```

OR Approach 3) Get the node IP off of 'kubectl get node' wide view.

```bash
kubectl get node -o wide
```

```bash
NAME                  STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
chipy-control-plane   Ready    control-plane   22m   v1.25.3   172.18.0.4    <none>        Ubuntu 22.04.1 LTS   5.15.0-94-generic   containerd://1.6.9
```

#### Find the ports that you need to connect to

In addition to finding the IP address of a node to connect to, we need to find
the port to connect to. The Nginx Ingress Controller created a k8s service of
type NodePort, which exposes a port on each node that will direct traffic to
the Ingress Controller pods.

Approach 1) Find the Nginx Ingress Controller's k8s service, and lookup the Node port for that service

```yaml
kubectl  get svc -n ingress-nginx ingress-nginx-release-controller -o yaml
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

OR Approach 2) Use Kubectl to query out the exact nodePort field on the Ingress
Controller service yaml spec.

```bash
# http port
kubectl get service \
    -n ingress-nginx ingress-nginx-release-controller \
    -o "jsonpath={.spec.ports[0].nodePort}"

30080

# https port
kubectl get service \
    -n ingress-nginx ingress-nginx-release-controller \
    -o "jsonpath={.spec.ports[1].nodePort}"

30443
```

#### Update your hosts file

Now that we have both the IP and Port of a kubernetes node, which is accepting traffic for the Ingress Controller, we are
almost ready to make a request to it. However, first we must
set an /etc/hosts value for `chipy-k8s.org`. We need to do this
because we want the request "host" header to include the ChiPy
domain, which Django uses validate the request and Kubernetes
ingress uses to route the request.

Note: in a production situation, we would have a load-balancer
that would load balance traffic between the N nodes, so we would
not have to deal with this /etc/hosts business or looking up the
IP and ports, but since this is a simple example running locally,
we are just directly connecting to a the control plane node.

Edit /etc/hosts and add an entry for the IP found earlier.

```bash
172.18.0.3 chipy-k8s.org
```

#### Make a request in a browser

Browse to:

```
http://chipy-k8s.org:30080
```

OR

```bash
curl  -k -v http://chipy-k8s.org:30080
```

## APPENDIX A: ADVANCED cache the docker images locally (for my talk)

To cache docker downloads with kind, run these docker commands and uncomment
the lines in cluster.yaml

https://medium.com/@charled.breteche/caching-docker-images-for-local-kind-clusters-252fac5434aa

```bash
docker run -d --name proxy-docker-hub --restart=always \
  --net=kind \
  -e REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io \
  registry:2

docker run -d --name proxy-registry-k8s-io --restart=always \
  --net=kind \
  -e REGISTRY_PROXY_REMOTEURL=https://registry.k8s.io \
  registry:2

docker run -d --name proxy-registry-opensource-zalan-do --restart=always \
  --net=kind \
  -e REGISTRY_PROXY_REMOTEURL=https://registry.opensource.zalan.do \
  registry:2

docker run -d --name proxy-ghcr-io --restart=always \
  --net=kind \
  -e REGISTRY_PROXY_REMOTEURL=https://ghcr.io \
  registry:2
```

## APPENDIX B: Port forward to get to the Kubernetes UI on OSX

Since Kind uses Docker, and Docker is a Linux technology, this tutorial works
best on Linux. OSX runs Docker inside of a virtual machine in order to emulate
Linux. Therefore, there is some extra networking involved to get traffic into
Docker running on OSX.  More research is needed for this.

As a work-around for getting going on OSX, you use a Kubernetes port-forward
to access the cluster via a browser.

Instead of adding a hosts file entry as documented above, add the following
hosts file entry to map chipy-k8s.org to localhost.

```bash
/etc/hosts
127.0.0.1 chipy-k8s.org
```

Then run a kubernetes port-forward command as follows to point to the Ingress
Controller service.

```bash
kubectl -n nginx-ingress \
    port-forward svc/ingress-nginx-release-controller 30080:80
```

Finally, access the chipy-k8s.org domain at the following url:

Browse to http://chipy-k8s.org:30080/
