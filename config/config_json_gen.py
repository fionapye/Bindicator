# colour config


import os
import json

os.chdir("/home/pi/Documents/Bindicator/config")

led_colours = {
    "pink" : {"r":255, "g":0, "b":140, "br":0.1},
    "blue" : {"r":0, "g":145, "b":255, "br":0.1},
    "green" : {"r":23, "g":146, "b":5, "br":0.2},
    "grey" : {"r":15, "g":15, "b":15, "br":0.2},
    "brown" : {"r":25, "g":10, "b":1, "br":0.2},
    "black" : {"r":2, "g":0, "b":2, "br":0.2}
    }

days = {
    "Monday" : 'Mon',
    "Tuesday" : 'Tue',
    "Wednesday" : 'Wed',
    "Thursday" : 'Thur',
    "Friday" : 'Fri',
    "Saturday" : 'Sat',
    "Sunday" : 'Sun'
    }

with open('led_colours.json', 'w') as outfile:
    json.dump(led_colours, outfile)

with open('days.json', 'w') as outfile:
    json.dump(days,outfile)

