#!/bin/bash
python3 /home/pi/button_scripts/button1.py &
python3 /home/pi/button_scripts/button2.py &
python3 /home/pi/button_scripts/button4.py &

# starts at boot due to cron @reboot
