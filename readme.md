Bindicator Project

(B)indicates via rgb LEDs which bins are due for collection and sends push messages to your devices by checking the council website daily

Inspired by https://twitter.com/tarbard/status/1002464120447397888?lang=en

Upgrade Status
* Done - push notifications with pushover
* In progress - allow multiple users to get personalised info
* To do - add additional council (Knowsley)
* Add options for user to choose notification time?
* Add poetry for packages? And/or docker?

Configured for
* St Helens Council - https://secure.sthelens.net/website/CollectionDates.nsf/servlet.xsp/CollectionDatesMenu

Folders:

* user_config - for storing the URL to where bin collection data is located and pushover tokens for the user and app. This is inside gitignore as it contains address data and private tokens. Add your own folder and json data (create based on sample_user_json_gen.py).
* config - folder for config files : json generator py file creates - rgb values for light colours, bin colours, days of the week as named on council wesbite, xpaths for data retrieval (per council). This data is all read in during the operation of the bindicator.

Webscraping tutorial - https://timber.io/blog/an-intro-to-web-scraping-with-lxml-and-python/

Automate bindicator (run at certain times)
* allow file to be executable from shell https://www.codementor.io/@gergelykovcs/how-to-run-and-schedule-python-scripts-on-raspberry-pi-n2clhe3kp
* add file execution via cron https://garyhall.org.uk/troubleshooting-cron-raspberry-pi.html --> this page is 404ing

Push Notifications with Pushover
https://pushover.net/

Run demo
* run the script from the terminal (list full filepath) with the variable "demo" as shown below </br>
&nbsp;&nbsp;&nbsp;&nbsp; .../Bindicator/bindicator.py "demo" 
* this will light up all the configured light codes and print the corresponding bin types to the terminal

Written in Python 3.7.3 and built using Rasperry Pi Zero W running on Raspbian GNU/Linux 10 (buster) </br>
Lights used are https://shop.pimoroni.com/products/blinkt and operated using the Python package blinkt
