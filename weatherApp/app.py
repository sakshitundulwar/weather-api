from flask_caching import Cache
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
# cache timeout is 30 minutes
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 1800})  

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Weather Dashboard</h1>
<p>Displays weather forecast for the given India zip code.</p>'''


@app.route('/weather_zipcode', methods=['GET'])
@cache.cached()
def weather_zipcode():
    '''
    Input: zipcode
    Output: JSON response with weather details
    '''
    # Get zipcode from request
    zip_code = request.args.get('zip_code')
    country = request.args.get('country')
    print(country)

    # Show valid error message when entered invalid zipcode
    if not zip_code:
        return jsonify({'error': 'Please enter valid zipcode'}), 400

    api_key = '5c0f922a682dcb1819ada389f807fe9c'
    weather_url = 'http://api.openweathermap.org/data/2.5/weather'

    # Request to openweathermap API with API_KEY
    params = {'zip': f'{zip_code},{country}', 'appid': api_key, 'units': 'metric'}
    response = requests.get(weather_url, params=params)
    # print(response.json())
    
    # Show valid error message when response is not successful
    if response.status_code != 200:
        return jsonify({'error': 'Error occured to get weather details'}), 500
    
    # JSON response parsing
    weather_details = response.json()

    # Extract the JSON response for relevant details 
    current_temp = weather_details['main']['temp']
    high_temp = weather_details['main']['temp_max']
    low_temp = weather_details['main']['temp_min']
    description = weather_details['weather'][0]['description']
    country_name = weather_details['sys']['country']
    city_name = weather_details['name']
    weather_icon = weather_details['weather'][0]['icon']
    
    # If zipcode is already in cache set 'cached' to True
    if cache.get(zip_code):
        final_result = cache.get(zip_code)
        final_result['cached'] = True
        return jsonify(final_result)
    
    # Create final JSON response to show in html
    final_result = {
        'cached': False,
        'zip_code': zip_code,
        'city': city_name,
        'country': country_name,
        'high_temp': high_temp,
        'low_temp': low_temp,
        'current_temp': current_temp,
        'description': description,
        'icon' : weather_icon
    }

    # Cache result for 30 minutes
    cache.set(zip_code, final_result, timeout=1800)

    return render_template("weather.html", final_result=final_result)

if __name__ == '__main__':
    app.run(debug=True)
