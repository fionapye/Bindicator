import blinkt
import numpy as np
import datetime
import time
from bs4 import BeautifulSoup
import urllib.request
import json

def read_json (path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def one_led (led,col):
    colr = led_colours.get(col)
#    blinkt.clear()
    blinkt.set_pixel(led,colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br') )
#    blinkt.show()

def all_led (col):
    colr = led_colours.get(col)
#    blinkt.clear()
    blinkt.set_all(colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br'))
    blinkt.show()

led_colours = read_json('/home/pi/Documents/Bindicator/config/led_colours.json')
days = read_json('/home/pi/Documents/Bindicator/config/days.json')


urlpage = read_json('/home/pi/Documents/Bindicator/urlpath/path.json')
page = urllib.request.urlopen(urlpage.get('urlpath'))
soup = BeautifulSoup(page, 'html.parser')
table = soup.find_all('table', attrs={'class':'multitable'})
table

# weekdays as a tuple
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
recycling = ['pink','pink','grey','grey','black','black','blue','blue']

# Get days
binday = "Thursday"
bins_out = "Wednesday"

today_date = datetime.date.today()

today_num = today_date.weekday()

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
        for i in range(len(recycling)):
            one_led(i,recycling[i])
        blinkt.show()
    elif bintype == 1:  # general
        all_led('brown')
    elif bintype == 2:
        all_led('green')
else:
    print (f'No tomorrow, {tomorrow_day}, is not binday')
    blinkt.clear()
    blinkt.show()

time.sleep(5)
blinkt.clear()
blinkt.show()

