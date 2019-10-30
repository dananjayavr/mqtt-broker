import paho.mqtt.client as mqtt
import time

# Start time and current time used to check refresh timer
start_time = time.time_ns() / 10**6 # ns -> ms
curr_time = start_time

# Refresh timer in ms
refresh = 5000 # 5000ms -> 5s

# Mqtt broker host and port
broker_url = "localhost"
broker_port = 1883

# Sensors subscribe topics
SENSORS_CONFIG_TOPIC = "/sensors/config"
SENSORS_GET_TOPIC = "/sensors/get"

# Sensors publish topics
SENSORS_TEMP_TOPIC = "/sensors/temp"
SENSORS_HUM_TOPIC = "/sensors/hum"
SENSORS_PRESS_TOPIC = "/sensors/press"

# Sensors subscribe config message callback
def on_message_config(client, userdata, message):
    global refresh
    
    # Debug message
    print("Sensors config message received: "+message.payload.decode())
    # Update refresh timer
    refresh = int(message.payload.decode())

# Sensors subscribe get message callback
def on_message_get(client, userdata, message):
    # Debug message
    print("Sensors get message received: "+message.payload.decode())

    # Message value handling
    if (message.payload.decode() == "temp"):
        client.publish(topic=SENSORS_TEMP_TOPIC, payload="22.8", qos=0, retain=False)
    elif (message.payload.decode() == "hum"):
        client.publish(topic=SENSORS_HUM_TOPIC, payload="38", qos=0, retain=False)
    elif (message.payload.decode() == "press"):
        client.publish(topic=SENSORS_PRESS_TOPIC, payload="900.5", qos=0, retain=False)
    else:
        print("Unknown get message !")

# Default subscribe message callback
def on_message(client, userdata, message):
    # Debug message
    print("Sensors other message received: "+message.payload.decode())

# Create and configure mqtt client
client = mqtt.Client()
client.on_message = on_message

# Connect to mqtt broker
client.connect(broker_url, broker_port)

# Subscribe to sensors config topic and register callback 
client.subscribe(SENSORS_CONFIG_TOPIC, qos=1)
client.message_callback_add(SENSORS_CONFIG_TOPIC, on_message_config)

# Subscribe to sensors get topic and register callback
client.subscribe(SENSORS_GET_TOPIC, qos=1)
client.message_callback_add(SENSORS_GET_TOPIC, on_message_get)

# Publish all sensors
client.publish(topic=SENSORS_TEMP_TOPIC, payload="19.5", qos=0, retain=False)
client.publish(topic=SENSORS_HUM_TOPIC, payload="25", qos=0, retain=False)
client.publish(topic=SENSORS_PRESS_TOPIC, payload="1024.2", qos=0, retain=False)

# Endless loop
while(True):

    # Call mqtt loop function (manages mqtt events)
    client.loop()

    # Check if refesh timeout is reached
    if((curr_time - (start_time + refresh)) >= 0):
        # Debug message
        print("Publish new sensors values...")
        client.publish(topic=SENSORS_TEMP_TOPIC, payload="19.5", qos=1, retain=False)
        client.publish(topic=SENSORS_HUM_TOPIC, payload="25", qos=0, retain=False)
        client.publish(topic=SENSORS_PRESS_TOPIC, payload="1024.2", qos=0, retain=False)

        # Update start time
        start_time = curr_time

    # Get current time
    curr_time = time.time_ns() / 10**6

    # Delay of 10ms
    time.sleep(0.01)
