#!/usr/bin/env python3

import urllib.request

import inline as inline
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import requests
import sys
import os
import getopt

def main(argv):
    import json
    def usage():
        print(('usage: %s [-c city] [-a accesstoken] [-n notify] [-h help] ...' % argv[0]))
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'c:a:n:h')
    except getopt.GetoptError:
        return usage()

    def help():
        print("py-hawa let the user know the real-time air quality values"
              "\ncity: name of the city"
              "\naccesstoken: You need to get access token by registering on http://aqicn.org/data-platform/register/"
              "\nif no accesstoken provided then demo accesstoken will be used and with demo access token only Shanghai's air quality values can be retrieved."
              "\nnotify: True or False- show the notification tray on linux")

    city = 'astana'
    accesstoken = '153147500b88026a9bc053bdf5c2b382cb90e806'
    notify = 'False'
    sendTrayNotification = False

    for (k, v) in opts:
        if k == '-c':
            city= v

        elif k == '-a':
            accesstoken = v

        elif k == '-n':
            if v!= True and v != False:
                return help()
            else:
                sendTrayNotification = v

        elif k == '-h' : return help()


    url = 'http://api.waqi.info/feed/'+city+'/?token=' + accesstoken
    #print('URL: ',url)

    """data = {}
    data['aqi'] = []
    data['aqi'].append({
        'city': city,
        'accesstoken': accesstoken
    })
    with open('data1.txt', 'w') as outfile:
        json.dump(data, outfile)"""

    r = requests.get(url, auth=('user', 'pass'))

    if r.status_code == 200:

        data = r.json()
        print(data)
        with open('data2.json', 'w') as outfile:
            json.dump(data, outfile)
        value = data['data']['iaqi']['pm25']['v']
        toDisplay = str(value)


        if value > 0 and value < 50:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Healthy - "' + toDisplay
            print("Air Quality Alert:" "Current Value: Healthy - " + toDisplay)

        elif value > 50 and value < 100:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Moderate - "' + toDisplay
            print("Air Quality Alert:" "Current Value: Moderate - " + toDisplay)

        elif value > 100 and value < 150:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Sensitive - "' + toDisplay
            print("Air Quality Alert:" "Current Value: Sensitive - " + toDisplay)

        elif value > 150 and value < 200:
            notify = 'notify-send "Air Quality Alert:" "Current Value: UnHealhty - "' + toDisplay
            print ("Air Quality Alert:" "Current Value: UnHealhty - " + toDisplay)

        elif value > 200 and value < 250:
            notify = 'notify-send "Air Quality Alert:" "Current Very Unhealhty - "' + toDisplay
            print ("Air Quality Alert:" "Current Very Unhealhty - " + toDisplay)

        elif value > 250 and value > 300:
            notify = 'notify-send "Air Quality Alert:" "Current Value: Hazardous -  "' + toDisplay
            print ("Air Quality Alert:" "Current Value: Hazardous -  " + toDisplay)

    else:
        notify = 'notify-send "Error: " "Unable to Connect"'
        print ('Error: Unable to connect to server')

    if sendTrayNotification:
        os.system(notify)
    else:
        print ('[Debug] Tray Notification is off.')

if __name__ == '__main__':
    sys.exit(main(sys.argv))
