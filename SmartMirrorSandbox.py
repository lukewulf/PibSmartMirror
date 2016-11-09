

#Tkinter is the GUI of Python

from Tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
#import feedparser

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

news_api_token = '3e330242de994dd28074ba838a73a80b'
news_provider = 'google-news'   #newsapi.org possible source: there's 50+ different news sources

xlarge_text_size = 94		#These numbers are just a start, we'll play with them
large_text_size = 48		#once we get the mirror
medium_text_size = 28
small_text_size = 18

#@contextmanager
#def setlocale(name)
#This is for multithreading, which is basically running two programs at once.

class Weather(object):
	def __init__(self):
		self.temperature = ''
		self.forecase = ''
		self.location = ''
		self.currently = ''
		self.icon = ''

	def get_ip(self):
		try:
			ip_url = "https://jsonip.com/"
			req = requests.get(ip_url)
			ip_json = json.loads(req.text)
			return ip_json['ip']
		except Exception as e:
			traceback.print_exc()
			return "Error: %s. Cannot get ip." % e

	def get_weather(self):
		try:
			if latitude is None and longitude is None:
				location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
				req = requests.get(location_req_url)
				location_obj = json.loads(req.text)

				lat = location_obj['latitude']
				lon = location_obj['longitude']
				print("Your latitude is: %f\n" % lat)
				print("Your longitude is: %f\n" % lon)

				location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

				weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat, lon, weather_lang, weather_unit)

			else:
				location2 = ""
				weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)
			print("the weather url is: ")
			print(weather_req_url)
			print("\n")
			r = requests.get(weather_req_url)
			weather_obj = json.loads(r.text)

			degree_sign = u'\N{DEGREE SIGN}'
			temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
			currently2 = weather_obj['currently']['summary']
			forecast2 = weather_obj['hourly']['summary']
		
			icon_id = weather_obj['currently']['icon']
			icon2 = None

			#print("It is %s outside\n" % temperature2)
			print("The weather is %s \n" % currently2)
			print("In the future it will be %s \n" % forecast2)
			print("The icon id is: %s\n" % icon_id)
		except Exception as e:
			traceback.print_exc()
			print "Error: %s. Cannot get weather" % e

class News(object):
	def __init__(self):
		self.title = 'News'
		
	
	def get_headlines(self):
		if news_api_token == None:
			print("please enter a news api token from newsapi.org")
			return
		if news_provider == None:
			news_source = 'google-news'
			news_req_url = "https://newsapi.org/v1/articles?source=%s&apiKey=%s" % (news_source, news_api_token)
		else:
			news_req_url = "https://newsapi.org/v1/articles?source=%s&apiKey=%s" % (news_provider, news_api_token)
		print("Your news req url is: " +news_req_url + "\n")
		r = requests.get(news_req_url)
		news_obj = json.loads(r.text)

		headline1 = news_obj['articles'][0]['title']
		headline2 = news_obj['articles'][1]['title']
		headline3 = news_obj['articles'][2]['title']

		print("%s\n" % headline1)
		print("%s\n" % headline2)
		print("%s\n" % headline3)
	
myWeather = Weather()
myWeather.get_weather()
myNews = News()
myNews.get_headlines()
