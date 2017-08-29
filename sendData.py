import ConfigParser
import cayenne.client
import time
import os
import string

Config = ConfigParser.ConfigParser()
Config.read("/opt/homelySensors/etc/cayenne.conf")

Sensors = ConfigParser.ConfigParser()
Sensors.read("/opt/homelySensors/etc/sensors.conf")

Collectors = ConfigParser.ConfigParser()
Collectors.read("/opt/homelySensors/etc/collectors.conf")

Config.read("/opt/homelySensors/etc/locations.conf")





# The callback for when a message is received from Cayenne.
def on_message(message):
  print("message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.


MQTT_USERNAME=Config.get('Cayenne','MQTT_USERNAME')
MQTT_PASSWORD=Config.get('Cayenne','MQTT_PASSWORD')
MQTT_CLIENT_ID=Config.get('Cayenne','MQTT_CLIENT_ID')



client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

timestamp = 0

while True:
  client.loop()
  if (time.time() > timestamp + 10):
        for section in Sensors.sections():
                for (key, val) in Sensors.items(section):
                        if key == "collector":
                                cmd=Collectors.get(val,'Command')+" -t "+Sensors.get(section,"Id")
                                for outline in os.popen(cmd).readlines():
                                        outline = outline[:-1]
                                        C = string.split(outline," ")
                                        if C[0] == Sensors.get(section,"romId"):
                                                channel=Sensors.get(section,"Channel")
                                                client.celsiusWrite(channel, C[1])
                                                print "Sending "+C[1]+" to channel "+channel
        timestamp = time.time()                              
                        





'''
i=0
timestamp = 0

while True:
  client.loop()

  if (time.time() > timestamp + 10):
    client.celsiusWrite(1, i)
    client.luxWrite(2, i*10)
    client.hectoPascalWrite(3, i+800)
    timestamp = time.time()
    i = i+1
'''

