#!/usr/bin/python
import RPi.GPIO as GPIO
import time

servoPin =15
servoPin2 =16
PIN_TRIGGER_A = 7
PIN_ECHO_A = 11
PIN_TRIGGER_B = 31
PIN_ECHO_B = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin,GPIO.OUT)
GPIO.setup(servoPin2,GPIO.OUT)
GPIO.setup(PIN_TRIGGER_A, GPIO.OUT)
GPIO.setup(PIN_ECHO_A, GPIO.IN)
GPIO.setup(PIN_TRIGGER_B, GPIO.OUT)
GPIO.setup(PIN_ECHO_B, GPIO.IN)
GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
GPIO.output(PIN_TRIGGER_B, GPIO.LOW)

p = GPIO.PWM(servoPin,60)
p2 = GPIO.PWM(servoPin2, 60)
p2.start(7.5)
p.start(7.5)


try:
	while True:
		p.ChangeDutyCycle(7.5)
		p2.ChangeDutyCycle(7.5)
		time.sleep(1)
		p.ChangeDutyCycle(12.5)
		p2.ChangeDutyCycle(12.5)
		time.sleep(1)
		p.ChangeDutyCycle(2.5)
		p2.ChangeDutyCycle(2.5)
		time.sleep(1)		
		print "Waiting for sensor to settle"
		time.sleep(2)
		print "Calculating distance"
		GPIO.output(PIN_TRIGGER_A, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(PIN_TRIGGER_A, GPIO.LOW)
		while GPIO.input(PIN_ECHO_A)==0:
				pulse_start_time = time.time()
		while GPIO.input(PIN_ECHO_A)==1:
				pulse_end_time = time.time()
		pulse_duration = pulse_end_time - pulse_start_time
		distanceA = round(pulse_duration * 17150, 2)
		print "Distance A:",distanceA,"cm"
		GPIO.output(PIN_TRIGGER_B, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(PIN_TRIGGER_B, GPIO.LOW)
		while GPIO.input(PIN_ECHO_B)==0:
				pulse_start_time = time.time()
		while GPIO.input(PIN_ECHO_B)==1:
				pulse_end_time = time.time()
		pulse_duration = pulse_end_time - pulse_start_time
		distanceB = round(pulse_duration * 17150, 2)
		print "Distance B:",distanceB,"cm"
	
	
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()

