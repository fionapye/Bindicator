Bindicator Project

(B)indicates via rgb LEDs which bins are due for collection by checking the council website

Inspired by https://twitter.com/tarbard/status/1002464120447397888?lang=en

Folders:

* urlpath - for storing the URL to where bin collection data is located. This is inside gitignore as it contains address data. Add your own folder and json with url to use.
* config - folder for config files : json generator py file creates - rgb values for light colours, bin colours, days of the week as named on council wesbite, xpaths for data retrival. This data is all read in during the operation of the bindicator.

Webscraping tutorial - https://timber.io/blog/an-intro-to-web-scraping-with-lxml-and-python/

Automate bindicator (run at certain times)
* allow file to be executable from shell https://www.codementor.io/@gergelykovcs/how-to-run-and-schedule-python-scripts-on-raspberry-pi-n2clhe3kp
* add file execution via cron https://garyhall.org.uk/troubleshooting-cron-raspberry-pi.html

Written in python 3.7.3 and built using Rasperry Pi Zero W running on Raspbian GNU/Linux 10 (buster)
Lights used are https://shop.pimoroni.com/products/blinkt and operated using the python package blinkt
