# Constants and Variables for the Simulator
sat_range = 2000.0  # Satellite communication range in kilometers
earth_radius = 6371.0  # Average radius of the Earth in kilometers

from Service_allocation_algorithms import (
    best_fit_allocation,
    less_distance_allocation,
    random_allocation,
    simple_allocation,
    best_exposure_time,
    improved_best_exposure_time,
    improved_best_fit
)

# Constants and Variables for the Algorithm
num_steps = 30  # Total number of steps in the simulation
default_coordinates = (-24.7875286, -55.768967)  # Default coordinates (latitude, longitude) when no coordinates are provided


# File Paths for Data and Dataset
default_path_log = './data/data.json' # Default path for the log file
default_simulation_config_path = './dataset/simulation.json' # Default path for the simulation configuration file
satellites_dataset_path = './dataset/satellites.json' # Path to the satellite dataset

default_algorithms = [
    best_fit_allocation,
     less_distance_allocation,
     random_allocation,
     simple_allocation,
     best_exposure_time,
     improved_best_exposure_time,
     improved_best_fit
] # Default allocation algorithms (you should changes this on the main.py file)
