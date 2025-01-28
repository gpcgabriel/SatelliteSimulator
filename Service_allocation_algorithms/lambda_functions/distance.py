from geopy.distance import geodesic
distance = lambda service_coordinates, satellite_coordinates: geodesic(service_coordinates, satellite_coordinates).kilometers