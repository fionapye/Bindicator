#!/usr/bin/python3

import blinkt
import datetime
import time
from time import strptime
import json
import os
import sys
import platform
import requests
import lxml.html
import http.client, urllib


# paths between platforms (webscrape and parsing developed in windows)
def gen_wdir():
    if platform.system() == 'Windows':
        wdir = 'D:\\GitHub\\Bindicator'  # working directory for windows
    elif platform.system() == 'Linux':
        wdir = '/home/pi/Documents/Bindicator'  # working directory for linux (rasperian)
    return wdir


# function to read in json data
def read_json (path):
    with open(path) as json_file:
        data = json.load(json_file)  # given a path to a json file, load into dictionary
    return data

# push notifications
def pushover(message):
    notifications = read_json(os.path.join(gen_wdir(),'notifications','tokens.json'))
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
    "token": notifications.get('app'),
    "user": notifications.get('user'),
    "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()


# webscraping
def webscrape(url):
    # webscraping
    html = requests.get(url)  # get the html data from a url
    doc = lxml.html.fromstring(html.content)  
    #print("Bin collection data read from website")
    return doc


 # function to test the vaildity of scraped day
def day_validity_test(scr_day):
    days = read_json(os.path.join(gen_wdir(),'config','days.json'))  # load the days list
    for day in days:
        if days.get(day) == scr_day:  # if the scraped day is in the days data
            test = True
            #print("Valid collection day identified")
            break
        else:
            test = False
            #print("No collection day set or unconfigured day abbreviation")
    return test


# function to parse date data from website
def info_extract(xpath_value):
    urlpage = read_json(os.path.join(gen_wdir(),'urlpath','path.json'))  # load url for bin collection
    doc = webscrape(urlpage.get('urlpath'))  # load url for council website
    date = doc.xpath(xpath_value + '/text()') # get the text from the xpath location given
    date_str = date[0].split(' ') # split  the text on spaces
    valid_date = day_validity_test(date_str[0]) # test is an allowed value
    if valid_date:
        #print("Valid collection day identified")
        #print(date_str)
        mon = str(strptime(date_str[2][:3],"%b").tm_mon) # turn month into numeric form, trim to three digits
        datenum = str(date_str[1]+mon+date_str[3]) # generate numeric date string for conversion
        #print(datenum)  
        binday_date = datetime.datetime.strptime(datenum, "%d%m%Y").date() # convert to datetime format
        info = [date_str[0],binday_date, binday_date.weekday()] # list for ouput
        #print(f'Next {date_str[0]} bin collection date is {binday_date}')
        return info
    else:
        info = [None, None, None]  # if no data found then return empty list
        #print("No collection day set or unconfigured day abbreviation")
        return info


# function to get the bindays into a list 
def get_bindays():
    xpaths = read_json(os.path.join(gen_wdir(),'config','xpaths.json'))  # load xpaths for webscrape (maybe merge with urlpage?)
    bindays = []  # empty list to compile data into
    for type in xpaths:
        print(type)
        data = [type] # get the name into a list
        data.append(info_extract(xpaths.get(type))) # attach data to names
        bindays.append(data) #put all the data together into list
    return bindays


# get timedate data for today and tomorrow to compare against scraped data
def gen_today_tomorrow():
    today_date = datetime.date.today()  # get the date for today
    tomorrow_date = today_date + datetime.timedelta(days = 1)  # get the date for tomorrow by adding a day
    return [today_date, tomorrow_date]


#function to get dayname from input date
def get_dayname(date):
    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")  # weekdays as a tuple to get day name from day number
    return weekdays[date.weekday()]


# function to define which bins to go out today
def bins_out (bindays):
    typeout = []
    for type in bindays:
        #print(type[0])
        #print(type[1][1])
        bintype = type[0]  # from the scraped data, get the bin type
        binday = type[1][1]  # associated bin days
#temp for testing        today_date, tomorrow_date = gen_today_tomorrow()
        today_date, tomorrow_date = gen_today_tomorrow()
        if binday: 
            if tomorrow_date == binday:  # if a bin type will be collected tomorrow
                data = [bintype,binday]
                typeout.append(data)  # append the bin data
                print(f'{bintype.title()} bin(s) to go out today as tomorrow is {get_dayname(tomorrow_date)}')  # user notification
                # send push message
                push_message = f'{bintype.title()} bin(s) to go out today as tomorrow is {get_dayname(tomorrow_date)}'
                pushover(push_message)
            else:
                print(f'{bintype.title()} bin(s) don\'t need to go out today as it is {get_dayname(today_date)}')  # user notification
        else:
            print(f'No data available for the collection of {bintype.title()} bin(s)')  # user notification
    return typeout


# dates for testing 
#today_date = datetime.date(2021,9,15)
#tomorrow_date = datetime.date(2021,9,16)
#bins_out(get_bindays())

