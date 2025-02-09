from Components import ComponentManager
from random import randint
import argparse
from Components import ComponentManager
from general_utilities import num_steps, default_path_log, default_simulation_config_path
from Service_allocation_algorithms import (
    best_fit_allocation,
    less_distance_allocation,
    random_allocation,
    simple_allocation,
    best_exposure_time
)

def generate_services(min_duration, max_duration, min_cpu, max_cpu, min_memory, max_memory, min_services, max_services):
    """Generates random service parameters."""
    starts = [i for i in range(num_steps) for _ in range(randint(min_services, max_services))]
    num_services = len(starts)
    demands = [{'cpu': randint(min_cpu, max_cpu), 'memory': randint(min_memory, max_memory)} for _ in range(num_services)]
    durations = [randint(min_duration, max_duration) for _ in range(num_services)]
    coordinates = [() for _ in range(num_services)]  # Placeholder for service coordinates
    return num_services, starts, demands, coordinates, durations

if __name__ == "__main__":
    """Main function to initialize and run the satellite service allocation simulator."""
    
    parser = argparse.ArgumentParser(description="Low-Orbit Earth Satellite Simulation")
    parser.add_argument("-v", "--verbose", type=int, default=1, help="Verbosity level (default: 1)")
    parser.add_argument("-o", "--output", type=str, default=default_path_log, help="Path to exit JSON (default: specified in general_utilities.py)")
    parser.add_argument("-c", "--simulation-config", type=str, default=default_simulation_config_path, help="Path to the simulation configuration (default: specified in general_utilities.py)")

    args = parser.parse_args()

    # Create the component manager
    cm = ComponentManager()

    # Loading simulation configuration
    simulation_config = cm.read_document(args.simulation_config)

    # Extracting configuration settings
    satellites_config = simulation_config.get("satellites", {})
    services_config = simulation_config.get("services", {})

    # Define the allocation algorithms
    allocation_algorithms = [
        best_fit_allocation,
        less_distance_allocation,
        random_allocation,
        simple_allocation,
        best_exposure_time
    ]

    # Create satellites
    cm.create_satellites(num_satellites=satellites_config["max"], dataset_path=satellites_config["dataset_path"])

    # Generate random services according to the configuration settings
    num_services, services_starts, services_demands, services_coordinates, services_durations = generate_services(
        min_duration=services_config["duration"]["min"], 
        max_duration=services_config["duration"]["max"], 
        min_cpu=services_config["demand"]["cpu"]["min"], 
        max_cpu=services_config["demand"]["cpu"]["max"], 
        min_memory=services_config["demand"]["memory"]["min"], 
        max_memory=services_config["demand"]["memory"]["max"], 
        min_services=services_config["per_step"]["min"], 
        max_services=services_config["per_step"]["max"]
    )

    # Create services in the simulator
    cm.create_services(
        num_services=num_services,
        starts=services_starts,
        demands=services_demands,
        coordinates=services_coordinates,
        services_durations=services_durations
    )

    # Initialize and start the simulator
    cm.initialize_simulator(algorithms=allocation_algorithms, num_executions=1, output=args.output, verbose=args.verbose)
    cm.start_simulator()

    print("\nDONE!")
