## Weather App

Input: Zipcode
Output:
Displays weather forecast for the given zip code
1. Forecast should at least have current temperature
2. Also shows high/low temperature and/or extended forecast

## Installation and Setup Instructions

Clone this repository. You will need `python`, `virtualenv`, and `virtualenvwrapper-win` installed on your machine.

#### Set up a virtual environment:

`mkvirtualenv weather-app`

#### Installation:

`pip install flask`

`pip install requests`

#### To Start Server:

`flask run`  

#### Can also be executed from postman:
`e.g.: http://127.0.0.1:5000/weather_zipcode?zip_code=400001&country=IN`


## Weather API
`python weather_api.py`

#### To get JSON details use below url:
`http://127.0.0.1:5000/weather_zipcode?zip_code=400001&country=IN`