# function to light up leds individually 
def one_led (led,col):
    led_colours = read_json(os.path.join(gen_wdir(),'config','led_colours.json'))  # load colour data (rgb)
    colr = led_colours.get(col)  # get the colour settings from dictionary
    blinkt.set_pixel(led,colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br') )  # insert rgb values and brightness
    blinkt.show()  # display the conficgured leds


# function to light up all leds in one colour
def all_led (col):
    led_colours = read_json(os.path.join(gen_wdir(),'config','led_colours.json'))  # load colour data (rgb)
    colr = led_colours.get(col)  # get pixel colour settings from dictionary
    blinkt.set_all(colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br'))  # insert rgb values and brightness
    blinkt.show()   # display the conficgured leds


# function to turn off all leds
def leds_off():
    blinkt.clear()  # clear all led settings 
    blinkt.show()  # display the configuration (no lights in this case)


# lights for one bin to go out
# def one_bindicate(binsout):
#     bins = read_json(os.path.join(gen_wdir(),'config','bins.json')) #load bins colour data
#     if len(binsout) != 1 : return  # if the len condition not met leave function
#     #print('lights')
#     blinkt.clear()  # clear any settings for leds
#     if binsout[0][0] == 'recycling':  # recycling
#         for ind,col in enumerate(bins.get('recycling')):
#             one_led(ind,bins.get('recycling')[ind])  # light up colours for recycling
#     elif binsout[0][0] == 'general':  # general bin
#         all_led(bins.get('general')[0])   # light up colours for general
#     elif binsout[0][0] == 'green':  # green bin
#         all_led(bins.get('green')[0])   # light up colours for green

def one_bindicate(binsout):
    bins = read_json(os.path.join(gen_wdir(),'config','bins.json')) #load bins colour data
    if len(binsout) != 1 : return  # if the len condition not met leave function
    #print('lights')
    blinkt.clear()  # clear any settings for leds
    if binsout[0][0] in bins.keys():
        for ind,col in enumerate(bins.get(binsout[0][0])):
            one_led(ind,bins.get(binsout[0][0])[ind])  # light up colours for recycling
    else:
        print(f'{binsout[0][0]} is an unconfigured type')


# lights if two bins to go out
def two_bindicate(binsout):
    bins = read_json(os.path.join(gen_wdir(),'config','bins.json')) #load bins colour data
    if len(binsout) != 2 : return  # if the len condition not met leave function
    #print('lights')
    # recycling and general
    if (binsout[0][0] == 'recycling' or binsout[1][0] == 'recycling') and (binsout[0][0] == 'general' or binsout[1][0] == 'general'):
        for ind,col in enumerate(bins.get('recycling_general')):
            one_led(ind,bins.get('recycling_general')[ind])  #light up colours for recycling and general
    # recycling and green
    elif (binsout[0][0] == 'recycling' or binsout[1][0] == 'recycling') and (binsout[0][0] == 'green' or binsout[1][0] == 'green'):
        for ind,col in enumerate(bins.get('recycling_green')):
            one_led(ind,bins.get('recycling_green')[ind])   #light up colours for recycling and green
    # general and green
    elif (binsout[0][0] == 'green' or binsout[1][0] == 'green') and (binsout[0][0] == 'general' or binsout[1][0] == 'general'):
        for ind,col in enumerate(bins.get('green_general')):
            one_led(ind,bins.get('green_general')[ind])    #light up colours for green and general

# lights for if three bins to go out
def three_bindicate(binsout):
    bins = read_json(os.path.join(gen_wdir(),'config','bins.json')) #load bins colour data
    if len(binsout) != 3 : return  # if the len condition not met leave function
    #print('lights')
    for ind,col in enumerate(bins.get('recyc_green_gen')):
        one_led(ind,bins.get('recyc_green_gen')[ind])  #   #light up colours for recycling, green and general

# run lights, route based on number required
def bindicate(binsout):
    if len(binsout) == 1:  # if binsout has one bin type
        one_bindicate(binsout)
    elif len(binsout) == 2: # if binsout has two bin types
        two_bindicate(binsout)
    elif len(binsout) == 3: # if binsout has three bin types
        three_bindicate(binsout)
    elif len(binsout) == 0:
        #print (f'Bin(s) don\'t need to go out today as it is {get_dayname(gen_today_tomorrow()[0])}')  # user notification
        leds_off()



#### main function to run the process
def main():
    
    if len(sys.argv) == 1:
        #do run stuff that isnt in demo
        print("Live bindicate")  # user notification
        bindays = get_bindays()  # get the bindays
        binsout = bins_out(bindays)  # get the data for bins to go out
        # light up to show if any bins need to go out
        bindicate(binsout)  # light up for any bins to go out today
        # cleanup
        time.sleep(900)  # stay lit for 15 mins
        leds_off()  # turn the leds off
        
    #arguments to indicate if demo
    elif len(sys.argv) == 2 and sys.argv[1] == "demo": # if the terminal is given the demo instruction run this 
        #demo stuff that overlaps with run
        print("Bindicate demo")

        tomorrow_date = gen_today_tomorrow()[1]  # generate day data

        # Data for demo
        binsout_recy = [['recycling', tomorrow_date]]
        binsout_gen = [['general', tomorrow_date]]
        binsout_green = [['green', tomorrow_date]]
        binsout_two_a = [['recycling', tomorrow_date], ['green', tomorrow_date]]
        binsout_two_b = [['recycling', tomorrow_date], ['general', tomorrow_date]]
        binsout_two_c = [['green', tomorrow_date], ['general', tomorrow_date]]
        binsout_three = [['recycling', tomorrow_date], ['green', tomorrow_date], ['general', tomorrow_date] ]

        print("Colour code for recycling")
        bindicate(binsout_recy)
        time.sleep(5)
        
        print("Colour code for general")
        bindicate(binsout_gen)
        time.sleep(5)
        
        print("Colour code for recycling")
        bindicate(binsout_green)
        time.sleep(5)
        
        print("Colour code for recycling and green")
        bindicate(binsout_two_a)
        time.sleep(5)
        
        print("Colour code for recycling and general")
        bindicate(binsout_two_b)
        time.sleep(5)
        
        print("Colour code for green and general")
        bindicate(binsout_two_c)
        time.sleep(5)
        
        print("Colour code for recycling, green and general")
        bindicate(binsout_three)
        time.sleep(5)
        leds_off()
    else:
        print("Unknown command for bindicator")
        


# run the bindicator
if __name__ == '__main__':
    main()


