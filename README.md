# Ouman_EH-800_USB-serial

Ouman EH-800(B)
- EH-800 includes webserver and ethernet port, EH-800B doesn't
- both includes RJ42-2 and miniUSB
- https://ouman.fi/wp-content/uploads/2018/08/EH-800__manual__fi.pdf#page=
- Atmel AT91SAM7X512 ARM microcontroller
- MP232EC serial interface
- NTC10 temperature sensors: https://www.taloon.com/media/attachments/ouman/huoneanturi_tmr_tekninen_esite.pdf
- power supply: 24V 300mA DC/AC (official power supply is DC)
- about 0.5A with 5V and ZTW-SY-8 step-up-module

Needed packages:
```
sudo apt install git screen python3-pip python3-serial python3-paho-mqtt
sudo pip3 install xmodem
```
Autostartup at bootup:
```
rc.local:
#su - pi -c "screen -d -m watch -n 600 ~/Ouman_EH-800_USB-serial/eh800.py"
su - pi -c "screen -dmS ouman python3 -m forever.run -t 10 python3 -u ~/Ouman_EH-800_USB-serial/eh800.py" 
```
# todo/bug
First run after reset Ouman sends greetings message. This script doesn't handle that right. Second time script works.
Script interpretes `**********************************` as reply to first time-command.

Doesn't try to make connetion again if first try is unsuccessful.

# RJ45-2

Pin | function | notes
--- | --- | ---
1 | GND | -
2 | 24VDC | max 3W
3 | Mittauskanava 6 | Digital input
4 | Mittauskanava 5 | Digital/analog input. If L2 enabled, can be used only for L2 menovesi.
5 | Releohjaus | relay OFF: 5 = not connected (floating), relay ON: 5 = GND (+24V between 5 and 2)
6 | L2 venttiilin ohjaus | Analog output. 0-10V or 2-10V (selectable from menu)
7 | RS232 output | RS232 levels, needs MAX232 or similar
8 | RS232 input | RS232 levels, needs MAX232 or similar

## EXU-800

- https://ouman.fi/wp-content/uploads/2018/08/EXU-800__installation_instructions__fi.pdf
- includes connectors for wires and relay?
- EXU-800 functions are usable straight from RJ45-2 without EXU-800 (excluding EXU-800-relay)

# RS-232 from RJ45-2

- 9600bps without flow control
- sends `AT` and `AT&F`, but I don't know how to reply

# USB-serial (miniUSB)
- miniUSB
- uses LF+CR / 0A+0D / 10+13 / `\n\r` as newline
- help with ? and [enter]
- doesn't echo back
- works with Raspberry Pi
- couldn't get to work with ESP8266/USB-host-shield and Arduino IDE (something to do with CDC/ACM?)
- cannot be used to set most values
- altought only reading values is possible, firmware can be written and time/date can be changed and filesystem can be manipulated. So keep it secure from Internet!

```
**********************************
*          OUMAN EH-800          *
*         command prompt         *
**********************************
```
### COMMAND: ?

<details>
<summary>Show</summary>
        
```
---------------------------------------------
?
        List all commands.
FORMAT
        Format hard drive.
DELETE [FILENAME]
        Delete file.
DOWNLOAD [filename]
        Download file from PC to EH-800.
        Used protocol is XModem with CRC
UPLOAD [filename]
        Upload file from EH-800 to PC.
        Used protocol is XModem with CRC
KEYECHO
        Echo key presses to USB bus.
LIST
        Print names of exist files.
MEASUREMENTS
        Print measurements.
OSINFO
        Print version of operation system.
DEVINFO
        Print information about devices.
RENAME [oldname] [newname]
        Rename file. Oldname to newname.
TYPE [filename]
        Print contents of file.
TIME
        Print date and time.
SET CLOCK [HH] [MM] [SS]
        Set new clock time.
SET DATE [YYYY] [MM] [DD]
        Set new date.
SET DAY [Day Number, 0=Monday...6=Sunday]
        Set new day of week.
FIRMWARE
        Update firmware version.
PTESTER [test number]
        Do tests with production tester.	
```
</details>

### COMMAND: LIST
<details>
<summary>Show</summary>

```
---------------------------------------------
20.10.2020 16:00        objects.dat     3172
19.07.2012 08:16        ea2.bmp         118
19.07.2012 08:16        alertsb.bmp     118
19.07.2012 08:16        curve.bmp       118
19.07.2012 08:16        curve_bg.bmp    972
19.07.2012 08:16        ea.bmp          118
19.07.2012 08:16        ea_bg.bmp       822
19.07.2012 08:16        L1_bg.bmp       1014
19.07.2012 08:16        l1b.bmp         118
19.07.2012 08:16        sch_bg.bmp      1014
19.07.2012 08:16        schedule.bmp    118
19.07.2012 08:16        set_bg.bmp      1254
19.07.2012 08:16        settings.bmp    118
19.07.2012 08:16        alarm_bg.bmp    1014
19.07.2012 08:16        svenska.lng     14465
19.07.2012 08:16        start.bmp       3894
19.07.2012 08:16        rele_bg.bmp     1388
19.07.2012 08:16        rele.bmp        118
19.07.2012 08:16        curve2.bmp      118
19.07.2012 08:16        l2b.bmp         118
19.07.2012 08:17        english.lng     14691
19.07.2012 08:17        russian.lng     24277
19.07.2012 08:17        smallfont.ehf   3504
19.07.2012 08:18        polish.lng      16002
19.07.2012 08:18        eesti.lng       15378
19.07.2012 11:36        alarm.log       563
20.10.2020 15:48        error.log       360
20.10.2020 16:38        trend.log       28822
28.11.2012 11:45        suomi.edt       44
20.10.2020 16:39        trend.otr       1
20.10.2020 16:39        objects.ini     0

31 Files in drive A
Memory usage 13 %
137472 B of 1004288 B
```
</details>

