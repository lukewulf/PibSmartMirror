

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

LOCALE_LOCK = threading.Lock()

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
xsmall_text_size = 12

@contextmanager
def setlocale(name):
	#This is for multithreading, which is basically running two programs at once.
	with LOCALE_LOCK:
		saved = locale.setlocale(locale.LC_ALL)
		try:
			yield locale.setlocale(locale.LC_ALL, name)
		finally:
			locale.setlocale(locale.LC_ALL, saved)


class Clock(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg='black')

		self.time1 = ''
		self.timeLabel = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
		self.timeLabel.pack(side=TOP, anchor=E)

		self.day_of_week1 = ''
		self.dowLabel = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
		self.dowLabel.pack(side=TOP, anchor=E)

		self.date1 = ''
		self.dateLabel = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
		self.dateLabel.pack(side=TOP, anchor=E)
		self.tick()

	def tick(self):
		with setlocale(ui_locale):				#This is a line for multithreading
			if time_format == 12:
				time2 = time.strftime('%I:%M %p')	#HH:MM am/pm time string
			else:
				time2 = time.strftime('%H:%M')		#HH:MM 24hr time

			day_of_week2 = time.strftime('%A')		#Name of the day of the week
			date2 = time.strftime(date_format)		#MM/DD/YYYY date format

			#updating time and date so its current
			if time2 != self.time1:
				self.time1 = time2
				self.timeLabel.config(text=time2)

			if day_of_week2 != self.day_of_week1:
				self.day_of_week1 = day_of_week2
				self.dowLabel.config(text=day_of_week2)

			if date2 != self.date1:
				self.date1 = date2
				self.dateLabel.config(text=date2)
			
			#dateDisplay = "It is %s on a %s.  The date is: %s\n" % (self.time1, self.day_of_week1, self.date1)
			#print(dateDisplay)
			
			self.timeLabel.after(200, self.tick)

#----------------------Weather Class--------------------------------

class Weather(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg="black")
		self.temperature = ''
		self.forecast = ''
		self.location = ''
		self.currently = ''
		self.icon = ''
		self.degreeFrame = Frame(self,bg="black")
		self.degreeFrame.pack(side=TOP, anchor = W)
		self.temperatureLabel = Label(self.degreeFrame, font=('Helvetica', xlarge_text_size), fg="white",  bg="black")
		self.temperatureLabel.pack(side=LEFT, anchor = N)
		self.iconLabel = Label(self.degreeFrame, bg="black")
		self.iconLabel.pack(side=LEFT, anchor=N, padx = 20)

		self.currentlyLabel = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
		self.currentlyLabel.pack(side=TOP, anchor=W)

		self.forecastLabel = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
		self.forecastLabel.pack(side=TOP, anchor=W)

		self.locationLabel = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
		self.locationLabel.pack(side=TOP, anchor=W)

		self.get_weather()		
	
	#Gets your ip if you did not enter it as a global variable
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
				#Grabbing your latitude and longitude based off the ip address
				location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
				req = requests.get(location_req_url)
				location_obj = json.loads(req.text)

				lat = location_obj['latitude']
				lon = location_obj['longitude']
				#print("Your latitude is: %f\n" % lat)
				#print("Your longitude is: %f\n" % lon)

				location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

				weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat, lon, weather_lang, weather_unit)

			else:
				location2 = ""
				weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)
			#print("the weather url is: ")
			#print(weather_req_url)
			#print("\n")

			#Grabbing the weather to your current location
			r = requests.get(weather_req_url)
			weather_obj = json.loads(r.text)

			degree_sign = u'\N{DEGREE SIGN}'
			temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
			currently2 = weather_obj['currently']['summary']
			forecast2 = weather_obj['hourly']['summary']
			#temperature2 = "%s" % (str(int(weather_obj['currently']['temperature'])))		
			icon_id = weather_obj['currently']['icon']
			icon2 = None

			if self.temperature != temperature2:
				self.temperature = temperature2
				self.temperatureLabel.config(text=temperature2)
	
			if self.currently != currently2:
				self.currently = currently2
				self.currentlyLabel.config(text=currently2)

			if self.forecast != forecast2:
				self.forecast = forecast2
				self.forecastLabel.config(text=forecast2)
		
			if self.location != location2:
				if location2 == ", ":
					self.location = "Cannot Pinpoint Location"
					self.locationLabel.config(text="Cannot Pinpoint Location")
				else:
					self.location = location2
					self.locationLabel.config(text=location2)

			#print("It is %s outside\n" % temperature2)
			#print("It is %s degrees outside\n" % temperature)
			#print("The weather is %s \n" % currently2)
			#print("In the future it will be %s \n" % forecast2)
			#print("The icon id is: %s\n" % icon_id)
		except Exception as e:
			traceback.print_exc()
			print "Error: %s. Cannot get weather" % e

		self.after(1200000, self.get_weather)

