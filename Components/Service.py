from general_utilities import default_coordinates, sat_range, num_steps
from geopy.distance import geodesic
from Components.Metrics import Metrics

class Service():
    instances = []
    num_services = 0

    def __init__(self, start: int=0, demand: dict={}, coordinates: tuple=(), provisioned_time: int=1) -> None:

        if demand:
            self.demand = demand
        else:
            self.demand = {'cpu': 50, 'memory': 50}

        if coordinates:
            self.coordinates = coordinates
        else:
            self.coordinates = default_coordinates

        self.satellite = None
        self.service_duration = provisioned_time if provisioned_time else 1
        self.provisioned_time = self.service_duration
        self.status = 'created'
        self.start = start if start else 0
        self.end = None
        self.history = {}
        self.migration_flag = False

        self.id = __class__.num_services+1
        __class__.instances.append(self)
        __class__.num_services += 1

    def update_history(self, id, start, end) -> None:
        self.history.update({ 
            id : {
                'start': start,
                'end': end
            }
        })

    def provision(self, satellite, step) -> None:
        """
            Se o serviço já estiver associado a um satélite, "stopa" o serviço 
            anterior (self.satellite) e inicia o provisionamento do 
            próximo satellite (migração)
        """
        if self.satellite:
            self.stop_service(self.satellite.id, step)
            Metrics.metrics.set_unprovisioned(self.id)
            self.start = step # Altera o start para a nova provisão
            self.migration_flag = True
        
        self.update_history(satellite.id, step, None) # Registra o início do provisionamento

        satellite.provision_service(self)
        self.satellite = satellite
        self.status = 'provisioning'
        Metrics.metrics.set_provisioning(self.id)
        if self.migration_flag:
            Metrics.metrics.set_migration(self.id)
            self.migration_flag = False

    def stop_service(self, id, step) -> None:
        self.satellite.stop_service(self.id, self.demand, step)
        self.status = 'stopped'
        self.update_history(id, self.start, step)
        self.satellite = None
        self.provisioned_time = self.service_duration

    def in_range(self, sat_coordinates) -> bool:
        return (geodesic(self.coordinates, sat_coordinates).kilometers) < sat_range

    def process_service(self, step) -> None:

        # Checking if the process is allocated to a satellite
        if self.satellite == None:
            return
        
        if step < self.start:
            return

        # Stopping process that achieved their time limit
        if self.provisioned_time < 1:
                self.end = step
                self.stop_service(self.satellite.id, step)
                Metrics.metrics.set_end_service(self.id)
                self.status = 'finished'
                return
        
        # If satellite is coming out of range, it finds a new one to migrate
        if step < num_steps:
            if not self.in_range(self.satellite.coordinates[step+1]) and not self.provisioned_time == 1:
                Metrics.metrics.set_migration(self.id)
                self.status = "unprovisioned"

        # Checking if the allocated satellite is out of range
        if not self.in_range(self.satellite.coordinates[step]):
            self.stop_service(self.satellite.id, step)
            Metrics.metrics.set_unprovisioned(self.id)
            return
                
        self.provisioned_time -= 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "demand": self.demand,
            "start": self.start,
            "provisioned_time": self.provisioned_time,
            "satellite": self.satellite.to_dict() if self.satellite else []
        }

    @classmethod
    def show_services(cls, id = None):
        for i in cls.instances:
            if id and i.id == id:
                print(f'id: ',i.id)
                print(f'duration: ',i.duration)
                print(f'demand: ',i.demand)
                print(f'satellites: ',i.satellites)
                print(f'provisioned time: ',i.provisioned_time)
                print(f'start: ',i.start)
                print(f'end: ',i.end)
                print(f'history: ',i.history)
                print('\n')
                break
            else:
                print(f'id: ',i.id)
                print(f'duration: ',i.duration)
                print(f'demand: ',i.demand)
                print(f'provisioned time: ',i.provisioned_time)
                print(f'start: ',i.start)
                print(f'end: ',i.end)
                print(f'history: ',i.history)
                print('\n')
                break
