# Load the AI model
import requests
import time
import serial
from tensorflow import keras
from keras.models import load_model
import joblib
import numpy as np
import warnings
# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = '30f4a29af2d9c0080c163eb2901ae805'

# Define the URL with latitude and longitude for Jaipur
url = f'https://api.openweathermap.org/data/2.5/weather?lat=26.9124&lon=75.7873&appid={api_key}'

# Load the AI model
model = joblib.load('/Users/devashishghanshani/Desktop/soil_moisture_model.pkl')
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


# Create a function to read the soil moisture value from the Arduino
def read_moisture_value():
    try:
        connection = serial.Serial('/dev/cu.usbserial-110', 9600)
        print('Connection established')

        # Read the moisture value from the Arduino
        moisture_value = connection.readline().decode('utf-8')
        print('Got the moisture value:', moisture_value)

        # Close the connection
        connection.close()

        return moisture_value
    except Exception as e:
        print('An error occurred:', str(e))
        return None
# Create a function to control the valve
def control_valve(valve_state):
    connection = serial.Serial('/dev/cu.usbserial-110', 9600)

    # Send the valve state to the Arduino
    connection.write(valve_state.encode('utf-8'))

    # Close the connection
    connection.close()

# Main loop
while True:
    try:
        # Send an HTTP GET request to the weather API
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            weather_data = response.json()
            
            # Extract relevant weather information
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            weather_description = weather_data['weather'][0]['description']
            
            # Print the weather information
            print(f"Temperature: {temperature}°F")
            print(f"Humidity: {humidity}%")
            print(f"Weather: {weather_description}")
        else:
            print(f"Failed to fetch weather data. Status code: {response.status_code}")
        
        # Read the soil moisture value
        moisture_value = read_moisture_value()
        if moisture_value is not None:
            print('got value')
        # Convert moisture_value to a 2D array
            moisture_value = np.array([float(moisture_value)]).reshape(-1, 1)
            print(moisture_value)

        # Predict the amount of water needed to irrigate the crop
            prediction = model.predict(moisture_value)[0]
            print(prediction)

        # Decide whether to open or close the valve
            if prediction > 500 and humidity > 50:
               valve_state = '1' 
               print('valve decision sent1') # Assuming the valve state is a string
            else:
               valve_state = '0'
               print('valve decision sent2')
        
        # Control the valve
            control_valve(valve_state)

        # Sleep for 1 minute
            time.sleep(10)
        else:
            print('moisture is zero')
     


    except KeyboardInterrupt:
        break