import json
import tkinter as tk
from datetime import datetime
from tkinter import *

import pytz as pytz
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

from geopy.geocoders import Nominatim
root = tk.Tk()
def cityToCordinates(city):

    geolocator = Nominatim(user_agent="Maciej Rys")
    location = geolocator.geocode(city)
    return (location.latitude, location.longitude)

def api(city, day = "today"):
    import requests

    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

    querystring = {"q": city, "cnt": "3", "units": "metric"}

    headers = {
        'x-rapidapi-key': "e6592117bdmsha6de3f2da2acda5p17303ajsn1750741cdf96",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }


    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    weatherList = response['list']
    iconsUrl = []
    tempList = []
    for x in range(3):
        iconsUrl.append("http://openweathermap.org/img/wn/" + weatherList[x]['weather'][0]['icon'] +"@2x.png")
        tempList.append(round(weatherList[x]['temp']['day']))
    CreateImages(iconsUrl, tempList)



    api_key = "b9fc36b5b69d63c5a971ef48888309be"
    lat = cityToCordinates(city)[0]
    lon = cityToCordinates(city)[1]
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

    response = requests.get(url)
    data = response.json()
    hourly = data["hourly"]
    addHours = 0
    howMuch = 24
    if day == "tommorow":
        addHours = 24 - datetime.now().hour
    elif day == "afterTommorow":
        addHours = 48 - datetime.now().hour
        howMuch = datetime.now().hour
    tempList = []
    timeList = []
    for x in range(addHours,howMuch + addHours):
        dt = datetime.fromtimestamp(hourly[x]["dt"], pytz.timezone('Europe/Warsaw'))
        temp = hourly[x]["temp"]
        tempList.append(round(temp))
        timeList.append(dt.time().hour)

    createGraph(tempList, timeList)

def createGraph(data, times):
    c_width = 500  # Define it's width
    c_height = 400  # Define it's height
    c = tk.Canvas(root, width=c_width, height=c_height, bg='white')
    c.grid(row=5, columnspan=3)

    y_stretch = 5  # The highest y = max_data_value * y_stretch
    y_gap = 120  # The gap between lower canvas edge and x axis
    x_stretch = 10  # Stretch x wide enough to fit the variables
    x_width = 10  # The width of the x-axis
    x_gap = 0  # The gap between left canvas edge and y axis

    # A quick for loop to calculate the rectangle
    i = 0
    for x, y in enumerate(data):
        # coordinates of each bar

        # Bottom left coordinate
        x0 = x * x_stretch + x * x_width + x_gap

        # Top left coordinates
        y0 = c_height - (y * y_stretch + y_gap)

        # Bottom right coordinates
        x1 = x * x_stretch + x * x_width + x_width + x_gap

        # Top right coordinates
        y1 = c_height - y_gap

        # Draw the bar
        color = "red"
        if y > 15:
            color = "red"
        elif(y > 5 and y < 16):
            color = "yellow"
        else:
            color = "blue"
        c.create_rectangle(x0, y0, x1, y1, fill=color)

        # Put the y value above the bar
        textHeight = y0
        if y < 0:
            textHeight += 20
        c.create_text(x0 + 2, textHeight, anchor=tk.SW, text=str(y))
        c.create_text(x0 + 2, 80, anchor=tk.SW, text=str(times[i]))
        i += 1

def createGUI():
    root.geometry("500x650")
    root.resizable(height=False, width=False)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    labelCity = tk.Label(root, text="Podaj miasto")
    labelCity.grid(row = 0, column = 0)
    textCity = tk.Text(root, height=2, width=20)
    textCity.grid(row = 1, column = 0)
    textCity.insert(END,"Wrocław")
    buttonCity = tk.Button(root, text="Pokaż pogodę", command = lambda: api(textCity.get("1.0",'end-1c')))
    buttonCity.grid(row=1, column=1)
    labelDay1 = tk.Button(root, text="Dziś" , command = lambda: api(textCity.get("1.0",'end-1c')))
    labelDay1.grid(row = 2, column = 0)
    labelDay2 = tk.Button(root, text="Jutro" , command = lambda: api(textCity.get("1.0",'end-1c'),"tommorow"))
    labelDay2.grid(row = 2, column = 1)
    labelDay3 = tk.Button(root, text="Pojutrze", command = lambda: api(textCity.get("1.0",'end-1c'),"afterTommorow"))
    labelDay3.grid(row = 2, column = 2)

def CreateImages(links, temps):
    labelTempDay1 = tk.Label(root, text=temps[0])
    labelTempDay1.grid(row = 3, column = 0)
    labelTempDay2 = tk.Label(root, text=temps[1])
    labelTempDay2.grid(row = 3, column = 1)
    labelTempDay3 = tk.Label(root, text=temps[2])
    labelTempDay3.grid(row = 3, column = 2)

    u = urlopen(links[0])
    raw_data = u.read()
    u.close()
    img = ImageTk.PhotoImage(Image.open(BytesIO(raw_data)))
    image1 = tk.Label(image = img)
    image1.image = img
    image1.grid(row = 4, column = 0)

    u = urlopen(links[1])
    raw_data = u.read()
    u.close()
    img = ImageTk.PhotoImage(Image.open(BytesIO(raw_data)))
    image1 = tk.Label(image = img)
    image1.image = img
    image1.grid(row = 4, column = 1)

    u = urlopen(links[2])
    raw_data = u.read()
    u.close()
    img = ImageTk.PhotoImage(Image.open(BytesIO(raw_data)))
    image1 = tk.Label(image = img)
    image1.image = img
    image1.grid(row = 4, column = 2)

if __name__ == '__main__':
    createGUI()
    api("Wrocław")
    root.mainloop()

