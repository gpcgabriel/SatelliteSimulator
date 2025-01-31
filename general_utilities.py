from Service_allocation_algorithms import best_fit_allocation, less_distance_allocation, random_allocation, simple_allocation, best_exposure_time

# Variáveis a serem utilizadas no algoritmo
num_satellites = 200
num_services = 20
num_steps = 20
default_coordinates = (-24.7875286, -55.768967)
earth_radius = 6371.0

service_duration = 3
provisioning_duration = 10

sat_range = 2000.0
raio_terra = 6371.0  # Raio médio da Terra em km

path_log = './data/data.json'
path_dataset = './dataset/dataset.json'

# Algoritmos utilizados
algorithms = [best_fit_allocation, less_distance_allocation, random_allocation, simple_allocation, best_exposure_time]
# algorithms = [best_exposure_time]