#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
sys.path.append(r'lib')
import epd2in7b
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

def cleardisplay():
    try:
        epd = epd2in7b.EPD()
        epd.init()
        print("Clear...")
        epd.Clear()

        epd.sleep()
        return

    except :
        print ('traceback.format_exc():\n%s',traceback.format_exc())
        exit()

if __name__ == '__main__':
	cleardisplay()
