
kind create cluster -n chipy --config cluster.yaml

docker build -f docker/Dockerfile -t  chipy:v1 .

kind load -n chipy docker-image chipy:v1

kind delete  cluster -n chipy