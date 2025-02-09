from general_utilities import default_path_log, num_steps, default_algorithms
from Components.Metrics import Metrics
from Components.ComponentManager import ComponentManager
from Components.Satellite import Satellite
from Components.Service import Service
from Service_allocation_algorithms import best_fit_allocation, simple_allocation, best_exposure_time

class Simulator:
    
    def __init__(self):
      self.satellites = []
      self.services = []
      self.step = 0
      self.algorithms = []
      self.num_executions = None
      self.verbose = False
      self.path_log = None

    def initialize(self, satellites, services, algorithms = [], num_executions = None, verbose: bool=False, output: str=default_path_log) -> None:
        self.satellites = [ Satellite('', sat.coordinates, {}) for sat in satellites ]
        self.services = [ Service(srv.start, srv.demand.copy(), srv.coordinates, srv.provisioned_time) for srv in services ]
        self.algorithms = algorithms or default_algorithms
        self.num_executions = num_executions or 1
        self.verbose = verbose or False
        self.path_log = output or default_path_log

    def remove_finished_services(self) -> None:
        for service in self.services:
            if service.status == 'finished':
                self.services.remove(service)

    def allocate_services(self, algorithm) -> any:
        # return algorithm(self.step, self.satellites, self.services)
        status_to_allocate = ["unprovisioned", "created", "migrating"]
        unprovided_services = [ s for s in self.services if s.start <= self.step and s.status in status_to_allocate ]
        return algorithm(self.step, self.satellites, unprovided_services)

    def process_services(self):
        for service in self.services:
            service.process_service(self.step)

    def run(self) -> None:
        data = []

        for execution in range(self.num_executions):
            data.append({})

            for alg in self.algorithms:
                data[execution][alg.__name__] = {}
                self.metrics = Metrics()

                print(f"============ EXECUTION {execution} --- {alg.__name__.upper()} ============")
                for self.step in range(0, num_steps):

                    # Checks if the satellite is coming out of range, if its finished...
                    self.process_services()

                    # Showing execution steps
                    if self.verbose:
                        print(f"============ EXECUTION {execution} --- {alg.__name__.upper()}: {self.step} ============")
                        for i, service in enumerate(self.services):
                            if service.start < self.step:
                                continue 

                            print(f"[{service.id}]: STATUS: {service.status}   TIME REMAINING: {service.provisioned_time}     START: {service.start}")
                        print()

                    # Try to allocate unallocated services
                    self.allocate_services(alg)

                    # Getting relevant metrics
                    for srv in self.services:

                        if self.step < srv.start:
                            continue

                        # if not srv.status == 'migrating' and not srv.status == 'created':
                        #     continue

                        if srv.status == 'created':
                            Metrics.metrics.set_unprovisioned(srv.id)
                            
                        for sat in self.satellites:    
                            if srv.in_range(sat.coordinates[self.step]) and srv.demand['cpu'] <= sat.capacity['cpu'] and srv.demand['memory'] <= sat.capacity['memory']:
                                Metrics.metrics.set_available_satellite(srv.id, sat)

                    data[execution][alg.__name__][self.step] = self.metrics.get_metrics(self.services)
                    
                    self.remove_finished_services()

                    self.metrics.clear_available_satellites()
                    # self.metrics.clear_migrations()
                
                if self.verbose:
                    print()
                    print()
                    print()

                self.services = [ Service(srv.start, srv.demand.copy(), srv.coordinates, srv.provisioned_time) for srv in ComponentManager.services ]
                self.satellites = [ Satellite('', sat.coordinates, {}) for sat in ComponentManager.satellites ]
                self.metrics.clear_metrics()

            ComponentManager.write_log(data, self.path_log)
            ComponentManager.plot_graphics(self.path_log)