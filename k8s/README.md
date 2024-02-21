
kind create cluster -n chipy --config cluster.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

docker build -f ../docker/Dockerfile -t  chipy:v1 ../

kind load -n chipy docker-image chipy:v1

kubectl apply -f ./yaml 

docker container inspect chipy-control-plane \
  --format '{{ .NetworkSettings.Networks.kind.IPAddress }}'


kind delete  cluster -n chipy