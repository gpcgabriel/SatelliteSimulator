from Components import ComponentManager
from random import randint
from Components import ComponentManager
from general_utilities import num_steps, path_log
from Service_allocation_algorithms import (
    best_fit_allocation,
    less_distance_allocation,
    random_allocation,
    simple_allocation,
    best_exposure_time
)

if __name__ == "__main__":
    cm = ComponentManager()

    # Configuration settings
    num_satellites = 140

    service_min_service_duration = 2
    service_max_service_duration = 10
    service_min_cpu = 20
    service_max_cpu = 70
    service_min_memory = 30
    service_max_memory = 60
    
    min_services_per_step = 20
    max_services_per_step = 70

    # Create satellites
    cm.create_satellites(num_satellites)

    # Define the allocation algorithms
    allocation_algorithms = [
        best_fit_allocation,
        less_distance_allocation,
        random_allocation,
        simple_allocation,
        best_exposure_time
    ]

    # Generate random start times for services
    service_starts = [
        i for i in range(num_steps - 2 * service_max_service_duration)
        for _ in range(randint(min_services_per_step, max_services_per_step))
    ]
    
    num_services = len(service_starts)

    # Generate random demands for services
    service_demands = [
        {'cpu': randint(service_min_cpu, service_max_cpu), 'memory': randint(service_min_memory, service_max_memory)}
        for _ in range(num_services)
    ]

    # Define service coordinates (empty for now)
    service_coordinates = [()]

    # Generate random provisioned times for services
    service_service_durations = [
        randint(service_min_service_duration, service_max_service_duration)
        for _ in range(num_services)
    ]

    # Create services in the simulator
    cm.create_services(
        num_services=num_services,
        starts=service_starts,
        demands=service_demands,
        coordinates=service_coordinates,
        services_durations=service_service_durations
    )
    
    # cm.create_services(
    #     num_services=2
    # )

    # Initialize and start the simulator
    cm.initialize_simulator(algorithms=allocation_algorithms, num_executions=10)
    cm.start_simulator()

    print("\nDONE!")
