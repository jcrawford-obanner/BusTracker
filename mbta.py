import requests
import json
import webbrowser
import sys

# Replace with your Google Maps API key
google_maps_api_key = "AIzaSyAPp41imieQrvMxzXcNQmgtRFd0QrREm1Y"

# Replace with the MBTA bus location API endpoint
mbta_bus_api_endpoint = "https://api-v3.mbta.com/vehicles"

# Create a function to fetch bus locations from the MBTA API
def get_bus_locations():
    params = {
        'api_key': '9c9841081e974e48971da86c982f61be',  # Replace with your MBTA API key
    }
    response = requests.get(mbta_bus_api_endpoint, params=params)
    if response.status_code == 200:
        return response.json()

# Write the HTML to a file

# Fetch bus locations and save them to a JSON file
bus_data = get_bus_locations()
if bus_data:
    with open("mbta_bus_locations.json", "w") as json_file:
      json.dump(bus_data, json_file)

def main(busRoute):
  html = """
  <!DOCTYPE html>
  <html>
    <head>
      <title>MBTA Bus Tracker</title>
      <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAPp41imieQrvMxzXcNQmgtRFd0QrREm1Y"></script>
    </head>
    <body>
      <div id="map" style="height: 600px;"></div>
      <script>
        markers = [];
        function initMap() {{
          var map = new google.maps.Map(document.getElementById('map'), {{
            center: {{ lat: 42.3601, lng: -71.0589 }}, // Boston, MA
            zoom: 13
          }});

          // Fetch bus locations from the MBTA API
          fetchBusLocations();

          // Refresh bus locations every 30 seconds
          setInterval(fetchBusLocations, 15000);

          function fetchBusLocations() {{
            var url = "https://api-v3.mbta.com/vehicles?api_key=9c9841081e974e48971da86c982f61be";
            var MBTARequest = new XMLHttpRequest();
            MBTARequest.open("GET", url, true);
            var self = this;
            for (let i = 0; i < markers.length; i++) {{
              markers[i].setMap(null);
            }}
            MBTARequest.onreadystatechange = function() {{
              var data = this.response;//JSON.parse(this.response);
              if(data != ""){{
                data = JSON.parse(data);
              }}
              if (this.readyState === 4) {{
                if (this.status === 200) {{
                  var route = {!r};
                  for (var i = 0; i < data.data.length; i++) {{
                    var bus = data.data[i];
                    if(bus.relationships.route.data.id == route){{
                      var latLng = new google.maps.LatLng(bus.attributes.latitude, bus.attributes.longitude);
                      var marker = new google.maps.Marker({{
                        position: latLng,
                        map: map,
                        title: route
                      }});
                      markers.push(marker);
                    }}
                  }}
                }}
              }}
            }};
            MBTARequest.send();
          }}
        }}
        initMap();
      </script>
    </body>
  </html>
  """
  html = html.format(busRoute)
  with open("mbta_bus_tracker.html", "w") as file:
    file.write(html)
  webbrowser.open("mbta_bus_tracker.html")

# Open the HTML file in a web browser
if __name__ == "__main__":
  main(sys.argv[1])