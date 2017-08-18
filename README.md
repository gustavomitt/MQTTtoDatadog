# Description

Project to read humidity data from vase sent to MQTT and send it some datalog service

## Build the image
```
docker build -t read_mqtt:v1 .
```
## To run tests
source ~/MQTTtoDatadog/mqtt.rc
source ~/MQTTtoDatadog/datadog.rc
```
docker run -it \
  -e MQTTSERVER \
  -e MQTTUSER \
  -e MQTTPASSWORD \
  -e MQTTPORT \
  -e DATADOG_APIKEY \
  -e DATADOG_APPKEY \
  read_mqtt:v1 \
  python /app/test.py
```

## To run test docker image
source ~/MQTTready/mqtt.rc
source ~/MQTTready/datadog.rc
```
docker run -it \
  -e MQTTSERVER \
  -e MQTTUSER \
  -e MQTTPASSWORD \
  -e MQTTPORT \
  -e DATADOG_APIKEY \
  -e DATADOG_APPKEY \
  read_mqtt:v1
```
## copiar a imagem para o Google Cloud Engine
```
PROJECT_ID="$(gcloud config get-value project)"
gcloud docker -- push gcr.io/${PROJECT_ID}/get-sales-data:v2
```
## criar os segredos no kubernetes
```
source ~/mssql.rc
kubectl create secret generic sqlserver \
      --from-literal=SQLCMDSERVER=$SQLCMDSERVER \
      --from-literal=SQLCMDUID=$SQLCMDUID \
      --from-literal=SQLCMDPASSWORD=$SQLCMDPASSWORD
kubectl create secret generic openvpn --from-file ~/openvpn/client.ovpn
kubectl create secret generic criar-arquivo-json --from-file <path to json>
kubectl create secret generic criar-arquivo-boto --from-file <path to boto>
kubectl create secret generic ver-arquivo-json --from-file <path to json>
kubectl create secret generic ver-arquivo-boto --from-file <path to boto>
kubectl create secret generic file-and-pubsub-rw --from-file <path to boto>
```
## criar o deployment no kubernetes
```
kubectl create -f ~/kubernetesCluster/getSalesData/get-sales-data-deployment.yaml  
```
## entrar no pod para testes
```
kubectl exec -it <nome do pod> -- /bin/bash
```
