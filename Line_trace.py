#!/usr/bin/python

import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from neopixel import *
from TRSensors import TRSensor
import time

Button = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button,GPIO.IN,GPIO.PUD_UP)

# LED strip configuration:
LED_COUNT      = 4     
LED_PIN        = 18     
LED_FREQ_HZ    = 800000  
LED_DMA        = 5      
LED_BRIGHTNESS = 255   
LED_INVERT     = False   
maximum = 50;
j = 0
integral = 0;
last_proportional = 0

TR = TRSensor()
Ab = AlphaBot2()
Ab.stop()
print("Line follow")
time.sleep(0.5)
for i in range(0,100):
	if(i<25 or i>= 75):
		Ab.right()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	else:
		Ab.left()
		Ab.setPWMA(30)
		Ab.setPWMB(30)
	TR.calibrate()
Ab.stop()
print(TR.calibratedMin)
print(TR.calibratedMax)
while (GPIO.input(Button) != 0):
	position,Sensors = TR.readLine()
	print(position,Sensors)
	time.sleep(0.05)
Ab.forward()

while True:
	position,Sensors = TR.readLine()
	
	if(Sensors[0] >900 and Sensors[1] >900 and Sensors[2] >900 and Sensors[3] >900 and Sensors[4] >900):
		Ab.setPWMA(0)
		Ab.setPWMB(0);
	else:
	
		proportional = position - 2000
		
		
		derivative = proportional - last_proportional
		integral += proportional
		
		
		last_proportional = proportional

		
		power_difference = proportional/30  + integral/10000 + derivative*2;  

		if (power_difference > maximum):
			power_difference = maximum
		if (power_difference < - maximum):
			power_difference = - maximum
		print(position,power_difference)
		if (power_difference < 0):
			Ab.setPWMA(maximum + power_difference)
			Ab.setPWMB(maximum);
		else:
			Ab.setPWMA(maximum);
			Ab.setPWMB(maximum - power_difference)
		
	for i in range(0,strip.numPixels()):
		strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255))
	strip.show();
	j += 1
	if(j > 256*4): 
		j= 0
