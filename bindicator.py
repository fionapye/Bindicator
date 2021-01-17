#!/usr/bin/python3

import blinkt
import numpy as np
import datetime
import time
import datetime
from time import strptime
import json
import os
import sys
import platform
import requests
import lxml.html



# paths between platforms (webscrape and parsing developed in windows)
def gen_wdir():
    if platform.system() == 'Windows':
        wdir = 'D:\\GitHub\\Bindicator'
    elif platform.system() == 'Linux':
        wdir = '/home/pi/Documents/Bindicator'
    return wdir


# function to read in json data
def read_json (path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


# webscraping
def webscrape(url):
    # webscraping
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    #print("Bin collection data read from website")
    return doc


 # function to test the vaildity of scraped day
def day_validity_test(scr_day):
    days = read_json(os.path.join(gen_wdir(),'config','days.json')) ## added here as test
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
    date = doc.xpath(xpath_value + '/text()') # get the text from the xpath location
    date_str = date[0].split(' ') # split  the text on spaces
    valid_date = day_validity_test(date_str[0]) # test is an allowed value
    if valid_date:
        #print("Valid collection day identified")
        #print(date_str)
        mon = str(strptime(date_str[2],'%b').tm_mon) # turn month into numeric form
        datenum = str(date_str[1]+mon+date_str[3]) # generate numeric date string for conversion
        #print(datenum)  
        binday_date = datetime.datetime.strptime(datenum, "%d%m%Y").date() # convert to datetime format
        info = [date_str[0],binday_date, binday_date.weekday()] # list for ouput
        #print(f'Next {date_str[0]} bin collection date is {binday_date}')
        return info
    else:
        info = [None, None, None]
        #print("No collection day set or unconfigured day abbreviation")
        return info


# function to get the bindays into a list 
def get_bindays():
    xpaths = read_json(os.path.join(gen_wdir(),'config','xpaths.json'))  # load xpaths for webscrape (maybe merge with urlpage?)
    bindays = []
    for type in xpaths:
        data = [type] # get the name into a list
        data.append(info_extract(xpaths.get(type))) # attach data to names
        bindays.append(data) #put all the data together
    return bindays


# get timedate data for today and tomorrow to compare against scraped data
def gen_today_tomorrow():
    today_date = datetime.date.today()
    tomorrow_date = today_date + datetime.timedelta(days = 1)
    return [today_date, tomorrow_date]

#function to get dayname from input date
def get_dayname(date):
    # weekdays as a tuple
    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    return weekdays[date.weekday()]


# function to define which bins to go out today
def bins_out (bindays):
    typeout = []
    for type in bindays:
        #print(type[0])
        #print(type[1][1])
        bintype = type[0]
        binday = type[1][1]
        today_date, tomorrow_date = gen_today_tomorrow()
        if binday: 
            if tomorrow_date == binday:
                data = [bintype,binday]
                typeout.append(data)
                print(f'{bintype.title()} bin(s) to go out today as tomorrow is {get_dayname(tomorrow_date)}')
            else:
                print(f'{bintype.title()} bin(s) don\'t need to go out today as it is {get_dayname(today_date)}')
        else:
            print(f'No data available for the collection of {bintype.title()} bin(s)')
    return typeout


# function to light up leds individually 
def one_led (led,col):
    led_colours = read_json(os.path.join(gen_wdir(),'config','led_colours.json'))  # load colour data (rgb)
    colr = led_colours.get(col)  # get the colour settings from dictionary
    blinkt.set_pixel(led,colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br') )  # insert rgb values and brightness
    blinkt.show()


# function to light up all leds in one colour
def all_led (col):
    led_colours = read_json(os.path.join(gen_wdir(),'config','led_colours.json'))  # load colour data (rgb)
    colr = led_colours.get(col)  # get pixel colour settings from dictionary
    blinkt.set_all(colr.get('r'), colr.get('g'), colr.get('b'), colr.get('br'))  # insert rgb values and brightness
    blinkt.show()  # display leds


# function to turn off all leds
def leds_off():
    blinkt.clear()
    blinkt.show()


# lights for one bin to go out
def one_bindicate(binsout):
    bins = read_json(os.path.join(gen_wdir(),'config','bins.json')) #load bins colour data
    if len(binsout) != 1 : return  # if the len condition not met leave function
    #print('lights')
    blinkt.clear()
    if binsout[0][0] == 'recycling':  # recycling
        for i in range(len(bins.get('recycling'))):
            one_led(i,bins.get('recycling')[i])  # light up colours for recycling
    elif binsout[0][0] == 'general':  # general
        all_led(bins.get('general')[0])  # light up brown for gener
    elif binsout[0][0] == 'green':
        all_led(bins.get('green')[0])
    else:
        print (f'Bin(s) don\'t need to go out today as it is {get_dayname(today_date)}')
        leds_off()

# lights if two bins to go out
def two_bindicate(binsout):
    bins = read_json(os.path.join(gen_wdir(),'config','bins.json')) #load bins colour data
    if len(binsout) != 2 : return  # if the len condition not met leave function
    #print('lights')
    # recycling and general
    if (binsout[0][0] == 'recycling' or binsout[1][0] == 'recycling') and (binsout[0][0] == 'general' or binsout[1][0] == 'general'):
        for i in range(len(bins.get('recycling_general'))):
            one_led(i,bins.get('recycling_general')[i])
    # recycling and green
    elif (binsout[0][0] == 'recycling' or binsout[1][0] == 'recycling') and (binsout[0][0] == 'green' or binsout[1][0] == 'green'):
        for i in range(len(bins.get('recycling_green'))):
            one_led(i,bins.get('recycling_green')[i])
    # general and green
    elif (binsout[0][0] == 'green' or binsout[1][0] == 'green') and (binsout[0][0] == 'general' or binsout[1][0] == 'general'):
        for i in range(len(bins.get('green_general'))):
            one_led(i,bins.get('green_general')[i])

# lights for if three bins to go out
def three_bindicate(binsout):
    bins = read_json(os.path.join(gen_wdir(),'config','bins.json')) #load bins colour data
    if len(binsout) != 3 : return  # if the len condition not met leave function
    #print('lights')
    for i in range(len(bins.get('recyc_green_gen'))):
        one_led(i,bins.get('recyc_green_gen')[i])

# run lights, route based on number required
def bindicate(binsout):
    if len(binsout) == 1:  # if binsout has value 
        one_bindicate(binsout)
    elif len(binsout) == 2:
        two_bindicate(binsout)
    elif len(binsout) == 3:
        three_bindicate(binsout)
    elif len(binsout) == 0:
        #print('no lights')
        leds_off()


#### DEMO - gets stuck, there will be the same issue for a run_bindicator function
def main(run):
    
    #arguments to indicate if demo
    #if len(sys.argv[1]) > 0:
    if run == 'demo':
        #demo stuff that overlaps with run
        print("Bindicate demo")

        today_date, tomorrow_date = gen_today_tomorrow()

        binsout_recy = [['recycling', tomorrow_date]]
        binsout_gen = [['general', tomorrow_date]]
        binsout_green = [['green', tomorrow_date]]
        binsout_two_a = [['recycling', tomorrow_date], ['green', tomorrow_date]]
        binsout_two_b = [['recycling', tomorrow_date], ['general', tomorrow_date]]
        binsout_two_c = [['green', tomorrow_date], ['general', tomorrow_date]]
        binsout_three = [['recycling', tomorrow_date], ['green', tomorrow_date], ['general', tomorrow_date] ]

        bindicate(binsout_recy)
        time.sleep(5)
        bindicate(binsout_gen)
        time.sleep(5)
        bindicate(binsout_green)
        time.sleep(5)
        bindicate(binsout_two_a)
        time.sleep(5)
        bindicate(binsout_two_b)
        time.sleep(5)
        bindicate(binsout_two_c)
        time.sleep(5)
        bindicate(binsout_three)
        time.sleep(5)
        leds_off()
    else:
        #do run stuff that isnt in demo
        print("Live bindicate")
        bindays = get_bindays()
        binsout = bins_out(bindays)
        # light up to show if any bins need to go out
        bindicate(binsout)
        # cleanup
        #time.sleep(900)
        leds_off()


#if __name__ == "__main__":
#    main()

    
###########################
# run demo of lights
#main("demo")
main("real")





