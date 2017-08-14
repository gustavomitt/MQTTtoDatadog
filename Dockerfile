FROM python:2.7

# Install required packages
#RUN apt-get update
#RUN apt-get install -y python-dev

# Install MQTT python libraries
RUN pip install paho-mqtt

# Install Datadog python libraries
RUN pip install datadog

# Copy application files
COPY mqtt.py /app/



# Run the command on container startup
CMD python /app/mqtt.py
