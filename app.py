import config

import requests
from flask import Flask, render_template, request, abort, Response
import os

# create flask app object
app = Flask(__name__)

@app.route("/city")
def current_temp():
    """
    search for a specific city's current temperature
    param:
        api_key: api key for openweathermap.org
        city: city name
    """

    # initialize api key
    api_k = config.api_key

    # pass city name as an arg
    city = request.args.get("q")

    # call api and convert response into dict
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_k}"
    response = requests.get(url).json()

    # error if unknown city name or invalid api key
    if response.get("cod") != 200:
        message = response.get("message", "")
        return (
            f"Error getting temperature for {city.title()}. Error message = {message}"
        )

    # get temperature data
    list_of_data = response.get("main", {})

    data = {
        "current_temperature": str(list_of_data["temp"]) + "K",
        "current_humidity": str(list_of_data["humidity"]) + "%",
        "min_temp": str(list_of_data["temp_min"]) + "K",
        "max_temp": str(list_of_data["temp_max"]) + "K",
    }

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
