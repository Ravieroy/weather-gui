from tkinter import *
import requests
import backend_weather
import sys
from tkinter import messagebox

def weather():

    try: #This try block checks for connection issues with api key(KeyError)
        api_key="32e7b591865fddfdd0eb143b98d44c4c"
        units="metric" #other options: imperial(Fahrenheit) and standard(kelvin) is default
        pincode= pincode_text.get()

        # This if-else block looks for input from the user. If not given it assumes the city is selected from the drop down menu
        if city_name_text.get() == "":
            city=city_listbox.get()
            print(city)

        else:
            city=city_name_text.get()
            print(city)
            
        #this block of if-elif checks for input city and pincode. It decides what to you accorinding to the input

        if pincode_text.get() != "" and city_name_text.get() != "": # Both name and pincode is given
            url="http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}&units={}".format(city,pincode,api_key,units)

        elif pincode_text.get() != "" and city_name_text.get() == "": #only pincode is given
            url="http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units={}".format(pincode,api_key,units)

        else:
             url="http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units={}".format(city,api_key,units)

        
        try: # This try block checks for connection 200 or 404. 
            res=requests.get(url)
            output=res.json()

            
            lon = output['coord']['lon']
            lat = output['coord']['lat']

            aqi_url=f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            res_aqi=requests.get(aqi_url)
            output_aqi=res_aqi.json()

            aqi=output_aqi['list'][0]['main']['aqi'] #air quality index
            aqi_index(aqi)
            wind_speed=output['wind']['speed']
            
            city_name=output['name']
            weather_status=output['weather'][0]['description']
            temperature=output['main']['temp']
            humidity=output['main']['humidity']
            
            city_label.configure(text="City Name: " + city_name)
            weather_status_label.configure(text="Weather status: " + weather_status)
            temperature_label.configure(text="Temperature: " + str(temperature) + " deg. C")
            humidity_label.configure(text="Humidity: " + str(humidity))
            wind_speed_label.configure(text="Wind Speed: " + str(wind_speed))

            aqi_label.configure(text="Air Quality Index: " + grade)
        except:
            messagebox.showerror('Connection Error', "Can not connect to the server. Try later")

    except KeyError:
        messagebox.showerror('API Key Error', 'Looks like API key has expired.')
        with open("error.log","w") as my_file:
            my_file.write("""Quite Possibly the API key has expired or isn't working as it should be.
            All you have to do is go to openweathermap.org, sign up and get your own free api key.
            Just copy the api key in the source code in frontend_weather.py script.""")
        sys.exit


def add_command(): # Adds the city into the databse
    backend_weather.insert(city_name_text.get())
    messagebox.showinfo('City Added', 'City Added: '+ city_name_text.get())

def aqi_index(aqi): # aqi index ------->>> Grade
    global grade
    if aqi == 1:
        grade= "Good"
        return grade
    elif aqi == 2:
        grade= "Fair"
        return grade
    elif aqi == 3:
        grade= "Moderate"
        return grade
    elif aqi == 4:
        grade= "Poor"
        return grade
    elif aqi == 5:
        grade= "Very Poor"
        return grade

def delete_command(): # deletes the entry from the database
    try:
        index = backend_weather.get_id(city_name_text.get())
        backend_weather.delete(index[0])
        messagebox.showinfo('City Removed', 'Removed from the list: ' + city_name_text.get())
    except IndexError:
        messagebox.showerror('Entry not found', 'Please enter the correct name.')

    

### This part (when uncommented) will open the help window in a new window. 

# def help_command():
#    top= Toplevel(window)
#    top.geometry("750x250")
#    top.title("Help Window")
#    message = """ Select city: .

# Add city: You can add your choice of city by entering the city name and pressing Add city button. 
# The updated list of cities will be shown in next run of the program

# Help: This button gets to basic functionality of the program

# Close: Closes the window

# Get Weather: Shows you weather data for selected city.
   
# """
#    Label(top, text= message).place(x=80,y= 80)

def help_command():
    help_box_label=Label(window,text="Help !", font=("times",14,"bold"))
    help_box_label.grid(row=11,column=2,columnspan=5)

    select_city_label=Label(window,text="Select city: Select from the existing database of cities")
    select_city_label.grid(row=12,column=2,columnspan=5)

    add_city_label=Label(window,text="Add city: Add you own city to database")
    add_city_label.grid(row=13,column=2,columnspan=5)

    get_weather_label=Label(window,text="Get weather: Shows weather data.")
    get_weather_label.grid(row=14,column=2,columnspan=5)

    close_label=Label(window,text="Close: Closes the window")
    close_label.grid(row=15,column=2,columnspan=5)

    delete_city_label=Label(window,text="Delete city: Removes the city from the list")
    delete_city_label.grid(row=16,column=2,columnspan=5)


window= Tk()
window.geometry("700x300")
window.title("Weather_GUI")

city_name_list= backend_weather.view()
city_listbox=StringVar(window)
city_listbox.set("select city")
option= OptionMenu(window,city_listbox,*city_name_list)
option.grid(row=2,column=1,padx=10,pady=10)


#Static labels

l1= Label(window, text='Enter City Name')
l1.grid(row=2, column=3)

city_name_text = StringVar()
e1 = Entry(window,text=city_name_text,borderwidth=5)
e1.grid(row=2,
        column=4,
        padx=10,
        pady=10,
        ipady=10)



l2= Label(window, text='PIN Code')
l2.grid(row=2, column=6)

pincode_text = StringVar()
e2 = Entry(window,text=pincode_text,borderwidth=5)
e2.grid(row=2,
        column=7,
        padx=10,
        pady=10,
        ipady=10)

#Lables

city_label=Label(window,font=("helvetica",12,"bold"))
city_label.grid(row=3,column=3)

weather_status_label=Label(window,font=("helvetica",12,"bold"))
weather_status_label.grid(row=4,column=3)

temperature_label=Label(window,font=("helvetica",12,"bold"))
temperature_label.grid(row=5,column=3)

humidity_label=Label(window,font=("helvetica",12,"bold"))
humidity_label.grid(row=6,column=3)

wind_speed_label=Label(window,font=("helvetica",12,"bold"))
wind_speed_label.grid(row=7,column=3)

aqi_label=Label(window,font=("helvetica",12,"bold"))
aqi_label.grid(row=8,column=3)




#Buttons
b1=Button(window,text="Get Weather",width=10,command=weather)
b1.grid(row=3,column=7)

b2=Button(window,text="Add city",width=10,command=add_command)
b2.grid(row=4,column=7)

b3=Button(window,text="Help",width=10,command=help_command)
b3.grid(row=5,column=7)

b4=Button(window,text="Close",width=10,command=window.destroy)
b4.grid(row=6,column=7)

b5=Button(window,text="Delete city",width=10,command=delete_command)
b5.grid(row=7,column=7)


window.mainloop()