from flask import Flask, render_template, request, jsonify
import requests
import folium
import os

app = Flask(__name__)

# Function to get elevation using Open-Elevation API
def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        elevation_data = response.json()
        if 'results' in elevation_data and len(elevation_data['results']) > 0:
            elevation = elevation_data['results'][0]['elevation']
            return elevation
        else:
            return "Elevation data not found"
    except requests.exceptions.RequestException as e:
        return f"Error fetching elevation data: {e}"

# Route for displaying the map
@app.route('/')
def index():
    # Create a Folium map centered on a default location (e.g., Lisbon)
    map_center = [38.736946, -9.142685]  # Example: Lisbon, Portugal
    m = folium.Map(
        location=map_center, 
        zoom_start=12, 
        tiles='Stamen Terrain',
        attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap'
    )
    # Add click event to get elevation when clicking on the map
    m.add_child(folium.LatLngPopup())

    # Render the map as an HTML string
    map_html = m._repr_html_()

    return render_template('map.html', map_html=map_html)

# Route for AJAX request to get elevation data
@app.route('/get_elevation', methods=['POST'])
def get_elevation_route():
    lat = request.json.get('lat')
    lon = request.json.get('lon')
    elevation = get_elevation(lat, lon)
    return jsonify({'elevation': elevation})

if __name__ == '__main__':
    app.run(debug=True)
