import time
import RPi.GPIO as GPIO
import threading

PIN_TRIGGER_A = 7
PIN_ECHO_A = 11
PIN_TRIGGER_B = 31
PIN_ECHO_B = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_TRIGGER_A, GPIO.OUT)
GPIO.setup(PIN_ECHO_A, GPIO.IN)
GPIO.setup(PIN_TRIGGER_B, GPIO.OUT)
GPIO.setup(PIN_ECHO_B, GPIO.IN)
GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
GPIO.output(PIN_TRIGGER_B, GPIO.LOW)

numberOfDistanceReadingsToTake = 3

lock = threading.Lock()
latestDistance = []

global getGPSData
global getLatestDistances


def run():
    print("run")
    sensorLoop()


def sensorLoop():
    print("Sensor Loop")
    gpsDataRetrieval()
    ultraSonicDataRetrieval()
    return


def gpsDataRetrieval():
    print("GPS Data")
    return


def ultraSonicDataRetrieval():
    print("Waiting for sensor to settle")
    time.sleep(0.2)
    print("Calculating distance")

    totalDistanceA = 0
    totalDistanceB = 0

    for i in range(numberOfDistanceReadingsToTake):
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

    return averageA, averageB


def getGPSData():
    return


def setUpdatedDistances(newDistances):
    global latestDistance
    with lock:
        latestDistance = newDistances


def getLatestDistances():
    return latestDistance
