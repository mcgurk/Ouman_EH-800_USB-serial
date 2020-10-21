#!/usr/bin/env python3

# sudo apt install python3-pip python3-serial
# (sudo apt install python3-matplotlib)
# sudo pip3 install xmodem

PORT = '/dev/ttyACM0'
FILENAME = 'trend.log'

import sys, time, serial
from xmodem import XMODEM
import matplotlib.pyplot as plt
#import numpy as np

#ser = serial.Serial(PORT, timeout=0) # or whatever port you need
ser = serial.Serial(PORT, timeout=2)

def getc(size, timeout=1):
  return ser.read(size) or None

def putc(data, timeout=1):
  return ser.write(data)  # note that this ignores the timeout

def send_cmd(cmd):
  ser.write(bytes(cmd, 'ASCII') + b'\n')
  print('cmd: ' + cmd)

def receive_line(verbose = True):
  line = ser.readline().decode("ASCII").rstrip("\r\n")
  if verbose:
    print('reply: ' + line) # b'Start receiving now.\r\n'
  return line

def download(filename):
  modem = XMODEM(getc, putc)
  cmd = 'upload ' + filename
  send_cmd(cmd) # b'upload trend.log\n'
  receive_line() # b'Start receiving now.\r\n'
  stream = open(FILENAME, 'wb')
  print('LOG: Start receiving (XMODEM-CRC)')
  ser.flushInput()
  modem.recv(stream, crc_mode=1)
  line = receive_line() # b'28822 Bytes Transmitted.\r\n'
  size = int(line.split()[0])
  stream.truncate(size)
  stream.close()
  print('LOG: downloaded ' + filename + ' (' + str(size) + ' bytes)')
  return size

def read_measurement(v):
  line = receive_line(False)
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
    print(values)
  print('Menovesi: ' + str(values[8]))
  print('Ulkoilma: ' + str(values[9]))
  print('Venttiili: ' + str(values[14]))


#send_cmd('time') # b'time\n'
#receive_line() # b'Wednesday, 2020-10-21 18:53.58\r\n'

if len(sys.argv) > 1:
  if str(sys.argv[1]) == 'download':
    download(FILENAME)

#get_measurements()

#00000000: 9d00 a005 1400 0200 0300 0400 0500 0900  ................
#00000010: 0800 1001 3201 1737 8f5f 0200 8c01 f1d8  ....2..7._......
#00000020: f1d8 f1d8 0000 0500 0000 2029 8f5f 0200  .......... )._..
#00000030: 8a01 f1d8 f1d8 f1d8 0000 0400 0000 782b  ..............x+
#00000040: 8f5f 0100 7901 f1d8 f1d8 f1d8 0000 0000  ._..y...........
#00000050: 0000 d02d 8f5f 0000 6d01 f1d8 f1d8 f1d8  ...-._..m.......
#00000060: 0000 0400 0000 2830 8f5f 0000 7a01 f1d8  ......(0._..z...
#00000070: f1d8 f1d8 0000 0900 0000 8032 8f5f 0000  ...........2._..
#00000080: 8201 f1d8 f1d8 f1d8 0000 0700 0000 d834  ...............4

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
#print(date)
#print(ulko)
#print(meno)
#print(vent)
#print(values)
file.close()

for x in range(samples):
#for x in range(100):
#  x1.append(x)
  epoch = values[x][0]
  x1.append(time.strftime('%H:%M', time.gmtime(epoch)))

#print(x1)
#plt.plot(x1, y1)
total = 160
plt.plot(x1[0:total], y1[0:total])
plt.xlabel('Aika')
plt.ylabel('°C')
plt.title('Menovesi')

#fig, ax = plt.subplots()
#width = np.diff(x1).min()
#ax.bar(x1, y1, align='center', width=width)
#ax.xaxis_date()
#fig.autofmt_xdate()

#x_ticks = [0, 16, 5]
x_ticks = x1[:total:20]
plt.xticks(x_ticks)

#plt.axhline(y=5,color='gray')
plt.grid()

plt.show()

ser.close()
