from __future__ import print_function
import sys
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime

# Initialize flask app
app = Flask(__name__)

load_dotenv()
google_api = os.getenv('google_api')

# Initialize google-maps-services-python
gmaps = googlemaps.Client(key=google_api)

display_map = "https://maps.googleapis.com/maps/api/js?key=" + google_api + "&callback=initMap"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Form input is sent here.
        # Send it to helper function to determine closest zoo.
        try:
            start_address = request.form['address_form']
            zoo = closest_zoo(start_address)   
            
            return render_template('index.html', origin=start_address, destination=zoo[1], panda_name=panda_names[zoo[0]])
        # If the geolocate button is used
        except:
            # A JSON of the longitude and Latitude are sent here after pressing geolocate button.
            # Send it to helper function to determine closest zoo.
            coords = request.get_json()
            lat = coords['latitude']
            long = coords['longitude']
            origin = f"{lat}, {long}"
            zoo = closest_zoo(origin)
            print(zoo)

            return {
                "origin" : origin,
                 "destination" : zoo[1],
                 "panda_name" : panda_names[zoo[0]],
                 "panda_portrait_src" : panda_portrait_src[panda_names[zoo[0]]],
            }

    else:

        return render_template("index.html")


@app.route("/geobutton", methods=["GET", "POST"])
def geobutton():
    # A JSON of the longitude and Latitude are sent here after pressing geolocate button.
    # Send it to helper function to determine closest zoo.
    coords = request.get_json()
    print(coords, file=sys.stderr)
    lat = coords['latitude']
    long = coords['longitude']
    origin = f"{lat}, {long}"
    print(origin, file=sys.stderr)
    zoo = closest_zoo(origin)

    return render_template('index.html', origin=origin, destination=zoo[1], panda_name=panda_names[zoo[0]])
    

# Finds the closest zoo in USA with a panda based off origin.
def closest_zoo(origin):
    
     # Return a matrix object with the distances from the origin to each of the destinations.
    zoo_distances = gmaps.distance_matrix(origin, zoo_addresses)
    
    # Determine zoo with the least distance value.
    least_distance = 0
    zoo_identifier = 0
    zoo_distances_elements = zoo_distances['rows'][0]['elements']
    for i in range(3):
        if zoo_distances_elements[i]['distance']['value'] < least_distance or least_distance == 0:
            least_distance = zoo_distances_elements[i]['distance']['value']
            zoo_identifier = i
    return [zoo_names[zoo_identifier], zoo_addresses[zoo_identifier]]



zoo_names = ['Zoo Atlanta', 'Memphis Zoo', 'Smithsonian National Zoo']
zoo_addresses = ["800 Cherokee Ave SE, Atlanta, GA 30315", 
     "2000 Prentiss Pl, Memphis, TN 38112", "3001 Connecticut Ave NW, Washington, DC 20008"]
# Panda name based off zoo name.
panda_names = {'Zoo Atlanta' : 'Yang Yang', 'Memphis Zoo' : 'Le Le', 'Smithsonian National Zoo' : 'Bao Bao'}
panda_portrait_src = {'Yang Yang' : 'static/yang_yang.jpg', 'Le Le' : 'static/lele.jpg', 'Bao Bao' : 'static/Bao_Bao.jpg'}

if __name__ == '__main__':
    app.run(debug=True)