import SensorThread
import BluetoothCommunicationThread
import threading
import time
import RPi.GPIO as GPIO

servoPin = 15
servoPin2 = 16

M1=35 #11
M2=36 #15
M3=37 #16
M4=38 #18


GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(servoPin2, GPIO.OUT)

p = GPIO.PWM(servoPin, 60)
p2 = GPIO.PWM(servoPin2, 60)

p2.start(7.5)
p.start(7.5)

try:
    sensorThread = threading.Thread(target=SensorThread.run)
    bluetoothThread = threading.Thread(target=BluetoothCommunicationThread.run)

    sensorThread.daemon = True
    bluetoothThread.daemon = True

    sensorThread.start()
    bluetoothThread.start()


    
except:
    print("Error starting threads")


def startNavigation():
    # make threads have qs so that functions can be called in them
    return


def moveServos(moveAmmount):
    p.ChangeDutyCycle(moveAmmount)
    p2.ChangeDutyCycle(moveAmmount)


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(M1, GPIO.OUT)
    GPIO.setup(M2, GPIO.OUT)
    GPIO.setup(M3, GPIO.OUT)
    GPIO.setup(M4, GPIO.OUT)


def moveForward(time):
    init()
    print('forward')
    GPIO.output(M1, False)
    GPIO.output(M2, True)
    GPIO.output(M3, False)
    GPIO.output(M4, True)
    time.sleep(time)
    GPIO.cleanup()


def reverse(time):
    init()
    print('reverse')
    GPIO.output(M1, True)
    GPIO.output(M2, False)
    GPIO.output(M3, True)
    GPIO.output(M4, False)
    time.sleep(time)
    GPIO.cleanup()


def right(time):
    init()
    print('right')
    GPIO.output(M1, False)
    GPIO.output(M2, False)
    GPIO.output(M3, False)
    GPIO.output(M4, True)
    time.sleep(time)
    GPIO.cleanup()


def left(time):
    init()
    print('left')
    GPIO.output(M1, False)
    GPIO.output(M2, True)
    GPIO.output(M3, False)
    GPIO.output(M4, False)
    time.sleep(time)
    GPIO.cleanup()

