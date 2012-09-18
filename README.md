##Valhalla Scientific Digital Power Analyzer##

###Introduction and Purpose###
The purpose of this library is to provide an easy method for retreiving voltage and power information from the Valhalla Scientific Digital Power Analyzers used in electrical engineering laboratories at the University of Illinois at Urbana-Champaign (UIUC).  The code has been tested to work with the 2100 and 2111 model power analyzers.  It should be noted the aforementioned meters did not come a serial port originally, rather they were retrofitted with custom hardware; thus, this software is only verified to work with the meters at the UIUC and will likely be unusable by anyone else.  The purpose of providing the code here is to make it accessible to everyone, particularly those who are from UIUC and wish to utilize the serial functionality of the meters.

###Using the Library###

####Initialization####
Like any other Python library, you must first import the ValhallaScientificDPA library as follows (note that [pyserial](http://pyserial.sourceforge.net/) must be installed on your computer.
````python
import ValhallaScientificDPA
````

Once imported, to begin collecting data from a meter, simply create an instance of the VSDPA object.  The constructor has 3 arguments, all of which are optional.  The first parameter is the port number (see below for more information), the second is the baud rate, and the third is an instance of the lock paramter to be used with the multiprocessing library.  The following example creates an instance of the VSPDA object called myDPA which utilizes serial port 3 (COM4) at a baud rate of 9600.
````python
myDPA = ValhallaScientificDPA.VSDPA(3,9600)
````

As mentioned above, all parameters for the constructor are optional.  
* The port number defaults to None, which will lead to the user being prompted for a port number.  Note that the code is setup to work on Windows devices, thus the port number corresponds to (n-1) where n is the number following the word "COMn", e.g., COM7 corresponds to port 6.
* If the baud rate is omitted, it will be defaulted to 9600.  There should never be a reason to change this as the hardware in the meters is only capable of communicating at 9600 baud.
* The third parameter, lock, takes a default value of None.  As mentioend above, the lock is only useful if the [multiprocessing library](http://docs.python.org/library/multiprocessing.html#synchronization-between-processes) is used.  In this case, the lock is used so that the ValhallaScientificDPA can print to the standard out without interfering with other processes.

####Reading Voltage and Power####
Once you've created an instance of the VSPDA object, reading voltage and power from the meter is a simple function call away.  Examples which utilize the above-created instance (myDPA) of both are given below.
````python
# Read voltage
voltage = myDPA.getVolts()
# Read power
power = myDPA.getWatts()
````

###Notes on Functionality###
* The VSDPA class is a superclass of the Serial object found in the [pyserial](http://pyserial.sourceforge.net/) library.  Thus, as mentioned in the introduction, you must have pyserial installed.
* There is a limit to the speed with which you can request information from the meter.  Based upon initial usage, it seems that the fastest period that information can be retreived is ~0.1 seconds.  Also note that the microcontroller which reads the data from the meters and sends it out the serial port can only perform one task at once, and the priority is servicing the serial port.  Thus, too many attempts to get data from the DPA may result in stale data being sent back.
* For those that are curious, but too lazy to read the code, the commands to receive voltage and power are as follows (both in ascii). Voltage: VOLTS?\r and Power: WATTS?\r
