# raspberry-pi-weather
These scripts are used on a Raspberry Pi Zero W with a Waveshare 2.7" ePaper Hat to display the local weather.
I use it when I get up in the morning to easily see the temperatures and precipitation for the rest of the day.

The weather API is from OpenWeatherMap on their free tier.
The font for displaying weather icons is Meteocons.

The get_weather_data script uses the OWM API to get the current weather conditions in Atlanta.
It displays the current temperature, high and low temperatures for the day, current precipitation, and a general description of the current weather.
It also creates a forecast in 3 hour increments for the next 18 hours. 
It displays only the precipitation for those forecast increments.

The 3 button scripts are for the buttons on the ePaper Hat. The top button displays the weather. The 2nd button clears the display. The 4th button clears the display then shuts down the pi.

Much thanks to Sridhar Rajagopal for his tutorial. It gave me the inspiration and much guidance when setting this up for the first time.
The link for his tutorial is here:
https://www.hackster.io/sridhar-rajagopal/weather-station-with-epaper-and-raspberry-pi-c26a70
