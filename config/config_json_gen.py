# colour config
import os
import json

os.chdir("/home/pi/Documents/Bindicator/config")

def write_json (filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

led_colours = {
    "pink" : {"r":255, "g":0, "b":140, "br":0.1},
    "blue" : {"r":0, "g":145, "b":255, "br":0.1},
    "green" : {"r":23, "g":146, "b":5, "br":0.2},
    "grey" : {"r":15, "g":15, "b":15, "br":0.2},
    "brown" : {"r":25, "g":10, "b":1, "br":0.2},
    "black" : {"r":2, "g":0, "b":2, "br":0.2}
    }

bins = {
    "general" : ['brown'],
    "recycling" : ['pink','pink','grey','grey','black','black','blue','blue'],
    "green" : ["green"]
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

write_json('led_colours.json', led_colours)
write_json('days.json', days)
write_json('bins.json', bins)
