import blinkt
import numpy as np
import datetime
import time
import datetime
from time import strptime
import json
import os
import platform
import requests
import lxml.html

# paths between platforms
if platform.system() == 'Windows':
    wdir = 'D:\\GitHub\\Bindicator'
elif platform.system() == 'Linux':
    wdir = '/home/pi/Documents/Bindicator'

# function to read in json data
def read_json (path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

 # function to test the vaildity of scraped day
def day_validity_test(scr_day):
    for day in days:
        if days.get(day) == scr_day:  # if the scraped day is in the days data
            test = True
            break
        else:
            test = False
    return test


# function to parse date data from xpath
def info_extract(xpath_value):
    date = doc.xpath(xpath_value + '/text()') # get the text from the xpath location
    date_str = date[0].split(' ') # split  the text on spaces
    valid_date = day_validity_test(date_str[0])
    if valid_date:
        print(date_str)
        mon = str(strptime(date_str[2],'%b').tm_mon) # turn month into numeric form
        datenum = str(date_str[1]+mon+date_str[3]) # generate numeric date string for conversion
        print(datenum)  
        binday_date = datetime.datetime.strptime(datenum, "%d%m%Y").date() # convert to datetime format
        info = [date_str[0],binday_date, binday_date.weekday()] # list for ouput
        return info
    else:
        info = [None, None, None]
        return info

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

# load data

led_colours = read_json(os.path.join(wdir,'config','led_colours.json'))  # load colour data
days = read_json(os.path.join(wdir,'config','days.json')) 
bins = read_json(os.path.join(wdir,'config','bins.json'))
urlpage = read_json(os.path.join(wdir,'urlpath','path.json'))  # load url for bin collection

#led_colours = read_json('/home/pi/Documents/Bindicator/config/led_colours.json')  # load colour data
#days = read_json('/home/pi/Documents/Bindicator/config/days.json')  # load days data
#bins = read_json('/home/pi/Documents/Bindicator/config/bins.json')
#urlpage = read_json('/home/pi/Documents/Bindicator/urlpath/path.json')  # load url for bin collection

# webscraping
html = requests.get(urlpage.get('urlpath'))
doc = lxml.html.fromstring(html.content)

xpaths ={
    'recycling' : '/html/body/div[2]/div/div/form/table/tbody/tr[1]/td[1]/div',
    'green' : '/html/body/div[2]/div/div/form/table/tbody/tr[2]/td[1]/div',
    'general' : '/html/body/div[2]/div/div/form/table/tbody/tr[3]/td[1]/div'
}

for type in xpaths:
    print(type)
    dayabr, date, weekday = info_extract(xpaths.get(type))

dayabr, date, weekday = info_extract(xpaths.get('green'))

if x == True:
    print('yes')
# weekdays as a tuple
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

# Get days
binday = "Thursday"
bins_out = "Wednesday"

today_date = datetime.date.today()  # get the date of today

today_num = today_date.weekday()  # get the day today

if today_num == 6:
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

