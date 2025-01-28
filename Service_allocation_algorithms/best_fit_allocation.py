from .lambda_functions import has_capacity_to_host as hcth
from .lambda_functions import distance as dst

sat_range = 2000.0

def best_fit_allocation(step, satellites: list, services: list):
    for service in services:
        sats = [sat for sat in satellites if (dst.distance(service.coordinates, sat.coordinates[step]) < sat_range) and hcth.has_capacity_to_host(service, sat)]

        if sats:
            selected = min(sats, key=lambda satellite: satellite.capacity['memory'] + satellite.capacity['cpu'])
            if (service.satellite and service.satellite.id != selected.id) or not service.satellite:
                service.provision(selected, step)