import blinkt
import numpy as np
import datetime
import time
from bs4 import BeautifulSoup
import urllib.request


## Data Setup
#Webscrape
urlpage = 
page = urllib.request.urlopen(urlpage)
soup = BeautifulSoup(page, 'html.parser')

table = soup.find_all('table', attrs={'class':'multitable'})
print('Number of results', len(table))
table

# weekdays as a tuple
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

# Get days
binday = "Thursday"
bins_out = "Wednesday"

#bin colours
#display colours
pinkr,pinkg,pinkb,pinkbr = (255,0,140,0.2)
bluer,blueg,blueb, bluebr = (0,145,255,0.2)
blackr,blackg,blackb = (2,0,2)
greenr,greeng,greenb = (23,146,5)
greyr,greyg,greyb = (15,15,15)
brownr,browng,brownb = (25,10,1)

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
bintype = 0

print(f'The day today is {today_day}')

    
if tomorrow_day == binday:
    print (f'Yes, today is {today_day} and {tomorrow_day} is binday')
    blinkt.clear()
    if bintype == 0:  # recycling
        blinkt.set_pixel(0,pinkr,pinkg,pinkb, brightness = pinkbr)
        blinkt.set_pixel(1,pinkr,pinkg,pinkb, brightness = pinkbr)
        blinkt.set_pixel(4,blackr,blackg,blackb)
        blinkt.set_pixel(5,blackr,blackg,blackb)
        blinkt.set_pixel(6,bluer,blueg,blueb, brightness = bluebr)
        blinkt.set_pixel(7,bluer,blueg,blueb, brightness = bluebr)
        blinkt.set_pixel(2,greyr,greyg,greyb)
        blinkt.set_pixel(3,greyr,greyg,greyb)
        blinkt.show()
    elif bintype == 1:  # general
        blinkt.set_all(brownr,browng,brownb)
        blinkt.show()
    elif bintype == 2:
        blinkt.set_all(greenr,greeng,greenb)
        blinkt.show()
else:
    print (f'No tomorrow, {tomorrow_day}, is not binday')
    blinkt.clear()
    blinkt.show()

time.sleep(5)
blinkt.clear()
blinkt.show()

    