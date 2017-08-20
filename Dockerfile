# image for amd
#FROM python:2.7
FROM python:2.7-alpine3.6

# image for raspberry pi
#FROM hypriot/rpi-python

# Install required packages
#RUN apt-get update
#RUN apt-get install -y python-dev

# Install MQTT python libraries
RUN pip install paho-mqtt

# Install Datadog python libraries
RUN pip install datadog

# Copy application files
COPY mqtt.py /app/
# Copy test files
COPY test.py /app/



# Run the command on container startup
CMD python /app/mqtt.py
