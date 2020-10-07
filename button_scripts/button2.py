#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	GPIO.wait_for_edge(6, GPIO.FALLING)
	subprocess.call(['python3', '/home/pi/screen_scripts/cleardisplay.py'], shell=False)

