import time
import RPi.GPIO

latestGPSData = 0
latestUltraSonicData = [0, 0]

UltraSonicA_Trig = 11
UltraSonicA_Echo = 12
UltraSonicB_Trig = 15
UltraSonicB_Echo = 16

def run():
    print("run")
    sensorLoop()



def sensorLoop():
    print("Sensor Loop")
    gpsDataRetrieval()
    ultraSonicDataRetrieval()
    time.sleep(1)
    return


def gpsDataRetrieval():
    print("GPS Data")
    return


def ultraSonicDataRetrieval():
    print("US Data")
    GPIO.output(UltraSonicA_Trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(UltraSonicA_Trig, GPIO.LOW)

    while GPIO.input(UltraSonicA_Echo) == 0:
        pulse_start_time = time.time()
    while GPIO.input(UltraSonicA_Echo) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distanceA = round(pulse_duration * 17150, 2)

    GPIO.output(UltraSonicB_Trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(UltraSonicB_Trig, GPIO.LOW)

    while GPIO.input(UltraSonicB_Echo) == 0:
        pulse_start_time = time.time()
    while GPIO.input(UltraSonicB_Echo) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distanceB = round(pulse_duration * 17150, 2)

    print("A:", distanceA, "B:", distanceB)
    return distanceA, distanceB
