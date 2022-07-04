#!/usr/bin/env python3

# sudo apt install python3-pip python3-serial
# (sudo apt install python3-matplotlib)
# (sudo apt install python3-paho-mqtt)
# sudo pip3 install xmodem

PORT = '/dev/ttyACM0'
FILENAME = 'trend.log'

INTERVAL=300

#VERBOSE = True
VERBOSE = False

import sys, time, datetime, serial
from xmodem import XMODEM
#import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt

def getc(size, timeout=1):
  return ser.read(size) or None

def putc(data, timeout=1):
  return ser.write(data)  # note that this ignores the timeout

def send_cmd(cmd):
  ser.write(bytes(cmd, 'ASCII') + b'\r\n')
  print('*cmd: ' + cmd)

def receive_line(verbose = True):
  line = ser.readline().decode("ASCII").rstrip("\r\n")
  if verbose:
    print('*reply: ' + line) # b'Start receiving now.\r\n'
  return line

def download(filename):
  modem = XMODEM(getc, putc)
  cmd = 'upload ' + filename
  send_cmd(cmd) # b'upload trend.log\n'
  receive_line() # b'Start receiving now.\r\n'
  stream = open(FILENAME, 'wb')
  print('*Start receiving (XMODEM-CRC)')
  ser.flushInput()
  modem.recv(stream, crc_mode=1)
  line = receive_line() # b'28822 Bytes Transmitted.\r\n'
  size = int(line.split()[0])
  stream.truncate(size)
  stream.close()
  print('*downloaded ' + filename + ' (' + str(size) + ' bytes)')
  return size

def read_measurement(v):
  line = receive_line(VERBOSE)
  if line != '':
    value = float(line.split()[0])
    v.append(value)

def get_measurements(verbose = False):
  send_cmd('measurements')
  values = []
  read_measurement(values)
  while ser.inWaiting():
    read_measurement(values)

  if verbose:
    print('*', values)
  #v = [ values[8], values[9], values[14] ]
  try:
    v = [ values[8], values[9], values[14] ]
  except:
    v = [ float("nan"), float("nan"), float("nan") ]
  print('*Menovesi: ' + str(v[0]))
  print('*Ulkoilma: ' + str(v[1]))
  print('*Venttiili: ' + str(v[2]))
  return v


#00000000: 9d00 a005 1400 0200 0300 0400 0500 0900  ................
#00000010: 0800 1001 3201 1737 8f5f 0200 8c01 f1d8  ....2..7._......
#00000020: f1d8 f1d8 0000 0500 0000 2029 8f5f 0200  .......... )._..
#00000030: 8a01 f1d8 f1d8 f1d8 0000 0400 0000 782b  ..............x+
#00000040: 8f5f 0100 7901 f1d8 f1d8 f1d8 0000 0000  ._..y...........
#00000050: 0000 d02d 8f5f 0000 6d01 f1d8 f1d8 f1d8  ...-._..m.......
#00000060: 0000 0400 0000 2830 8f5f 0000 7a01 f1d8  ......(0._..z...
#00000070: f1d8 f1d8 0000 0900 0000 8032 8f5f 0000  ...........2._..
#00000080: 8201 f1d8 f1d8 f1d8 0000 0700 0000 d834  ...............4
def graph():
  file = open(FILENAME, 'rb')
  #"header" 22 bytes
  #one entry 20 bytes
  file.seek(0, 2) # end of file
  filesize = file.tell()
  file.seek(0, 0) # start of file
  samples = int((filesize - 22) / 20)
  print(samples)
  header = file.read(22)
  values = []
  x1 = []
  y1 = []
  for c in range(samples):
    data = file.read(20)
    epoch = (data[3] << 24) + (data[2] << 16) + (data[1] << 8) + data[0]
    ulko = ((data[5] << 8) + data[4]) / 10.0
    meno = ((data[7] << 8) + data[6]) / 10.0
    vent = ((data[17] << 8) + data[16]) / 1.0
    values.append([ epoch, ulko, meno, vent ])
    y1.append(float(meno))

  #print(epoch)
  date = time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(epoch))
  #print(values)
  file.close()

  for x in range(samples):
    epoch = values[x][0]
    x1.append(time.strftime('%H:%M', time.gmtime(epoch)))

  total = 160
  plt.plot(x1[0:total], y1[0:total])
  plt.xlabel('Aika')
  plt.ylabel('°C')
  plt.title('Menovesi')
  x_ticks = x1[:total:20]
  plt.xticks(x_ticks)
  #plt.axhline(y=5,color='gray')
  plt.grid()

  plt.show()

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

