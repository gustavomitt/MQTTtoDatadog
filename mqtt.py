import logging
from datetime import datetime
import sys
import os
import paho.mqtt.client as paho
from datadog import initialize, api
import json
import time

# Setup datalog connection
def setup_datalog():
    options = { 'api_key': os.environ['DATADOG_APIKEY'], 'app_key': os.environ['DATADOG_APPKEY'] }
    initialize(**options)


# Get Datalog metricJson
def get_datalog_metric(start,end,query):
    return api.Metric.query(start=start, end=end, query=query)


# Get Datalog metricJson
def set_datalog_metric(metric,timestamp,value,host):
    return api.Metric.send(metric=metric, points=(timestamp,value),host=host)

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/IoTmanager/dev01-vaso/Humidade/status")

def on_message(mosq, obj, msg):
    logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    metricJson = json.loads(str(msg.payload))
    sadasd = metricJson['status']
    logger.info("Status: " + metricJson['status'])
    resp = set_datalog_metric('vase.humidity',time.time(),float(metricJson['status']),'vase')
    #resp = api.Metric.send(metric='vase.humidity', points=(time.time(), float(metricJson['status'])),host='vase')
    logger.info("Response: " + str(resp))

def on_publish(mosq, obj, mid):
    logger.info("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    logger.info(string)


def intLogging():
    logger = logging.getLogger('python')
    hdlr = logging.FileHandler('/var/log/python.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    logger = intLogging()

    # init datadog
    setup_datalog()

    # get data files
    mqttc = paho.Client()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    #mqttc.on_log = on_log

    # Get CLOUDMQTT environment variables
    server=os.environ['MQTTSERVER']
    user=os.environ['MQTTUSER']
    password=os.environ['MQTTPASSWORD']
    port=os.environ['MQTTPORT']
    #url_str = "mqtt://" + server + ":" + port
    #url = urlparse.urlparse(url_str)

    # Connect
    mqttc.username_pw_set(user, password)
    mqttc.connect(server, port)

    # Subscription inside on_connect
    # mqttc.subscribe("/IoTmanager/dev01-vaso/Humidade/status", 0)


    # Continue the network loop, exit when an error occurs
    #rc = 0
    while True:
        rc = mqttc.loop_forever()
        if rc != 0:
            logger.info("rc: " + mqttc.error_string(rc))
