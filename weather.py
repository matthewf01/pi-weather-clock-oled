#!/usr/bin/env python
#weather script

import json
import time
import math
import RPi.GPIO as GPIO
import datetime
import os
from decimal import getcontext, Decimal
#set decimal precision used for printing temperature
getcontext().prec = 2

#imports modules for 128x64 OLED
#import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
#OLED setup
RST=24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
# Get display width and height.
width = disp.width
height = disp.height
# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))
# Load a font font.
fontsize=16
font = ImageFont.truetype('fonts/Roboto-Thin.ttf', fontsize)
#font = ImageFont.load_default()
# Create drawing object.
draw = ImageDraw.Draw(image)

#set paths to files
working_dir="/home/pi/pi-weather-clock-oled/"
weather_conditions_json="weatherconditions.json"
#weather_forecast_json="weatherforecast.json"
conditions_api_file = working_dir + weather_conditions_json
#forecast_api_file = working_dir + weather_forecast_json

def LCD_clear():
  disp.clear()
  draw.rectangle((0,0,width,height), outline=0, fill=0)

def LCD_write():
  disp.image(image)
  disp.display()

def LCD_text(message,x,y):
  draw.text((x,y),message,font=font,fill=255)
  
def LCD_time():
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	fontsize=22
	font = ImageFont.truetype('fonts/Roboto-Thin.ttf', fontsize)
	draw.text((0,0),(datetime.datetime.now().strftime('%I:%M %p')),font=font,fill=255)
	fontsize=17
	font = ImageFont.truetype('fonts/Roboto-Thin.ttf', fontsize)
	draw.text((3,21),(datetime.datetime.now().strftime('%a, %b %d')),font=font,fill=255)
	LCD_text(tempf+(chr(176))+"F",93,10)
	LCD_text(weather,0,45)
	LCD_write()
	
#JSON parsing
def read_json_conditions():
  json_cond_text = open(conditions_api_file)
  parsed_cond_json = json.load(json_cond_text)
  global weather
  global tempf
  global weatherdisplay
  weather = parsed_cond_json['current_observation']['weather']
  temp_raw = str(parsed_cond_json['current_observation']['temp_f'])
  tempf = str(Decimal(temp_raw)/Decimal(1))
  obs_time=str(parsed_cond_json['current_observation']['observation_time'])
  weatherdisplay=("{}{}F, {}".format(tempf,chr(176),weather))
  #for character LCD:
  #weatherdisplay=("{}, {}{}F".format(weather,tempf,chr(223)))
  timenow = time.strftime("%X")
  datenow = time.strftime("%x")
  print("{} {} READ FILE: {}".format(timenow,datenow,conditions_api_file))
  print("{} -- {}`F -- {}".format(weather,tempf,obs_time))
  global weather_aging
  weather_aging=0
  return

#####################################################

#initialize everything
print("initializing...")
LCD_clear()
LCD_write()
LCD_text("Checking weather...",0,20)
LCD_write()
read_json_conditions()
weather_aging_refresh=60 #how many S to re-read the weather JSON file. JSON file pulled in a configurable interval in get-weather-json.py
weather_aging=weather_aging_refresh -2

def main():
 while (True):
 # Main program block
  global weather_aging
  weather_aging=weather_aging + 1
  if weather_aging > weather_aging_refresh:
   read_json_conditions()
   LCD_clear()
   LCD_text(weather,0,0)
   LCD_text(weatherdisplay,0,60)
   LCD_write()
   break
  else:
   LCD_time()
   time.sleep(1)


#if __name__ == '__main__':

while (True):
 main()

#####################################################