def on_publish(client, userdata, rc): #create function for callback
  #print("data published \n")
  print("*Data published with result code "+str(rc))
  #pass

def sendMQTTmsg():
  print('*' + str(datetime.datetime.now()))
  msg = '{ "v0":' + str(v[0]) + ', "v1":' + str(v[1]) + ', "v2":' + str(v[2]) + ' }'
  print("*MQTT-message: " + msg)
  client1.publish("ouman", msg)

#--------------------------------
# MAIN
#--------------------------------
print("McGurk Ouman MQTT-utility")
print(" Usage parameters: download [filename] or once")
print(" Without any parameters goes to MQTT-loopmode")

ser = serial.Serial(PORT, timeout=2)

send_cmd('time') # b'time\n'
receive_line() # b'Wednesday, 2020-10-21 18:53.58\r\n'

ONCE = False
if len(sys.argv) > 1:
  if str(sys.argv[1]) == 'download':
    download(FILENAME)
  if str(sys.argv[1]) == 'once':
    ONCE = True

f = open(sys.path[0]+"/credentials.txt", "r")
exec(f.read())
f.close()
#print(MQTT_SERVER)
#print(MQTT_PORT)
#print(MQTT_USERNAME)
#print(MQTT_PASSWORD)
#print(MQTT_API_KEY)

flag_connected = 0

#--- ONCE ---

if ONCE:
  v = get_measurements(VERBOSE)
  #print(v)
  ser.close()
  client1 = mqtt.Client("", clean_session=True)
  client1.on_connect = on_connect # callback
  client1.on_publish = on_publish # callback
  client1.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
  client1.connect(MQTT_SERVER, MQTT_PORT) # establish connection
  timeout = 5
  timeout_start = time.time()
  while not flag_connected:
    client1.loop()
    if time.time() > timeout_start + timeout:
      print("*Connect error!")
      sys.exit()
  sendMQTTmsg()
  client1.disconnect()
  sys.exit()

#--- LOOP ---

client1 = mqtt.Client("", clean_session=True)
client1.on_connect = on_connect # callback
client1.on_publish = on_publish # callback
client1.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
lwm = '{ "v0":"NaN", "v1":"NaN", "v2":"NaN" }'
client1.will_set("ouman", lwm)
while not flag_connected:
  try:
    print("*Trying to connect")
    client1.connect(MQTT_SERVER, MQTT_PORT, keepalive=INTERVAL*2+10) # establish connection
  except Exception as e:
    print("*client1.connect() failed")
    print(e)
    time.sleep(5)
    continue
  #time.sleep(2)
  client1.loop_start()
  #time.sleep(2)
  timeout = 5
  timeout_start = time.time()
  while not flag_connected:
    client1.loop()
    if time.time() > timeout_start + timeout:
      print("*Connection timeout error!")
      break
  #    sys.exit()
  #client1.loop()
  #time.sleep(2)
print("*Connected")
#timeout = 5
#timeout_start = time.time()
#while not flag_connected:
#  client1.loop()
#  if time.time() > timeout_start + timeout:
#    print("*Connection timeout error!")
#    sys.exit()

next_reading = time.time()
#client1.loop_start()

try:
  while True:
    v = get_measurements(VERBOSE)
    #print(v)
    #msg = '{ "v0":' + str(v[0]) + ', "v1":' + str(v[1]) + ', "v2":' + str(v[2]) + ' }'
    #print("*MQTT-message: " + msg)
    #client1.publish("ouman", msg)   #publish
    sendMQTTmsg()
    next_reading += INTERVAL
    sleep_time = next_reading-time.time()
    if sleep_time > 0:
      time.sleep(sleep_time)
except KeyboardInterrupt:
  pass

client1.loop_stop()
v[0] = "NaN"
v[1] = "NaN"
v[2] = "NaN"
#v[0] = float("NaN")
#v[1] = float("NaN")
#v[2] = float("NaN")
sendMQTTmsg()
client1.disconnect()
ser.close()

