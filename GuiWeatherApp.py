import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from datetime import datetime
from API_key import OWM_API_KEY
from urllib.request import urlopen
import json

win = tk.Tk()
win.title("Python Project")

#Exit GUI function
def quit():
    win.quit()
    win.destroy()
    exit()

#creating a Menu bar
menuBar=Menu()
win.config(menu=menuBar)

#Add Menu items
fileMenu = Menu(menuBar,tearoff=0)
fileMenu.add_command(label="New")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quit)
menuBar.add_cascade(label="File",menu=fileMenu)

#Add another Menu
helpMenu = Menu(menuBar,tearoff=0)
helpMenu.add_command(label="About")
menuBar.add_cascade(label="Help", menu=helpMenu)

# TAb control
tabControl = ttk.Notebook(win)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='OpenWeatherMap')

tabControl.pack(expand=1)

#create a container to hold all other widgets
weather_conditions_frame= ttk.LabelFrame(tab1, text='Current Weather Conditions')

#using tkinter grid layout manager
weather_conditions_frame.grid_configure(column=0, row=1, padx=8, pady=4)

#adding new labelframe
open_weather_cities_frame = ttk.LabelFrame(tab1, text=' Latest Observation for ')
open_weather_cities_frame.grid_configure(column=0, row=0, padx=8, pady=4)

#place label and combobox into new frame
ttk.Label(open_weather_cities_frame, text="Location: ").grid(column=0, row=0,sticky='W')

#Add combobox
city = tk.StringVar()
station_id_combo = ttk.Combobox(open_weather_cities_frame, width=16, textvariable=city)
station_id_combo['values']=('Los Angeles, US','London, UK','Paris, FR','Mumbai, IN', 'Texas, US')
station_id_combo.grid(column=1, row=0)
#selecting first city
station_id_combo.current(0)

#increase combobox width to longest city
max_width = max([len(x) for x in station_id_combo['values']])

ENTRY_WIDTH = max_width + 3
# Add label and Textbox entry widgets
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Last Updated:").grid(column=0, row=1, sticky='E')
open_updated = tk.StringVar()
updatedEntry = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=open_updated,
                         state='readonly')
updatedEntry.grid(column=1,row=1,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Weather:").grid(column=0, row=2, sticky='E')
open_weather = tk.StringVar()
weatherEntry = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=open_weather,
                         state='readonly')
weatherEntry.grid(column=1,row=2,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Temperature:").grid(column=0, row=3, sticky='E')
open_temp = tk.StringVar()
tempEntry = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=open_temp,state='readonly')
tempEntry.grid(column=1,row=3,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Relative Humidity:").grid(column=0, row=4, sticky='E')
open_rel_humi = tk.StringVar()
humiEntry = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=open_rel_humi,state='readonly')
humiEntry.grid(column=1,row=4,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Wind:").grid(column=0, row=5, sticky='E')
open_wind = tk.StringVar()
tempWind = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=open_wind,state='readonly')
tempWind.grid(column=1,row=5,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Visibility:").grid(column=0, row=6, sticky='E')
open_visi = tk.StringVar()
tempWind = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=open_visi,state='readonly')
tempWind.grid(column=1,row=6,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Pressure:").grid(column=0, row=7, sticky='E')
open_msl = tk.StringVar()
tempWind = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=open_msl,state='readonly')
tempWind.grid(column=1,row=7,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Sunrise:").grid(column=0, row=8, sticky='E')
sunrise = tk.StringVar()
sunriseEntry = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=sunrise,state='readonly')
sunriseEntry.grid(column=1,row=8,sticky='W')
#-------------------------------------------------------------------------------------
ttk.Label(weather_conditions_frame, text="Sunset:").grid(column=0, row=9, sticky='E')
sunset = tk.StringVar()
sunsetEntry = ttk.Entry(weather_conditions_frame,width=ENTRY_WIDTH,textvariable=sunset,state='readonly')
sunsetEntry.grid(column=1,row=9,sticky='W')
#-------------------------------------------------------------------------------------
# Station City label
open_location = tk.StringVar()
ttk.Label(open_weather_cities_frame, textvariable=open_location).grid(column=0, row=1, columnspan=3)
#-------------------------------------------------------------------------------------

#adding space aroung each label
for child in weather_conditions_frame.winfo_children():
    child.grid_configure(padx=4, pady=2)

# OpenWeatherMap Data collection
def get_open_weather_data(city='London, UK'):
    city = city.replace(' ', '%20')
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city,OWM_API_KEY)
    response = urlopen(url)
    data = response.read().decode()
    json_data = json.loads(data)
    # print (json_data)
    lastupdate_unix = json_data['dt']
    humidity = json_data['main']['humidity']
    pressure = json_data['main']['pressure']
    temp_kelvin = json_data['main']['temp']
    city_name = json_data['name']
    city_country = json_data['sys']['country']
    sunrise_unix = json_data['sys']['sunrise']
    sunset_unix = json_data['sys']['sunset']
    try:
        visibility_meter = json_data['visibility']
    except:
        visibility_meter = 'N/A'
    own_weather = json_data['weather'][0]['description']
    win_degree = json_data['wind']['speed']

    # function to covert kelvin to celsius
    def kelvin_to_celsius(temp_k):
        return ("{:.1f}".format(temp_k - 273.15))

    # function to convert kalvin to fahrenheit
    def kelvin_to_fahrenheit(temp_k):
        return ("{:.1f}".format((temp_k - 273.15) * 1.8000 + 32.00))

    # function to convert unix time
    def unix_to_datetime(unix_time):
        return datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')

    # function to convert meter to miles
    def meter_to_miles(meter):
        return "{:.2f}".format((meter * 0.00062137))

    if visibility_meter is 'N/A':
        visibility_miles = 'N/A'
    else:
        visibility_miles = meter_to_miles(visibility_meter)

    # function to convert meter per sec to miles per hour
    def mps_to_mph(meter_second):
        return "{:.1f}".format((meter_second * 2.23693629))

    # Update GUI entry widgets with live data
    open_location.set('{}, {}'.format(city_name, city_country))
    lastupdate = unix_to_datetime(lastupdate_unix)
    open_updated.set(lastupdate)
    open_weather.set(own_weather)
    temp_fahr = kelvin_to_fahrenheit(temp_kelvin)
    temp_cels = kelvin_to_celsius(temp_kelvin)
    open_temp.set('{} \xb0F ({} \xb0C)'.format(temp_fahr,temp_cels))
    open_rel_humi.set('{} %'.format(humidity))
    wind_speed_mph = mps_to_mph(win_degree)
    open_wind.set('{} degress at {} MPH'.format(win_degree,wind_speed_mph))
    open_visi.set('{} miles'.format(visibility_miles))
    open_msl.set('{} hPa'.format(pressure))
    sunrise_dt = unix_to_datetime(sunrise_unix)
    sunrise.set(sunrise_dt)
    sunset_dt = unix_to_datetime(sunset_unix)
    sunset.set(sunset_dt)

# callback function
def get_station():
    station = station_id_combo.get()
    get_open_weather_data(station)

get_weather_btn = ttk.Button(open_weather_cities_frame, text='Get Weather', command=get_station).grid(column=2,row=0)

# start GUI
win.mainloop()