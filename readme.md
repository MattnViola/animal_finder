# Panda_finder, a Flask App
#### Video Demo: https://youtu.be/3rW0lrY3z5Y
#### Description:

This is a web app that will show the closest panda to yourself 
as well as a route to it. Your closest panda makes use of 
various googlemaps API's, your location using the navigator API 
or by manual input of an address, and a static relational database containing info about pandas.

Panda_finder utilizes three googlemaps API's, namely the Directions API,
the Maps Javascript API, as well as the Distance Matrix API. 
The implementation of Maps Javascript and Directions API are both 
in static/scripts.js, and are used to render the route on the map 
after the form is filled out or the geolocation button is clicked.
The Distance Matrix API implementation is in app.py, and uses the [Python Client](https://github.com/googlemaps/google-maps-services-python). 

The most unique (and possibly bad) design choice is to have the geolocate
button make a fetch() request, and update the page dynamically, while the 
manual form routes to the flask app and renders the webpage again, using
jinja conditionals to change the html. This requires two seperate expressions to 
render the map route, either based on updated html, or a successful fetch request.


Panda_finder currently only uses a static database of zoos in the USA and only routes by driving.

### Requirements:

- Flask 2.2.2
- A Google Maps Platform API key, with the Maps Javascript API, Directions API, and Distance Matrix API enabled.
- The same API key replacing the key within scripts.js
- googlemaps python client
- python-dotenv
- A .env file containing the same API key.
