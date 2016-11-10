# pibSmartMirror.py
# -----------------------------------------------------
'''
Pib Smart Mirror Python File

Update Log:
11/2/16: TODO: make getters for ip and weather
''' 

#------------------------------------------------------


#Tkinter is the GUI of Python

from Tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
import feedparser

from PIL import Image, ImageTk
from contextlib import contextmanager

#LOCALE_LOCK = threading.Lock()

ip = '<IP>'			#Stores IP address
ui_locale = ''			
time_format = 12		#12 hour format (normal time)
date_format = "%b %d, %Y" 	#However we want to make the date look
news_country_code = 'us' 	#Searches Google News for US news

weather_api_token = '8029c8320bb5b984c3236cf3f6f79153'  	#darksky.net/dev secret key
weather_lang = 'en' 		#darksky language setting to english
weather_unit = 'us'		#Imperial units returned from darksky
latitude = None			#Needed in darkSky API call, can set from ip address
longitude = None		#Needed in darkSky API call, can set from ip address

xlarge_text_size = 94		#These numbers are just a start, we'll play with them
large_text_size = 48		#once we get the mirror
medium_text_size = 28
small_text_size = 18

#@contextmanager
#def setlocale(name)
#This is for multithreading, which is basically running two programs at once.


