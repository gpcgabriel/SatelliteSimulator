from .lambda_functions import distance as dst
from .lambda_functions import has_capacity_to_host as hcth
from general_utilities import sat_range

def get_exposed_time(service, satellite, current_step) -> int:
    count = 0
    for coordinate in satellite.coordinates[current_step:]:
        if not service.in_range(coordinate):
            return count
        count += 1

def sort_services_by_time(services: list):
    sorted_services = {}
    result = []

    for service in services:
        if not sorted_services.get(service.provisioned_time):
            sorted_services[service.provisioned_time] = []
        sorted_services[service.provisioned_time].append(service)
    
    result = []
    for key in sorted(sorted_services.keys()):
        result.extend(sorted_services[key])
    
    return result

def best_exposure_time(step, satellites : list, services : list):

    services = sort_services_by_time(services)
    for service in services:
        selected = None
        exposed_time = None
        for sat in satellites:
            if dst.distance(service.coordinates, sat.coordinates[step]) < sat_range:
                if not selected and hcth.has_capacity_to_host(service, sat):
                    selected = sat
                    exposed_time = get_exposed_time(service, sat, step)

                else:
                    if hcth.has_capacity_to_host(service, sat) and get_exposed_time(service, sat, step) > exposed_time:
                        selected = sat
                        exposed_time = get_exposed_time(service, sat, step)
        if selected:
            if (service.satellite and service.satellite.id != selected.id) or not service.satellite:
                service.provision(selected, step)
