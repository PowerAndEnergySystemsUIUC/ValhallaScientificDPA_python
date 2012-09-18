import serial
import operator
import sys
import itertools
import time
import _winreg as winreg

class VSDPA(serial.Serial):
	def __init__(self, port = None, baud = 9600, l = None):
		self.__l = l
		if(port == None):
			port = self.promptForPort()
		if(baud == None):
			baud = self.promptForBaud()
		serial.Serial.__init__(self,int(port),long(baud),timeout=1)
		time.sleep(1)
		
	def printStdOut(self, msg, quiet = False):
		if self.__l != None:
			self.__l.acquire()
		if quiet == False:
			print msg
		if self.__l != None:
			self.__l.release()
		
	def promptForPort(self):
		self.printStdOut("Serial ports available:")
		numPorts = self.scanSerial()
		port = raw_input("Select a serial port number: ")
		if port == "q":
			sys.exit()
		elif (int(port) < 0):
			self.printStdOut("Invalid port selected. Try again (or enter q to quit).")
			return self.promptForPort()
		else:
			port = port.strip()
			return port

	def promptForBaud(self):
		availableBaud = ['9600']
		self.printStdOut("Baud rates available:")
		for b in availableBaud:
			self.printStdOut(b)
		baud = raw_input("Select a baud rate: ")
		if baud == "q":
			sys.exit()
		elif not baud in availableBaud:
			self.printStdOut("Inavlid baud rate. Try again (or enter q to quit).")
			return self.promptForBaud()
		else:
			return baud

	def scanSerial(self):
		path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
		key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
		for i in itertools.count():
			try:
				val = winreg.EnumValue(key, i)
				portName = str(val[1])
				self.printStdOut(str(int(portName[-1])-1) + ": " + portName)
			except EnvironmentError:
				break
		return i-1
        
	def closeSerial(self):
		self.printStdOut("Attempting to disconnect serial connection...") 
		try:
			self.close()
			if(self.isOpen()):
				self.printStdOut("Unable to close serial port.")
			else:
				self.printStdOut("Serial closed successfully.")
				return True
		except AttributeError:
			self.printStdOut("Serial connection never opened.") 
		return False
		
	def getWatts(self):
		return self.__readValue('WATTS')
		
	def getVolts(self):
		return self.__readValue('VOLTS')

	def __readValue(self,command):
		command += '?' + chr(0x0D)	# add question mark and carriage return
		try:
			if(self.isOpen()):
				self.write(command)
				line = self.readline()
				value = 0
				if len(line) == 7:
					for i in range(0,4):		# do for four values to left of decimal
						value = value*10 + int(line[i])
					value += float(line[5])/10	# add decimal
				return value
			else:
				self.printStdOut("Serial connection not open")
		except serial.SerialException:
			return 0
		except AttributeError:
			self.printStdOut("Serial connection never opened.")
		return False