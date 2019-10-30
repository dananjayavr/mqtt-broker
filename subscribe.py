import paho.mqtt.client as mqtt
from time import sleep
from sense_hat import SenseHat

broker_url = "broker.hivemq.com"
#broker_url = "localhost"

# Specific information for Thingsboard
# username="qVOnV8Xtt7qAVzqM3jLt"
# password="" # not used
# broker_url= "demo.thingsboard.io"
# topic = "v1/devices/me/telemetry"

broker_port = 1883

sense = SenseHat()

def on_connect(client,userdata,flags,rc):
    print("Connected With Result Code " + rc)

def on_message(client,userdata,message):
    print("Message Recieved: " + message.payload.decode())

def on_disconnect(client,userdata,rc):
    print("Disconnected With Result Code " + rc)

def on_message_from_temp(client,userdata,message):
    print("Data received from the temperature sensor: " + message.payload.decode())

def on_message_from_hum(client,userdata,message):
    print("Data received from the humidity sensor: " + message.payload.decode())

def on_message_from_orientation(client,userdata,message):
    print("Data received from IMU (orientation): " + message.payload.decode())

def on_message_from_pressure(client,userdata,message):
    print("Data received from the pressure sensor: " + message.payload.decode())

def on_led_on(client,userdata,message):
    X = [0, 181, 155]  # T2 Green
    R = [255, 0, 0]  # Red
    shape = [
        X, X, X, X, X, X, X, X,
        X, R, R, R, R, R, R, X,
        X, R, R, R, R, R, R, X,
        X, R, R, R, R, R, R, X,
        X, R, R, R, R, R, R, X,
        X, R, R, R, R, R, R, X,
        X, R, R, R, R, R, R, X,
        X, X, X, X, X, X, X, X
        ]
    sense.set_pixels(shape)

def on_led_off(client,userdata,message):
    sense.clear()

client = mqtt.Client()
#client.username_pw_set(username,password)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(broker_url, broker_port)

# Subscribing 
client.subscribe("raspberrypi/temp",qos=1)
client.subscribe("raspberrypi/hum",qos=1)
client.subscribe("raspberrypi/pressure",qos=1)
client.subscribe("raspberrypi/orientation",qos=0)

client.subscribe("raspberrypi/led/on",qos=1)
client.subscribe("raspberrypi/led/off",qos=1)

# Adding specific callback functions according to the topic
client.message_callback_add("raspberrypi/temp",on_message_from_temp)
client.message_callback_add("raspberrypi/hum",on_message_from_hum)
client.message_callback_add("raspberrypi/orientation",on_message_from_orientation)
client.message_callback_add("raspberrypi/pressure",on_message_from_pressure)

client.message_callback_add("raspberrypi/led/on",on_led_on)
client.message_callback_add("raspberrypi/led/off",on_led_off)

client.loop_forever()