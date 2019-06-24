import time
import RPi.GPIO as GPIO
from bluetooth import *
import threading
import numpy as np
import serial


M1=35 #11
M2=36 #15
M3=37 #16
M4=38 #18

PIN_TRIGGER_A = 7
PIN_ECHO_A = 11
PIN_TRIGGER_B = 31
PIN_ECHO_B = 29

servoPin =15
servoPin2 =16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin,GPIO.OUT)
GPIO.setup(servoPin2,GPIO.OUT)
GPIO.setup(PIN_TRIGGER_A, GPIO.OUT)
GPIO.setup(PIN_ECHO_A, GPIO.IN)
GPIO.setup(PIN_TRIGGER_B, GPIO.OUT)
GPIO.setup(PIN_ECHO_B, GPIO.IN)
#GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
GPIO.output(PIN_TRIGGER_B, GPIO.LOW)

p = GPIO.PWM(servoPin,60)
p2 = GPIO.PWM(servoPin2, 60)
p2.start(7.5)
p.start(7.5)


numberOfDistanceReadingsToTake = 3
ser = serial.Serial('/dev/ttyACM0', 9600)

lock = threading.Lock()
latestDistance = []

global getGPSData
global getLatestDistances
current_position = [34, 34]


def run():
	print("run")
	#sensorLoop()
	run_obstacle_avoidance()
	

def sensorLoop():
	print("Sensor Loop")
	gpsDataRetrieval()
	ultraSonicDataRetrieval()
	return


def gpsDataRetrieval():
	print("GPS Data")
	return


