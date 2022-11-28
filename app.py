from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime
import sqlite3

# Initialize flask app
app = Flask(__name__)

# Initialize google-maps-services-python
load_dotenv()
google_api = os.getenv('google_api')
gmaps = googlemaps.Client(key=google_api)




@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Form input is sent here.
        # Send it to helper function to determine closest zoo.
        try:
            start_address = request.form['address_form']
            zoo = closest_zoo(start_address)   
            
            return render_template('index.html', origin=start_address, panda_name=zoo[0], zoo_name=zoo[1], destination=zoo[3])
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
                 "destination" : zoo[3],
                 "panda_name" : zoo[0],
                 "panda_portrait_src" : zoo[2],
                 "zoo_name" : zoo[1],
            }

    else:

        return render_template("index.html")

# Finds the closest zoo in USA with a panda based off origin.
def closest_zoo(origin):
    
    # Initialize database and retrieve a list of zoo addresses.
    con = sqlite3.connect("panda_finder.db")
    panda_db = con.cursor()
    con = sqlite3.connect("panda_finder.db")
    con.row_factory = lambda cursor, row: row[0]
    panda_db = con.cursor()
    zoo_addresses = panda_db.execute("SELECT address FROM panda_info").fetchall()

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
    
    # Retrieve the rest of the zoo info after identifying the closest zoo
    panda_name = panda_db.execute("SELECT name FROM panda_info WHERE address=?", (zoo_addresses[zoo_identifier],)).fetchone()
    zoo_name = panda_db.execute("SELECT zoo FROM panda_info WHERE address=?", (zoo_addresses[zoo_identifier],)).fetchone()
    portrait_src = panda_db.execute("SELECT portrait_src FROM panda_info WHERE address=?", (zoo_addresses[zoo_identifier],)).fetchone()

    return [panda_name, zoo_name, portrait_src, zoo_addresses[zoo_identifier]]

if __name__ == '__main__':
    app.run()