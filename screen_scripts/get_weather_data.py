#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
sys.path.append('/home/pi/lib')

import signal
import epd2in7
import epdconfig
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from cleardisplay import cleardisplay
import pyowm

owm = pyowm.OWM('6247512f91aa075a475215fc436d6ec2')

city_id = 4180439 # Atlanta, GA, USA

# Map weather code from OWM to meteocon icons
weather_icon_dict = {200 : "6", 201 : "6", 202 : "6", 210 : "6", 211 : "6", 212 : "6", 
                     221 : "6", 230 : "6" , 231 : "6", 232 : "6", 

                     300 : "7", 301 : "7", 302 : "8", 310 : "7", 311 : "8", 312 : "8",
                     313 : "8", 314 : "8", 321 : "8", 
 
                     500 : "7", 501 : "7", 502 : "8", 503 : "8", 504 : "8", 511 : "8", 
                     520 : "7", 521 : "7", 522 : "8", 531 : "8",

                     600 : "V", 601 : "V", 602 : "W", 611 : "X", 612 : "X", 613 : "X",
                     615 : "V", 616 : "V", 620 : "V", 621 : "W", 622 : "W", 

                     701 : "M", 711 : "M", 721 : "M", 731 : "M", 741 : "M", 751 : "M",
                     761 : "M", 762 : "M", 771 : "M", 781 : "M", 

                     800 : "1", 

                     801 : "H", 802 : "N", 803 : "N", 804 : "Y"
}

# Main function
    
def main():
    epd = epd2in7.EPD()

    # Get Weather data from OWM
    obs = owm.weather_at_id(city_id)
    location = obs.get_location().get_name()
    weather = obs.get_weather()
    reftime = weather.get_reference_time()
    description = weather.get_detailed_status()
    temperature = weather.get_temperature(unit='fahrenheit')

    #Create 12 hour forecast
    fc = owm.three_hours_forecast('Atlanta,us')
    f = fc.get_forecast()
    lst = f.get_weathers()
    forecast_times = []
    forecast_stats = []
    for i in range(5):
        index = time.strftime('%I%p', time.localtime(lst[i].get_reference_time()))
        if index[0] == "0":
            index = index[1:]    #removes leading 0
        forecast_times.append(index.lower())
        status = lst[i].get_status()
        if(status == "Rain") or (status == "Thunderstorm"):
            forecast_stats.append("Rain")
        elif status == "Drizzle":
            forecast_stats.append("Drizzle")
        elif status == "Snow":
            forecast_stats.append("Snow")
        else:
            forecast_stats.append("  ----")

    # Print weather details to console
    print("location: " + location)
    print("weather: " + str(weather))
    print("description: " + description)
    print("temperature: " + str(temperature))
    for i in range(5):
        print("{}: {}".format(forecast_times[i], forecast_stats[i]))

    # Display Weather Information on e-Paper Display
    try:
        epd.init()

        # Drawing on the Horizontal image
        HBlackimage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 298*126

        print("Drawing")
        drawblack = ImageDraw.Draw(HBlackimage)
        font60 = ImageFont.truetype('fonts/arial.ttf', 60)
        font30 = ImageFont.truetype('fonts/arial.ttf', 30)
        font24 = ImageFont.truetype('fonts/arial.ttf', 24)
        font16 = ImageFont.truetype('fonts/arial.ttf', 16)
        font20 = ImageFont.truetype('fonts/arial.ttf', 20)
        fontweather = ImageFont.truetype('fonts/meteocons-webfont.ttf', 30)
        fontweatherbig = ImageFont.truetype('fonts/meteocons-webfont.ttf', 60)

        w1, h1 = font24.getsize(location)
        w2, h2 = font30.getsize(description)
        w3, h3 = fontweatherbig.getsize(weather_icon_dict[weather.get_weather_code()])

        #Top: Location, Description, Icon
        drawblack.text((10, 0), location, font = font24, fill = 0)
        drawblack.text((10, 25), description, font = font30, fill = 0)
        drawblack.text((264 - w3 - 1, 0), weather_icon_dict[weather.get_weather_code()], font = fontweatherbig, fill = 0)
        drawblack.text((10, 60), "Currently : " + time.strftime( '%I:%M %p', time.localtime(reftime)), font = font16, fill = 0)

        #Temperatures
        tempstr = str("{0}{1}F".format(int(round(temperature['temp'])), u'\u00b0'))
        print( tempstr)
        w4, h4 = font24.getsize(tempstr)
        drawblack.text((10, 115), tempstr, font = font60, fill = 0)
        drawblack.text((150, 130), str("{0}{1} | {2}{3}".format(int(round(temperature['temp_max'])), u'\u00b0', int(round(temperature['temp_min'])), u'\u00b0')), font = font30, fill = 0)

        #Precipitation Forecast
        drawblack.text((10, 80), "{}\n{}".format(forecast_times[0], forecast_stats[0]), font = font16, fill = 0)
        drawblack.text((60, 80), "{}\n{}".format(forecast_times[1], forecast_stats[1]), font = font16, fill = 0)
        drawblack.text((110, 80), "{}\n{}".format(forecast_times[2], forecast_stats[2]), font = font16, fill = 0)
        drawblack.text((160, 80), "{}\n{}".format(forecast_times[3], forecast_stats[3]), font = font16, fill = 0)
        drawblack.text((210, 80), "{}\n{}".format(forecast_times[4], forecast_stats[4]), font = font16, fill = 0)

        epd.display(epd.getbuffer(HBlackimage))
        time.sleep(2)

        epd.sleep()

    except IOError as e:
        print ('traceback.format_exc():\n%s',traceback.format_exc())
        epdconfig.module_init()
        epdconfig.module_exit()
        exit()

    # Wait 10 minutes, then clear screen
    time.sleep(600)
    cleardisplay()

# gracefully exit without a big exception message if possible
def ctrl_c_handler(signal, frame):
    print('Goodbye!')
    epdconfig.module_init()
    epdconfig.module_exit()
    exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

if __name__ == '__main__':
    main()
