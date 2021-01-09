import blinkt
import numpy as np
import datetime
import time
from bs4 import BeautifulSoup
import urllib.request
import json

# function to read in json data
def read_json (path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

# function to light up leds individually 
def one_led (led,col):
    colr = led_colours.get(col)  # get the colour settings from dictionary
    blinkt.set_pixel(led,colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br') )  # insert rgb values and brightness
    blinkt.show()

# function to light up all leds in one colour
def all_led (col):
    colr = led_colours.get(col)  # get pixel colour settings from dictionary
    blinkt.set_all(colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br'))  # insert rgb values and brightness
    blinkt.show()  # display leds
    
# function to turn off all leds
def leds_off():
    blinkt.clear()
    blinkt.show()


led_colours = read_json('/home/pi/Documents/Bindicator/config/led_colours.json')  # load colour data
days = read_json('/home/pi/Documents/Bindicator/config/days.json')  # load days data
bins = read_json('/home/pi/Documents/Bindicator/config/bins.json')

urlpage = read_json('/home/pi/Documents/Bindicator/urlpath/path.json')  # load url for bin collection
page = urllib.request.urlopen(urlpage.get('urlpath'))
soup = BeautifulSoup(page, 'html.parser')
table = soup.find_all('table', attrs={'class':'multitable'})
table

# weekdays as a tuple
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

# Get days
binday = "Thursday"
bins_out = "Wednesday"

today_date = datetime.date.today()  # get the date of today

today_num = today_date.weekday()  # get the day today

if today_num == 7:
    tomorrow_num = 0
else:
    tomorrow_num = today_num + 1

today_day = weekDays[today_num]
tomorrow_day = weekDays[tomorrow_num]

#remove, for real version
today_day = 'Wednesday'
tomorrow_day = 'Thursday'
bintype = 2

    
if tomorrow_day == binday:
    print (f'Yes, today is {today_day} and {tomorrow_day} is binday')
    blinkt.clear()
    if bintype == 0:  # recycling
        for i in range(len(bins.get('recycling'))):
            one_led(i,bins.get('recycling')[i])  # light up colours for recycling
        #blinkt.show()
    elif bintype == 1:  # general
        all_led(bins.get('general')[0])  # light up brown for gener
    elif bintype == 2:
        all_led(bins.get('green')[0])
else:
    print (f'No tomorrow, {tomorrow_day}, is not binday')
    leds_off()

time.sleep(5)
leds_off()

