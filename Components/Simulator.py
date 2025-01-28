from general_utilities import num_steps, algorithms, path_log
from Components.Metrics import Metrics
from Components.ComponentManager import ComponentManager
from Components.Satellite import Satellite
from Components.Service import Service

class Simulator:
    
    def __init__(self):
      self.satellites = []
      self.services = []
      self.step = 0

    def initialize(self, satellites, services) -> None:
        self.satellites = [ Satellite('', sat.coordinates, {}) for sat in satellites ]
        self.services = [ Service(srv.start, srv.demand.copy(), srv.coordinates, srv.provisioning_duration) for srv in services ]

    def remove_finished_services(self) -> None:
        for service in self.services:
            if service.status == 'finished':
                self.services.remove(service)

    def allocate_services(self, algorithm) -> any:
        # return algorithm(self.step, self.satellites, self.services)
        status_to_allocate = ["unprovisioned", "created"]
        unprovided_services = [ s for s in self.services if s.satellite == None and s.status in status_to_allocate ]
        return algorithm(self.step, self.satellites, unprovided_services)

    def process_services(self):
        for service in self.services:
            service.process_service(self.step)

    def set_unprovisioned(self):
        for service in self.services:
            self.metrics.set_unprovisioned(service.id)

    def run(self) -> None:
        data = {}

        for alg in algorithms:
            data[alg.__name__] = {}
            self.metrics = Metrics()

            # Setting all services as 'unprovisioned'
            self.set_unprovisioned()

            for self.step in range(0, num_steps):

                # Checks if the satellite is coming out of range, if its finished...
                self.process_services()

                print(f"============ {alg.__name__.upper()}: {self.step} ============")
                for i, service in enumerate(self.services):
                    print(f"[{service.id}]: STATUS: {service.status}   TIME REMAINING: {service.provisioning_duration}")
                print()

                # Try to allocate unallocated services
                self.allocate_services(alg)

                data[alg.__name__][self.step] = self.metrics.get_metrics(self.services)
                
                self.remove_finished_services()
                self.metrics.clear_migrations()
            
            print()
            print()
            print()

            self.services = [ Service(srv.start, srv.demand.copy(), srv.coordinates, srv.provisioning_duration) for srv in ComponentManager.services ]
            self.metrics.clear_metrics()

        ComponentManager.write_log(data, path_log)
        ComponentManager.plot_graphics(path_log)