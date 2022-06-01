#!/usr/bin/env python3

import signal
import sys
#from time import sleep
import time, datetime
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

BUTTON_GPIO = 3
flag_connected = 0

def signal_handler(sig, frame):
  GPIO.cleanup()
  sys.exit(0)

def on_connect(client, userdata, flags, rc):
  print("*Connected with result code "+str(rc))
  #client.subscribe("$SYS/#")
  global flag_connected
  if rc == 0:
    print("*Connection OK")
    flag_connected = 1
  else:
    print("*Connection error!")
    flag_connected = 0

def send(cmd):
  global flag_connected
  flag_connected = 0
  client1 = mqtt.Client("", clean_session=True)
  client1.on_connect = on_connect # callback
  #client1.on_publish = on_publish # callback
  client1.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
  client1.connect(MQTT_SERVER, MQTT_PORT) # establish connection
  timeout = 5
  timeout_start = time.time()
  while not flag_connected:
    client1.loop()
    if time.time() > timeout_start + timeout:
      print("*Connect error!")
      sys.exit()
  #sendMQTTmsg()
  print('*' + str(datetime.datetime.now()))
  msg = '{ "state": "' + cmd + '" }'
  print("*MQTT-message: " + msg)
  #client1.publish("zigbee2mqtt/olohuone_jalkalamppu_ylos/set", msg)
  client1.publish("zigbee2mqtt/vessan_eteinen_kattolamppu/set", msg)
  client1.disconnect()
  #sys.exit()

def button_callback(channel):
  time.sleep(0.2)
  if GPIO.input(BUTTON_GPIO):
    print("Button off!")
    send("OFF")
  else:
    print("Button on!")
    send("ON")

if __name__ == '__main__':

  f = open(sys.path[0]+"/credentials.txt", "r")
  exec(f.read())
  f.close()

  #send("OFF")
  #time.sleep(1)
  #send("ON")

  GPIO.setwarnings(False) # Ignore warning for now
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.add_event_detect(BUTTON_GPIO, GPIO.BOTH, callback=button_callback, bouncetime=500)
  signal.signal(signal.SIGINT, signal_handler)
  signal.pause()

