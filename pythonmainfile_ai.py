import requests
import time
import serial
from tensorflow import keras
from keras.models import load_model
import joblib
import numpy as np
import warnings

api_key = '30f4a29af2d9c0080c163eb2901ae805'
url = f'https://api.openweathermap.org/data/2.5/weather?lat=26.9124&lon=75.7873&appid={api_key}'

model = joblib.load('/Users/devashishghanshani/Desktop/soil_moisture_model.pkl')
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


#Function to read the soil moisture value from the Arduino
def read_moisture_value():
    try:
        connection = serial.Serial('/dev/cu.usbserial-110', 9600)
        print('Connection established')

        # Reading the moisture value from the Arduino
        moisture_value = connection.readline().decode('utf-8')
        print('Got the moisture value:', moisture_value)
        connection.close()

        return moisture_value
    except Exception as e:
        print('An error occurred:', str(e))
        return None
#function to control the valve
def control_valve(valve_state):
    connection = serial.Serial('/dev/cu.usbserial-110', 9600)

    # Send the valve state to the Arduino
    connection.write(valve_state.encode('utf-8'))
    connection.close()

while True:
    try:
        # HTTP GET request to the weather API
        response = requests.get(url)
        
        if response.status_code == 200:

            weather_data = response.json()
            
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            weather_description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temperature}°F")
            print(f"Humidity: {humidity}%")
            print(f"Weather: {weather_description}")
        else:
            print(f"Failed to fetch weather data. Status code: {response.status_code}")
        
        # Read the soil moisture value
        moisture_value = read_moisture_value()
        if moisture_value is not None:
            print('got value')
            moisture_value = np.array([float(moisture_value)]).reshape(-1, 1)
            print(moisture_value)
            prediction = model.predict(moisture_value)[0]
            print(prediction)

            if prediction > 500 and humidity > 50:
               valve_state = '1' 
               print('valve decision sent1') 
            else:
               valve_state = '0'
               print('valve decision sent2')
            control_valve(valve_state)

            time.sleep(10)
        else:
            print('moisture is zero')
     


    except KeyboardInterrupt:
        break
