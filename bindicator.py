import blinkt
import numpy as np
import datetime

# weekdays as a tuple
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
binday = "Thursday"
bins_out = "Wednesday"

#display colours
pinkr,pinkg,pinkb = (255,0,140)
bluer,blueg,blueb = (0,145,255)
#greenr,greeng,greenb = (23,146,23)
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
bintype = 1

print(f'The day today is {today_day}')

#if tomorrow_day == binday:
#    print (f'Yes, today is {today_day} and {tomorrow_day} is binday')
#    blinkt.clear()
#    blinkt.set_all(0, 128, 128)
#    blinkt.show()  
#else:
#    print (f'No tomorrow, {tomorrow_day}, is not binday')
#    blinkt.clear()
#    blinkt.show()
    
if tomorrow_day == binday:
    print (f'Yes, today is {today_day} and {tomorrow_day} is binday')
    blinkt.clear()
    if bintype == 0:  # recycling
        blinkt.set_pixel(0,pinkr,pinkg,pinkb)
        blinkt.set_pixel(1,pinkr,pinkg,pinkb)
        blinkt.set_pixel(4,bluer,blueg,blueb)
        blinkt.set_pixel(5,bluer,blueg,blueb)
        blinkt.set_pixel(6,greyr,greyg,greyb)
        blinkt.set_pixel(7,greyr,greyg,greyb)
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