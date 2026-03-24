import random
from .lambda_functions import distance as dst
from general_utilities import sat_range

def calculate_cost(chromosome, satellites_dict, service, step):
    total_cost = 0
    allocated_demands = {sat_id: {'cpu': 0, 'memory': 0} for sat_id in set(chromosome)}
    
    subtask_cpu = service.demand['cpu'] / len(chromosome)
    subtask_mem = service.demand['memory'] / len(chromosome)
    
    for sat_id in chromosome:
        sat = satellites_dict[sat_id]
        d = dst.distance(service.coordinates, sat.coordinates[step])
        total_cost += d
        allocated_demands[sat_id]['cpu'] += subtask_cpu
        allocated_demands[sat_id]['memory'] += subtask_mem
        
    for sat_id, demand in allocated_demands.items():
        sat = satellites_dict[sat_id]
        if sat.capacity['cpu'] < demand['cpu'] or sat.capacity['memory'] < demand['memory']:
            total_cost += 1000000 
            
    return total_cost

def lcmga_allocation(step, satellites, services, num_subtasks=4, pop_size=20, generations=10):
    for service in services:
        available_sats = [sat for sat in satellites if dst.distance(service.coordinates, sat.coordinates[step]) < sat_range]
        
        if not available_sats:
            continue
            
        satellites_dict = {sat.id: sat for sat in available_sats}
        available_ids = list(satellites_dict.keys())
        
        population = [[random.choice(available_ids) for _ in range(num_subtasks)] for _ in range(pop_size)]
        
        for _ in range(generations):
            fitness = []
            for chromo in population:
                cost = calculate_cost(chromo, satellites_dict, service, step)
                fitness.append((cost, chromo))
            
            fitness.sort(key=lambda x: x[0])
            
            survivors = [x[1] for x in fitness[:pop_size//2]]
            
            next_gen = survivors.copy()
            while len(next_gen) < pop_size:
                p1, p2 = random.sample(survivors, 2)
                crossover_point = random.randint(1, num_subtasks-1)
                child = p1[:crossover_point] + p2[crossover_point:]
                next_gen.append(child)
                
            for chromo in next_gen:
                if random.random() < 0.1:
                    mutate_idx = random.randint(0, num_subtasks-1)
                    chromo[mutate_idx] = random.choice(available_ids)
                    
            population = next_gen
            
            fitness = []
            for chromo in population:
                cost = calculate_cost(chromo, satellites_dict, service, step)
                fitness.append((cost, chromo))
            fitness.sort(key=lambda x: x[0])
            
            best_cost = fitness[0][0]
            best_chromosome = fitness[0][1]
            
            if best_cost >= 1000000:
                continue
            
            selected_satellites_set = list(set(best_chromosome))
            selected_satellites = [satellites_dict[sid] for sid in selected_satellites_set]
            
            subtask_cpu = service.demand['cpu'] / num_subtasks
            subtask_mem = service.demand['memory'] / num_subtasks
            
            demand_distribution = []
            for sat in selected_satellites:
                count = best_chromosome.count(sat.id)
                demand_distribution.append({
                    'cpu': subtask_cpu * count,
                    'memory': subtask_mem * count
                })
                
            current_sat_ids = sorted([s.id for s in service.satellites])
            new_sat_ids = sorted([s.id for s in selected_satellites])
            
            if current_sat_ids != new_sat_ids or not service.satellites:
                service.provision(selected_satellites, step, demand_distribution)