def ultrasonicA():
	#print("Waiting for sensor to settle")
	#time.sleep(0.2)
    #print("Calculating distance")
	GPIO.output(PIN_TRIGGER_A, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
	pulse_end_time = 0
	while GPIO.input(PIN_ECHO_A)==0:
		pulse_start_time = time.time()
	while GPIO.input(PIN_ECHO_A)==1:
		pulse_end_time = time.time()
	pulse_duration = pulse_end_time - pulse_start_time
	distanceA = round(pulse_duration * 17150, 2)
	print "Distance A:",distanceA,"cm"
	return distanceA
	

def ultrasonicB():
	#print("Waiting for sensor to settle")
	#time.sleep(0.2)
    #print("Calculating distance")
	GPIO.output(PIN_TRIGGER_B, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(PIN_TRIGGER_B, GPIO.LOW)
	pulse_end_time = 0
	while GPIO.input(PIN_ECHO_B)==0:
		pulse_start_time = time.time()
	while GPIO.input(PIN_ECHO_B)==1:
		pulse_end_time = time.time()
	pulse_duration = pulse_end_time - pulse_start_time
	distanceB = round(pulse_duration * 17150, 2)
	print "Distance B:",distanceB,"cm"
	return distanceB
	


def getGPSData():
	return


def setUpdatedDistances(newDistances):
	global latestDistance
	with lock:
		latestDistance = newDistances


def getLatestDistances():
	return latestDistance


# init pin
def init_pin():

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(M1, GPIO.OUT)
	GPIO.setup(M2, GPIO.OUT)
	GPIO.setup(M3, GPIO.OUT)
	GPIO.setup(M4, GPIO.OUT)

# motor movements and powers
def stop():
	init_pin()
	print('stop')
	GPIO.output(M1, False)
	GPIO.output(M2, False)
	GPIO.output(M3, False)
	GPIO.output(M4, False)
	time.sleep(3)
	


def step_forward():
	init_pin()
	print('forward')
	GPIO.output(M1, False)
	GPIO.output(M2, True)
	GPIO.output(M3, False)
	GPIO.output(M4, True)
	time.sleep(3)
	


def step_backward():
	init_pin()
	print('reverse')
	GPIO.output(M1, True)
	GPIO.output(M2, False)
	GPIO.output(M3, True)
	GPIO.output(M4, False)
	time.sleep(3)
	

def step_right():
	init_pin()
	print('right')
	GPIO.output(M1, False)
	GPIO.output(M2, False)
	GPIO.output(M3, False)
	GPIO.output(M4, True)
	time.sleep(3)
	


def step_left():
	init_pin()
	print('left')
	GPIO.output(M1, False)
	GPIO.output(M2, True)
	GPIO.output(M3, False)
	GPIO.output(M4, False)
	time.sleep(3)
	

# these methods rotate the wheels depending on the count by for looping
def move_forward(count=1 ):
	for i in range(count):
		step_forward()
		stop()

def move_backward(count=1 ):
	for i in range(count):
		step_backward()
		stop()

def move_right(count=1):
	for i in range(count):
		step_right()
		stop()

def move_left(count=1):

	for i in range(count):
		step_left()
		stop()

def run_obstacle_avoidance():
	while True:
		# the count is the amount of times the wheels should spin... we should base that on the whether the robot has reached its target or not

		#gets the two distances read from ur sensors
		dist1, dist2 = ultraSonicDataRetrieval()

		#picks the smallest one
		mindist = min(dist1, dist2)

		# if that distance is bigger than 10 move forward
		if mindist > 10:
			move_forward(count=1)

		#otherwise pick a random turn , turn and repeat the process
		else:
			if np.random.ranf() > 0.5:
				move_left(count=1)


			else:
				move_right(count=1)
				
				# provide more condition for better maneuvering preferably using the gps location


def random_movement():
	# niccekjaw il minimum jekk hu inqas minn 10 takitvetja boolean u jigi u jekk tkun true tidhol forloop
	
	#for x in range(3):
	while True:
		print("getting distace from A")
		distanceA=ultrasonicA()
		print("getting distace from B")
		distanceB=ultrasonicB()
		mindist = min(distanceA, distanceB)
		print("mindist is", mindist)
		if mindist>10:
			print("moving foward")
			move_forward(count=1)
		else:
			print("moving left")
			move_left(count=1)
		

def gps_movement():
	# niccekjaw il minimum jekk hu inqas minn 10 takitvetja boolean u jigi u jekk tkun true tidhol forloop
	#(Lan, Lon)...find the difference
	target_positon = [35, 32]
	previous_position = [34, 33]
	previous_distance = 4
	
	#call bluetooth app to get the target position
	target_position = getCommuicationData()
	
	if (ser.isOpen()):
		newData = ser.readline()
		parseLocatonUpdate(newData)
	
	targetReached = 0
	if(targetReached == 0):
		stop()
	else:
		while True:
			distanceA=ultrasonicA()
			distanceB=ultrasonicB()
			mindist = min(distanceA, distanceB)
			print(mindist)
			if mindist>10:
				move_forward(count=1)
				#this could be extreamly inefficient if the target it slightly to the right of the robot
				if(distanceBetween(current_position, target_position) > previous_distance):
					move_left(count=2) # what ever is enough for a 20 degree left turn
			else:
				move_left(count=1)


#def parseLocatonUpdate(newData):
#	if 'LAT' in newData:
#		# update lat
#		splitData = newData.split(" ")
#		current_position = [splitData[2], current_position[0]

#	if 'LNG' in newData:
		# update lng
#		splitData = newData.split(" ")
#		current_position = [current_position[0], splitData[2]


#def distanceBetween(pos1, pos2):
#	difference_lat = pos1[0] - pos2[0]
#	difference_lng = pos1[1] - pos2[1]
#	distance = Math.sqrt((difference_lat * difference_lat) + (difference_lng * difference_lng))
#	return distance

def getCommuicationData():
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service(server_sock, "RPiServer",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE], )

    while True:
        print("Wating for RFCOMM connection")

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        try:
            # client_ock has no attribute 'rcv'
            gpsData = client_sock.recv(1024)
            if len(gpsData) == 0:
                print("GPS data is empty")
                break
            else:
                print("GPS data received ", gpsData)
                return gpsData
                # 35.545454, 34.3434343
                # call 2nd class to handle gpsData

        except IOError:
            pass
        except KeyboardInterrupt:
            print("Keyboard interrupt")

            client_sock.close()
            server_sock.close()

            print("All done")
            break
    return
		
def servo_rotate():
	p.ChangeDutyCycle(7.5)
	p2.ChangeDutyCycle(7.5)
	time.sleep(1)
	p.ChangeDutyCycle(12.5)
	p2.ChangeDutyCycle(12.5)
	time.sleep(1)


servo_rotate()
