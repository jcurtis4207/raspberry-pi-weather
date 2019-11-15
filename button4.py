#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(19, GPIO.FALLING)

subprocess.call(['python3', 'cleardisplay.py'], shell=False)
subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)
