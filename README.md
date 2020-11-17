# Ouman_EH-800_USB-serial
Ouman EH-800 USB serial interface

# RJ45-2

Pin | function | notes
--- | --- | ---
1 | GND | -
2 | 24VDC | - 
3 | Mittauskanava 6 | Digital input
4 | Mittauskanava 5 | Digital/analog input. If L2 enabled, can be used only for L2 menovesi.
5 | Releohjaus | relay OFF: 5 = not connected (floating), relay ON: 5 = GND (+24V between 5 and 2)
6 | L2 venttiilin ohjaus | 0-10V or 2-10V (selectable from menu)
7 | RS232 output | RS232 levels, needs MAX232 or similar
8 | RS232 input | RS232 levels, needs MAX232 or similar

# RS-232

9600bps without flow control. Sends `AT` and `AT&F`, but I don't know how to reply.
