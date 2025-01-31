from random import choice
from .lambda_functions import distance as dst
from general_utilities import sat_range

def random_allocation(step, satellites : list, services : list):
    for service in services:
        sats_capacity = {}
        for sat in satellites:
            if dst.distance(service.coordinates, sat.coordinates[step]) < sat_range:
                if sat.capacity['cpu'] >= service.demand['cpu'] and sat.capacity['memory'] >= service.demand['memory']:
                    sats_capacity.update({sat.id: sat.capacity})
        
        sat_in_region = list(sats_capacity.keys())
        if sat_in_region:
            satid = choice(sat_in_region)
            selected = [sat for sat in satellites if sat.id == satid][0]

            if (service.satellite and service.satellite.id != selected.id) or not service.satellite:
                service.provision(selected, step)