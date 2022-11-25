
// Initialization of the map, as well as rendering a route
// if there is already one in the invisible html divs.
var map;
function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
  directionsRenderer.setMap(map);
  if (!(document.getElementById('origin').innerHTML == '123')) {
  var origin = document.getElementById('origin').innerHTML;
  var destination = document.getElementById('destination').innerHTML;
  var request = {
    origin: origin,
    destination: destination,
    travelMode: 'DRIVING'
  };
  directionsService.route(request, function(result, status) {
    if (status == 'OK') {
      directionsRenderer.setDirections(result);
    }
  });
}}


// Geolocation button along with dynamically updating the page from it.
document.addEventListener("DOMContentLoaded", function () {

  document.querySelector('#geolocate').addEventListener('click', function() {
    navigator.geolocation.getCurrentPosition(success, error);

    function success(position) {
    const lat = position.coords.latitude;
    const long = position.coords.longitude;
    
    let coords = {
      "latitude": lat,
      "longitude": long,
  }
    fetch("/", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(coords),
    })
    .then((response) => response.json())
    .then((panda_info) => {
      // Parsed Json response with information necessary to render gmaps,
      // as well as the panda name/image.
      console.log(panda_info["origin"])
      // Update #panda_name and #panda_portrait
      document.getElementById('panda_name').innerHTML = panda_info["panda_name"];
      document.getElementById('panda_portrait').src = panda_info["panda_portrait_src"]
      // Initialize map client again and render route.
      var directionsService = new google.maps.DirectionsService();
      var directionsRenderer = new google.maps.DirectionsRenderer();
      map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
      });
      directionsRenderer.setMap(map);
      var request = {
        origin: panda_info["origin"],
        destination: panda_info["destination"],
        travelMode: 'DRIVING'
      };
      directionsService.route(request, function(result, status) {
        if (status == 'OK') {
          directionsRenderer.setDirections(result);
        }
    
    })
      })}
    function error() {
      alert('Unable to retrieve your location')
    }
});
});