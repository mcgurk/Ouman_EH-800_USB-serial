# Ouman_EH-800_USB-serial
Ouman EH-800 USB serial interface

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

# RS-232

9600bps without flow control. Sends `AT` and `AT&F`, but I don't know how to reply.

# USB-serial (miniUSB)
- miniUSB
- uses LF+CR / 0A+0D / 10+13 / `\n\r` as newline
- help with ? and [enter]
- doesn't echo back
```
**********************************
*          OUMAN EH-800          *
*         command prompt         *
**********************************
```
### ?
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
### LIST
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
### DEVINFO
```
Device: OUMAN EH-800B  V2.2.2
Serial Number: xxxxxxxx
MAC Address:
Actuator: XHALOMO
Serial Number: xxxxxxxxxxxxxxxxxxxxx
Kohde:
```
### OSINFO
```
FreeRTOS V5.2.0
Tasks running: 14
```
### MEASUREMENTS
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
