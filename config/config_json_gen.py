# colour config
import os
import json
import platform

# paths between platforms
if platform.system() == 'Windows':
    wdir = 'D:\\GitHub\\Bindicator'
elif platform.system() == 'Linux':
    wdir = '/home/pi/Documents/Bindicator'


os.chdir(os.path.join(wdir,'config'))
#os.chdir("/home/pi/Documents/Bindicator/config")

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
    "green" : ["green"],
    "recycling_general" : ['pink','grey','black','blue','brown','brown','brown','brown'],
    "recycling_green" : ['pink','grey','black','blue','green','green','green','green'],
    "green_general" : ['brown','brown','brown','brown','green','green','green','green'],
    "recyc_green_gen" : ['pink','grey','black','blue','brown','brown','green','green']
    }

days = {
    "Monday" : 'Mon',
    "Tuesday" : 'Tues',
    "Wednesday" : 'Wed',
    "Thursday" : 'Thurs',
    "Friday" : 'Fri',
    "Saturday" : 'Sat',
    "Sunday" : 'Sun'
    }

xpaths ={
    'recycling' : '/html/body/div[2]/div/div/form/table/tbody/tr[1]/td[1]/div',
    'green' : '/html/body/div[2]/div/div/form/table/tbody/tr[2]/td[1]/div',
    'general' : '/html/body/div[2]/div/div/form/table/tbody/tr[3]/td[1]/div'
}

write_json('led_colours.json', led_colours)
write_json('days.json', days)
write_json('bins.json', bins)
write_json('xpaths.json', xpaths)