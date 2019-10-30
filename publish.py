import paho.mqtt.client as mqtt
from sense_hat import SenseHat
from scipy import stats
from datetime import datetime
from time import sleep
from json import dumps

#broker_url = "broker.hivemq.com"
#broker_url = "localhost"
broker_port = 1883

# Specific information for Thingsboard
username="qVOnV8Xtt7qAVzqM3jLt"
password="" # not used
broker_url= "demo.thingsboard.io"
topic = "v1/devices/me/telemetry"

def on_connect(client,userdata,flags,rc):
    print("Connected With Code: {}".format(rc))

def on_disconnect(client,userdata,rc):
    print("Disconnected With Code: {}".format(rc))

client = mqtt.Client()
client.username_pw_set(username,password)
# Calling callback on connect and disconnect
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(broker_url, broker_port)

sense = SenseHat()
sense.set_imu_config(True,False,False) # Only compass is enabled
data = dict()
# Publishing the message
while True:
    # Environmental sensors
    
    # Curve fitting temp data (TODO)
    # x = round(sense.get_temperature(),3)
    # y = datetime.timestamp(datetime.now())

    # slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

    temp = round(sense.get_temperature(),3)
    hum = round(sense.get_humidity())
    pressure = round(sense.get_pressure(),3)
    temp_from_hum = round(sense.get_temperature_from_humidity(),3,)
    north = round(sense.get_compass())

    #IMU Sensor
    orientation = sense.get_compass_raw()
    orientation_msg = "x: {x}, y: {y}, z: {z}".format(**orientation)
    
    # client.publish(topic="raspberrypi/temp", payload=temp, qos=0, retain=False)
    # client.publish(topic="raspberrypi/hum", payload=hum, qos=0, retain=False)
    # client.publish(topic="raspberrypi/pressure", payload=pressure, qos=0, retain=False)
    # client.publish(topic="raspberrypi/temp_from_humidity", payload=temp_from_hum, qos=0, retain=False)
    
    # client.publish(topic="raspberrypi/orientation",payload=orientation_msg,qos=0,retain=False)

    data["temp"] = temp
    data["hum"] = hum
    data["pressure"] = pressure
    data["temp_from_hum"] = temp_from_hum
    data["orientation"] = orientation_msg
    data["north"] = north

    published_data = dumps(data)
    client.publish(topic=topic,payload=published_data,qos=0,retain=False)
    sleep(0.5)

# Looping the program forever
client.loop_forever()