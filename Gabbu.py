import time
import RPi.GPIO as GPIO
import threading
import numpy as np


M1=35 #11
M2=36 #15
M3=37 #16
M4=38 #18

PIN_TRIGGER_A = 7
PIN_ECHO_A = 11
PIN_TRIGGER_B = 31
PIN_ECHO_B = 29

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_TRIGGER_A, GPIO.OUT)
GPIO.setup(PIN_ECHO_A, GPIO.IN)
GPIO.setup(PIN_TRIGGER_B, GPIO.OUT)
GPIO.setup(PIN_ECHO_B, GPIO.IN)
#GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
GPIO.output(PIN_TRIGGER_B, GPIO.LOW)

numberOfDistanceReadingsToTake = 3

lock = threading.Lock()
latestDistance = []

global getGPSData
global getLatestDistances


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


def ultraSonicDataRetrieval():
	#print("Waiting for sensor to settle")
	#time.sleep(0.2)
    #print("Calculating distance")

    totalDistanceA = 0
    totalDistanceB = 0

    for i in range(numberOfDistanceReadingsToTake):
        #print ("Obtaining distance", i)
        GPIO.output(PIN_TRIGGER_A, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
        while GPIO.input(PIN_ECHO_A) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO_A) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time

        distanceA = round(pulse_duration * 17150, 2)

        print("Distance A:", distanceA, "cm")

        GPIO.output(PIN_TRIGGER_B, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER_B, GPIO.LOW)
        while GPIO.input(PIN_ECHO_B) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO_B) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time

        distanceB = round(pulse_duration * 17150, 2)
        print("Distance B:", distanceB, "cm")

        totalDistanceA += distanceA
        totalDistanceB += distanceB

    averageA = totalDistanceA / numberOfDistanceReadingsToTake
    averageB = totalDistanceB / numberOfDistanceReadingsToTake

    print "A average:", averageA, "B Average", averageB
    return averageA, averageB


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
	# GPIO.cleanup()


def step_forward():
	init_pin()
	print('forward')
	GPIO.output(M1, False)
	GPIO.output(M2, True)
	GPIO.output(M3, False)
	GPIO.output(M4, True)
	time.sleep(3)
	GPIO.cleanup()


def step_backward():
	init_pin()
	print('reverse')
	GPIO.output(M1, True)
	GPIO.output(M2, False)
	GPIO.output(M3, True)
	GPIO.output(M4, False)
	time.sleep(3)
	GPIO.cleanup()

def step_right():
	init_pin()
	print('right')
	GPIO.output(M1, False)
	GPIO.output(M2, False)
	GPIO.output(M3, False)
	GPIO.output(M4, True)
	time.sleep(3)
	GPIO.cleanup()


def step_left():
	init_pin()
	print('left')
	GPIO.output(M1, False)
	GPIO.output(M2, True)
	GPIO.output(M3, False)
	GPIO.output(M4, False)
	time.sleep(3)
	GPIO.cleanup()

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


 

run()
