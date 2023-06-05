from flask import Flask, render_template, request
import pandas as pd
import folium

from folium import Map, Marker
from folium.plugins import LocateControl
import os

app = Flask(__name__)

# load the csv file
path = os.path.join("data", "Fredagsbarer_oversigt.xlsx")
df = pd.read_excel(path)

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
    if wheelchair_access != 'anything goes':
        filtered_df = filtered_df[filtered_df['wheelchair_access'] == wheelchair_access]
    if party_factor:
        filtered_df = filtered_df[filtered_df['party_factor'] >= int(party_factor)]

    bars = filtered_df.to_dict('records')
    
    
    # create the map
    m = Map(location=[56.16, 10.20], zoom_start=14)

    # add a marker for each bar
    for bar in bars:
        if isinstance(bar['geo location'], str): # check if 'geo location' is a string
            lat, lon = map(float, bar['geo location'].split(','))
            Marker([lat, lon], popup=bar['name']).add_to(m)

            # format the popup string
            popup_text = f"""
                            <h4>{bar['name']}</h4><br>
                            <b>Address: </b>{bar['address']}<br>
                            <b>Opening hours: </b>{bar['opening hours']}<br>
                            <b>SoMe: </b><a href="{bar['social media']}">Link</a><br>
                            <b>Information: </b>{bar['information']}<br>
                            <b>Prices: </b>{bar['prices']}<br>
                         """
            # create a marker and add it to the map
            folium.Marker(
                [lat, lon], 
                popup=folium.Popup(popup_text, max_width=250)
            ).add_to(m)


    # add locate control to the map
    folium.plugins.LocateControl().add_to(m)

    # render the map to an HTML string
    map_html = m._repr_html_()

    # pass the map to the template
    return render_template('map.html', map=map_html)



if __name__ == '__main__':
    app.run(debug=True)
