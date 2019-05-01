import time

latestGPSData = 0
latestUltraSonicData = [0, 0]


def run():
    print("run")
    for x in range(15):
        print("Sensor", x)
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
    return