from flask import Flask, render_template, request, jsonify
import requests
import folium

app = Flask(__name__)

# Example function to get elevation data from a clicked point using Open Elevation API
def get_elevation(lat, lon):
    try:
        # Open Elevation API URL (free and open source)
        response = requests.get(
            f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}')
        elevation_data = response.json()
        elevation = elevation_data['results'][0]['elevation']
        return elevation
    except Exception as e:
        return f"Error fetching elevation data: {e}"

# Example function to get rainfall data (using OpenWeatherMap or another API)
def get_rainfall_data(lat, lon):
    # Replace with actual API key and request to a weather API
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}")
        data = response.json()
        rainfall = data.get('rain', {}).get('1h', 0)  # Get last hour's rainfall
        return rainfall
    except Exception as e:
        return f"Error fetching rainfall data: {e}"

# Route for displaying the map
@app.route('/')
def index():
    # Create a Folium map centered on a default location (e.g., Lisbon)
    map_center = [38.736946, -9.142685]  # Example: Lisbon, Portugal
    m = folium.Map(location=map_center, zoom_start=12)

    # Add click event to get elevation when clicking on the map
    m.add_child(folium.LatLngPopup())

    # Save the map as HTML to render in the template
    m.save('templates/map.html')

    return render_template('map.html')

# Route for AJAX request to get elevation data
@app.route('/get_elevation', methods=['POST'])
def get_elevation_route():
    lat = request.json.get('lat')
    lon = request.json.get('lon')
    elevation = get_elevation(lat, lon)
    return jsonify({'elevation': elevation})

if __name__ == '__main__':
    app.run(debug=True)