#----------------------News Classes---------------------------------

class News(Frame):
	def __init__(self, parent, *args, **kwargs):

		#initializing the parent constructor to make News a frame
		Frame.__init__(self, parent, *args, **kwargs)
		
		self.config(bg='black')
		
		self.title = 'Today\'s Headlines'
		self.newsLabel1 = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
		self.newsLabel1.pack(side=TOP, anchor=W)
		self.headlinesContainer = Frame(self,bg="black")
		self.headlinesContainer.pack(side=TOP)
		self.get_headlines()
		
	
	def get_headlines(self):
		
		#Removes all pre-existing news headlines so that you don't have two headlines overlapping		
		for widget in self.headlinesContainer.winfo_children():
			widget.destroy()

		#If you don't have an api token you cannot get news
		if news_api_token == None:
			print("please enter a news api token from newsapi.org")
			return
		#There are 50+ news sources from newsapi.org, our program default is google news
		if news_provider == None:
			news_source = 'google-news'
			news_req_url = "https://newsapi.org/v1/articles?source=%s&apiKey=%s" % (news_source, news_api_token)
		else:
			news_req_url = "https://newsapi.org/v1/articles?source=%s&apiKey=%s" % (news_provider, news_api_token)
		#print("Your news req url is: " +news_req_url + "\n")
		r = requests.get(news_req_url)
		news_obj = json.loads(r.text)

		headline1 = news_obj['articles'][0]['title']
		headline2 = news_obj['articles'][1]['title']
		headline3 = news_obj['articles'][2]['title']

		headlineGUI1 = NewsHeadline(self.headlinesContainer, headline1)
		headlineGUI1.pack(side = TOP, anchor = W)

		headlineGUI2 = NewsHeadline(self.headlinesContainer, headline2)
		headlineGUI2.pack(side = TOP, anchor = W)

		headlineGUI3 = NewsHeadline(self.headlinesContainer, headline3)
		headlineGUI3.pack(side = TOP, anchor = W)

		self.after(600000, self.get_headlines)

		#print("%s\n" % headline1)
		#print("%s\n" % headline2)
		#print("%s\n" % headline3)

class NewsHeadline(Frame):
	def __init__(self, parent, title=""):
		Frame.__init__(self, parent, bg='black')

		#Could have an image of a news icon
		self.title = title
		self.titleLabel = Label(self, text=self.title, font=('Helvetic', xsmall_text_size), fg="white", bg="black")
		self.titleLabel.pack(side=LEFT, anchor=N)

#-------------------Holder for all the GUI elements --------------------------
class DisplayWindow:
	def __init__(self):
		self.tk = Tk()
		self.tk.configure(background = 'black')
		self.topFrame = Frame(self.tk, background = 'black')
		self.bottomFrame = Frame(self.tk, background = 'black')
		self.topFrame.pack(side = TOP, fill = BOTH, expand = YES)
		self.bottomFrame.pack(side = BOTTOM, fill = BOTH, expand = YES)
		self.state = False
		self.tk.bind("<Return>", self.toggle_fullscreen)
		self.tk.bind("<Escape>", self.end_fullscreen)

		#Clock module
		self.clock = Clock(self.topFrame)
		self.clock.pack(side = RIGHT, anchor = N, padx = 100, pady = 60)

		#Weather
		self.weather = Weather(self.topFrame)
		self.weather.pack(side = LEFT, anchor = N, padx = 100, pady = 60)

		#News
		self.news = News(self.bottomFrame)
		self.news.pack(side=LEFT, anchor=S, padx = 100, pady = 60)

	def toggle_fullscreen(self, event=None):
		self.state = not self.state
		self.tk.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.tk.attributes("-fullscreen", self.state)
		return "break"	

if __name__ == '__main__':
	w = DisplayWindow()
	w.tk.mainloop()


#myWeather = Weather()
#myWeather.get_weather()
#myNews = News()
#myNews.get_headlines()
#myClock = Clock()
#myClock.tick()
