from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests as req
import folium
from folium import Map, Marker
from folium.plugins import LocateControl 
import os # For loading the environment variables (API keys and data paths)
from dotenv import load_dotenv # For loading the environment variables (API keys and playlist URI's)
##########################
from folium import PolyLine
from folium import GeoJson
from getpass import getpass
#########################

app = Flask(__name__)

# load the csv file
path = os.path.join("data", "Fredagsbarer_oversigt.xlsx")
df = pd.read_excel(path)

##############################
# get the API key from .env file
load_dotenv() # Load the environment variables from the .env file
api_key = os.getenv("ORS_API_KEY") # Get the API key from the environment variable

def get_route(start, end, api_key, mode):
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": api_key,
        "Content-Type": "application/json; charset=utf-8"
    }
    body = {
        "coordinates": [start, end],
        "instructions": "false",
    }
    r = req.post(f"https://api.openrouteservice.org/v2/directions/{mode}/geojson", json=body, headers=headers)
    
    data = r.json()
    if 'features' in data:
        geometry = data['features'][0]['geometry']['coordinates']
        properties = data['features'][0]['properties']
        if 'summary' in properties and 'duration' in properties['summary']:  # Check if 'duration' is in 'summary'
            duration = properties['summary']['duration']  # Get the travel time from 'summary'
            # Convert duration from seconds to minutes
            duration_in_minutes = duration / 60
            return geometry, duration_in_minutes
        else:
            print(f'Error: Could not get route properties. {data}')
            return [], 0
    else:
        print(f'Error: Could not get route. {data}')
        return [], 0

def generate_legend(durations_cycling, durations_walking, durations_driving):
    durations_cycling = [d for d in durations_cycling if d is not None]
    durations_walking = [d for d in durations_walking if d is not None]
    durations_driving = [d for d in durations_driving if d is not None]

    avg_cycling = sum(durations_cycling) / len(durations_cycling)
    avg_walking = sum(durations_walking) / len(durations_walking)
    avg_driving = sum(durations_driving) / len(durations_driving)
    
    legend_html = """
    <div style="position: fixed; top: 50px; right: 50px; width: 170px; height: 150px; padding-right: 10px; padding-left: 10px; padding-top: 5px; \
                border:2px solid grey; z-index:9999; font-size:14px; background-color:white; \
                ">
      <p><b>Average travel times between Friday Bars:</b></p>
    """
    legend_html += f"<p>Walking: {avg_walking:.2f} minutes</p>"
    legend_html += f"<p>Cycling: {avg_cycling:.2f} minutes</p>"
    legend_html += f"<p>Driving: {avg_driving:.2f} minutes</p>"
    legend_html += "</div>"
    return legend_html

def get_google_maps_directions_url(lat, lon):
    url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    return url

#################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/filter_bars', methods=['POST'])
def filter_bars():
    price = request.form['price']
    floor_quality = request.form['floor_quality']
    love_potential = request.form['love_potential']
    hygge_factor = request.form['hygge_factor']
    wheelchair_access = request.form['wheelchair_access']
    party_factor = request.form['party_factor']
    
    filtered_df = df.copy()

    if price != 'anything goes':
        filtered_df = filtered_df[filtered_df['prices'] == price]
    if floor_quality:
        filtered_df = filtered_df[filtered_df['floor_quality'] >= int(floor_quality)]
    if love_potential:
        filtered_df = filtered_df[filtered_df['love_potential'] >= int(love_potential)]
    if hygge_factor:
        filtered_df = filtered_df[filtered_df['hygge_factor'] >= int(hygge_factor)]
    if wheelchair_access != 'dontcare':
        filtered_df = filtered_df[filtered_df['wheelchair_access'] == wheelchair_access]
    if party_factor:
        filtered_df = filtered_df[filtered_df['party_factor'] >= int(party_factor)]

    bars = filtered_df.to_dict('records')  
    
    durations = []
    # create the map
    m = Map(location=[56.16, 10.20], zoom_start=14)

    # add a marker for each bar
    for bar in bars:
        if isinstance(bar['geo location'], str): # check if 'geo location' is a string
            lat, lon = map(float, bar['geo location'].split(','))
            Marker([lat, lon], popup=bar['name']).add_to(m)

            # format the popup string
            directions_url = get_google_maps_directions_url(lat, lon)
            popup_text = f"""
                            <h4 style='color: #4CAF50;'>{bar['name']}</h4><br>
                            <b style='font-size: 18px;'>Address: </b><span style='font-size: 16px;'>{bar['address']}</span><br>
                            <b style='font-size: 18px;'>Opening hours: </b><span style='font-size: 16px;'>{bar['opening hours']}</span><br>
                            <b style='font-size: 18px;'>SoMe: </b><a href="{bar['social media']}" style='font-size: 16px;'>Link</a><br>
                            <b style='font-size: 18px;'>Information: </b><span style='font-size: 16px;'>{bar['information']}</span><br>
                            <b style='font-size: 18px;'>Prices: </b><span style='font-size: 16px;'>{bar['prices']}</span><br>
                            <div style='text-align: center;'>
                                <a href='{directions_url}' target='_blank'><button type='button' style='background-color: #4CAF50; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border: none; border-radius: 12px;'>Get Directions</button></a>
                            </div>
                        """
            # create a marker and add it to the map
            folium.Marker(
                [lat, lon], 
                popup=folium.Popup(popup_text, max_width=250)
            ).add_to(m)

#####################    
    # ROUTING
    durations_cycling = []
    durations_walking = []
    durations_driving = []

    bars_to_exclude = ["Barbaren", "Arken"]

    for i in range(len(bars)-1):
        bar1 = bars[i]
        bar2 = bars[i+1]
        if bar1['name'] in bars_to_exclude or bar2['name'] in bars_to_exclude:
            continue
        if isinstance(bar1['geo location'], str) and isinstance(bar2['geo location'], str): 
            lat1, lon1 = map(float, bar1['geo location'].split(','))
            lat2, lon2 = map(float, bar2['geo location'].split(','))

            route, duration = get_route([lon1, lat1], [lon2, lat2], api_key, "cycling-regular")
            if duration is not None:
                durations_cycling.append(duration)
            route, duration = get_route([lon1, lat1], [lon2, lat2], api_key, "foot-walking")
            if duration is not None:
                durations_walking.append(duration)
            route, duration = get_route([lon1, lat1], [lon2, lat2], api_key, "driving-car")
            if duration is not None:
                durations_driving.append(duration)
            
            #route = get_route([lon1, lat1], [lon2, lat2], api_key)

            if route:
                # convert the coordinates to a format that folium can understand
                route = [(y, x) for x, y in route]
                PolyLine(route).add_to(m)
            # Get the route and duration to the bar
            
            durations.append(duration)

    # Create the legend HTML
    legend_html = generate_legend(durations_cycling, durations_walking, durations_driving)
    # Add the HTML to the map
    m.get_root().html.add_child(folium.Element(legend_html))

#####################

    # add locate control to the map
    folium.plugins.LocateControl().add_to(m)

    # render the map to an HTML string
    map_html = m._repr_html_()

    # pass the map to the template
    return render_template('map.html', map=map_html, durations=durations)
        
    map_html = m._repr_html_()
    return render_template('map.html', map=map_html)


if __name__ == '__main__':
    app.run(debug=True)