### COMMAND: DEVINFO

<details>
<summary>Show</summary>

```
Device: OUMAN EH-800B  V2.2.2
Serial Number: xxxxxxxx
MAC Address:
Actuator: XHALOMO
Serial Number: xxxxxxxxxxxxxxxxxxxxx
Kohde:
```
</details>

### COMMAND: OSINFO

<details>
<summary>Show</summary>

```
FreeRTOS V5.2.0
Tasks running: 14
```
</details>

### COMMAND: MEASUREMENTS

<details>
<summary>Show</summary>

```
MEASUREMENTS (menovesi 37 ja ulkolämp 1):
34.0 C
0.0 C
0.0 C
3.0 C #ei ainakaan ulkolämpötila tämähetki
0.0 C
0.0 C
36.7 C
0.0 C
36.6 C #menovesi tämähetki? [8]
1.2 C #ulko tämähetki? [9]
1.6 C
0.0 C
0.0 C
0.0 C
8.0 % [14]
8.4 % [15]
0.0 C
0.0 C
39.7 C
15.0 C 
-.5 C #maksimi/minimi tai jokin keskiarvo?
0.0 C
0.0 C
0.0 C
0.0 %
0.0 %
42.2 C
0.0 dig
```
</details>

### COMMAND: TIME
```
Wednesday, 2020-10-21 18:53.58
```

### COMMAND: UPLOAD
```
Start receiving now.
28822 Bytes Transmitted.
```

## Raspberry Pi lsusb

<details>
<summary>Show</summary>

```
pi@raspberrypi:~ $ lsusb -v

Bus 001 Device 007: ID eb03:0920 MakingThings Make Controller Kit
Couldn't open device, some information will be missing
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               1.10
  bDeviceClass            2 Communications
  bDeviceSubClass         0
  bDeviceProtocol         0
  bMaxPacketSize0         8
  idVendor           0xeb03 MakingThings
  idProduct          0x0920 Make Controller Kit
  bcdDevice            1.10
  iManufacturer           1
  iProduct                2
  iSerial                 0
  bNumConfigurations      1
  Configuration Descriptor:
    bLength                 9
    bDescriptorType         2
    wTotalLength       0x0043
    bNumInterfaces          2
    bConfigurationValue     1
    iConfiguration          3
    bmAttributes         0x80
      (Bus Powered)
    MaxPower              100mA
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           1
      bInterfaceClass         2 Communications
      bInterfaceSubClass      2 Abstract (modem)
      bInterfaceProtocol      0
      iInterface              4
      CDC Header:
        bcdCDC               1.10
      CDC ACM:
        bmCapabilities       0x00
      CDC Union:
        bMasterInterface        0
        bSlaveInterface         1
      CDC Call Management:
        bmCapabilities       0x00
        bDataInterface          1
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x83  EP 3 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval             255
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        1
      bAlternateSetting       0
      bNumEndpoints           2
      bInterfaceClass        10 CDC Data
      bInterfaceSubClass      0
      bInterfaceProtocol      0
      iInterface              0
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x01  EP 1 OUT
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0040  1x 64 bytes
        bInterval               0
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x82  EP 2 IN
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0040  1x 64 bytes
        bInterval               0

```
</details>

## Download file manually
- Notice that upload/download is from EH-800B perspective. If you want download file e.g. to your computer, use "upload".
- Notice that downloaded file is always dividable by 128 bytes. If original file is not dividable by 128, 0x1a is padded to end of file.
- Uses Xmodem (-X option) with crc (-c option)
```
sudo apt install screen
screen /dev/ttyACM0 115200
upload trend.log
ctrl-a -> :
exec !! rx -X -c file.log
truncate --size=28822 file.log # trend.log is always 28822 bytes
```

## trend.log
- always 28822 bytes (header 22 bytes. one record 20 bytes, 1440 records (10 days, one record every 600s (10min))
- used for drawing trends at EH-800B display
- check fileformat from eh800.py

## shell snippets
```
~/get:
FILENAME=trend.log
echo "Starting connection..."
screen -d -m -S ouman /dev/ttyACM0 115200
sleep 1
screen -S ouman -X stuff "time^M"
sleep 1
screen -S ouman -X stuff "upload trend.log^M"
sleep 1
screen -S ouman -X exec \!\! rx -X -c $FILENAME
echo "now transfering... "
sleep 5
screen -S ouman -X kill
truncate --size=28822 $FILENAME

~/cmd:
stty -F /dev/ttyACM0 115200 raw -echo
exec 99<>/dev/ttyACM0
printf "measurements\r" >&99
#read answer <&99  # this reads just a CR
#read answer <&99  # this reads the answer OK
exec 99>&-
(usage: ./cmd > test.txt)
```
