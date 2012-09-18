import sys
import csv
import time
import ValhallaScientificDPA

# Function for writing to log
def writeToLog(fn,Vab,Vcb,Pa,Pc,header = False):
	f = open(fn,'ab')
	w = csv.writer(f,delimiter=',')
	if header == True:
		w.writerow(["Vab","Vcb","Pa","Pc"])
	else:
		w.writerow([Vab,Vcb,Pa,Pc])
	f.close()
		
# Create file name
fn = "twoWattMeterMethod.csv"

# Write header to log file
writeToLog(fn,"Vab","Vcb","Pa","Pc",True)

# Create instance of VSPDA object for A-phase wattmeter (Pa and Vab)
aPhaseDPA = ValhallaScientificDPA.VSDPA(6,9600)

# Wait before creating second object
time.sleep(1)

# Create instance of VSPDA object for C-phase wattmeter (Pc and Vbc)
cPhaseDPA = ValhallaScientificDPA.VSDPA(4,9600)

# wait before asking for data
time.sleep(1)

# Use try to allow for keyboard interrupt to kill the system
try:
    # Get 300 readings
	for i in range(0,300):
        # Get voltage and power from the meters
		Vcb = aPhaseDPA.getVolts()
		Pc = aPhaseDPA.getWatts()
		Vab = cPhaseDPA.getVolts()
		Pa = cPhaseDPA.getWatts()
        # Print voltage and power readings to the standard output
		msg = "Vab: %0.1f V; Pa: %0.1f W; Vcb: %0.1f V; Pc: %0.1f W\r" % (Vab,Pa,Vcb,Pc)
		sys.stdout.write(msg)
        # Write voltage and power readings to log file
        writeToLog(fn,Vab,Vcb,Pa,Pc)
        # Delay 10th of a second
		time.sleep(0.1)
except KeyboardInterrupt:
    # Close serial port if (ctrl+c) keyboard interrupt received
	aPhaseDPA.closeSerial()
	cPhaseDPA.closeSerial()