from .lambda_functions import distance as dst
from .lambda_functions import has_capacity_to_host as hcth
from general_utilities import sat_range

def search(service, satellites, step) -> object:
    selected = None

    for sat in satellites:
        if dst.distance(service.coordinates, sat.coordinates[step]) < sat_range:
            if selected:
                if hcth.has_capacity_to_host(service, sat) and sat.capacity['cpu'] < selected.capacity['cpu'] and sat.capacity['memory'] < selected.capacity['memory']:
                    selected = sat
            else:
                if hcth.has_capacity_to_host(service, sat):
                    selected = sat
    return selected

def simple_allocation(step, satellites, services):
    for service in services:
        selected = search(service, satellites, step)
        if selected:
            if (service.satellite and service.satellite.id != selected.id) or not service.satellite:
                service.provision(selected, step)