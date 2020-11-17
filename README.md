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
- Help with ? and [enter]
```
**********************************
*          OUMAN EH-800          *
*         command prompt         *
**********************************
```
? and [enter]:
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
