# Description

Project to read humidity data from vase sent to MQTT and send it some datalog service

## Build the image
```
PROJECT_ID="$(gcloud config get-value project)"
docker build -t gcr.io/${PROJECT_ID}/read_mqtt:v1 .
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
gcloud docker -- push gcr.io/${PROJECT_ID}/read_mqtt:v1
```
## criar os segredos no kubernetes
```
source ~/MQTTtoDatadog/mqtt.rc
source ~/MQTTtoDatadog/datadog.rc
kubectl create secret generic mqtt \
      --from-literal=MQTTSERVER=$MQTTSERVER \
      --from-literal=MQTTUSER=$MQTTUSER \
      --from-literal=MQTTPASSWORD=$MQTTPASSWORD \
      --from-literal=MQTTPORT=$MQTTPORT
kubectl create secret generic datadog \
      --from-literal=DATADOG_APIKEY=$DATADOG_APIKEY \
      --from-literal=DATADOG_APPKEY=$DATADOG_APPKEY
```
## criar o deployment no kubernetes
```
kubectl create -f ~/MQTTtoDatadog/getSalesData/get-sales-data-deployment.yaml  
```
## entrar no pod para testes
```
kubectl exec -it <nome do pod> -- /bin/bash
```
