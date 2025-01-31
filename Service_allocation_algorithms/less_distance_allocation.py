from .lambda_functions import distance as dst
from .lambda_functions import less_distance as ld
from .lambda_functions import has_capacity_to_host as hcth
from general_utilities import sat_range

def less_distance_allocation(step, satellites : list, services : list):
    for service in services:
        selected = None
        for sat in satellites:
            if dst.distance(service.coordinates, sat.coordinates[step]) < sat_range:
                if not selected and hcth.has_capacity_to_host(service, sat):
                    selected = sat
                else:
                    if hcth.has_capacity_to_host(service, sat) and ld.less_distance(sat.coordinates[step], selected.coordinates[step]):
                        selected = sat

        if selected:
            if (service.satellite and service.satellite.id != selected.id) or not service.satellite:
                service.provision(selected, step)