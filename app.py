import config

import requests
from flask import Flask, render_template, request, abort, Response
import os

# create flask app object
app = Flask(__name__)

@app.route('/city')
def search_city():

    ''' 
    search for a specific city
    param:
        api_key: api key for openweathermap.org
        city: city name
    '''

    # initialize api key
    api_k = config.api_key

    # pass city name as an arg
    city = request.args.get('q')

    # call api and convert response into dict
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_k}'
    response = requests.get(url).json()

    # error if unknown city name or invalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message}'
    
    # get temperature and description
    current_temperature = response.get('main', {}).get('temp')
    current_wind_speed = response.get('wind', {}).get('speed')

    if current_temperature:
        current_temperature_celsius = round(current_temperature - 273.15, 2)
        return f'The current temperature of {city.title()} is {current_temperature_celsius} &#8451;. The wind speed is {current_wind_speed} mph.'
    else:
        return f'Error getting temperature for {city.title()}'

if __name__ == '__main__':
    app.run(debug=True)
