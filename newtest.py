import RPi.GPIO as gpio
import time


M1=35 #11
M2=36 #15
M3=37 #16
M4=38 #18



def init():

 gpio.setmode(gpio.BOARD)
 gpio.setup(M1, gpio.OUT)
 gpio.setup(M2, gpio.OUT)
 gpio.setup(M3, gpio.OUT)
 gpio.setup(M4, gpio.OUT)

def forward(sec):
 init()
 print('forward')
 gpio.output(M1, False)
 gpio.output(M2, True)
 gpio.output(M3, False) 
 gpio.output(M4, True)
 time.sleep(sec)
 gpio.cleanup()

def reverse(sec):
 init()
 print('reverse')
 gpio.output(M1, True)
 gpio.output(M2, False)
 gpio.output(M3, True) 
 gpio.output(M4, False)
 time.sleep(sec)
 gpio.cleanup()
 
def right(sec):
 init()
 print('right')
 gpio.output(M1, False)
 gpio.output(M2, False)
 gpio.output(M3, False) 
 gpio.output(M4, True)
 time.sleep(sec)
 gpio.cleanup() 
 
def left(sec):
 init()
 print('left')
 gpio.output(M1, False)
 gpio.output(M2, True)
 gpio.output(M3, False) 
 gpio.output(M4, False)
 time.sleep(sec)
 gpio.cleanup()  

#forward(0.05)
#reverse(0.15)
#left(0.05)
right(0.05)
