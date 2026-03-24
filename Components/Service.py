from general_utilities import default_coordinates, sat_range
from geopy.distance import geodesic
from Components.Metrics import Metrics

class Service:
    instances = []
    num_services = 0

    def __init__(self, start: int=0, demand: dict=None, coordinates: tuple=(), service_duration: int=1) -> None:
        self.demand = demand if demand else {'cpu': 50, 'memory': 50}
        self.coordinates = coordinates if coordinates else default_coordinates
        self.satellites = []
        self.satellite_demands = {}
        self.service_duration = service_duration if service_duration else 1
        self.provisioned_time = self.service_duration
        self.status = 'created'
        self.start = start if start else 0
        self.end = None
        self.history = {}
        self.migration_flag = False
        self.id = __class__.num_services + 1
        __class__.instances.append(self)
        __class__.num_services += 1

    @property
    def satellite(self):
        return self.satellites[0] if self.satellites else None

    @satellite.setter
    def satellite(self, value):
        pass

    def update_history(self, id, start, end) -> None:
        self.history.update({ 
            id : {
                'start': start,
                'end': end
            }
        })

    def provision(self, satellites_input, step, demand_distribution=None) -> None:
        new_satellites = satellites_input if isinstance(satellites_input, list) else [satellites_input]
        
        if self.satellites:
            for sat in list(self.satellites):
                if sat not in new_satellites:
                    self.stop_service(sat.id, step)
                    self.migration_flag = True
            
            if self.migration_flag:
                self.start = step
        
        for i, sat in enumerate(new_satellites):
            if sat not in self.satellites:
                self.update_history(sat.id, step, None)
                allocated_demand = demand_distribution[i] if demand_distribution else self.demand.copy()
                self.satellite_demands[sat.id] = allocated_demand
                
                original_demand = self.demand
                self.demand = allocated_demand
                sat.provision_service(self)
                self.demand = original_demand
                
                self.satellites.append(sat)
        
        self.status = 'provisioning'
        
        if self.migration_flag:
            Metrics.metrics.set_migration(self.id)
            self.migration_flag = False
        else:
            Metrics.metrics.set_provisioning(self.id)

    def stop_service(self, id, step) -> None:
        sat_to_stop = next((s for s in self.satellites if s.id == id), None)
        if sat_to_stop:
            allocated_demand = self.satellite_demands.pop(id, self.demand)
            sat_to_stop.stop_service(self.id, allocated_demand, step)
            
            if id in self.history:
                self.history[id]['end'] = step
                
            self.satellites.remove(sat_to_stop)
            
        if not self.satellites:
            self.status = 'stopped'
            self.provisioned_time = self.service_duration

    def in_range(self, sat_coordinates) -> bool:
        return (geodesic(self.coordinates, sat_coordinates).kilometers) < sat_range

    def process_service(self, step) -> None:
        if not self.satellites:
            return
        
        if step < self.start:
            return

        if self.provisioned_time < 1:
            self.end = step
            for sat in list(self.satellites):
                self.stop_service(sat.id, step)
            Metrics.metrics.set_end_service(self.id)
            self.status = 'finished'
            return
        
        out_of_range_sats = []
        for sat in self.satellites:
            if step < len(sat.coordinates):
                if not self.in_range(sat.coordinates[step+1]) and not self.provisioned_time == 1:
                    self.status = "migrating"

            if not self.in_range(sat.coordinates[step]):
                out_of_range_sats.append(sat)
        
        for sat in out_of_range_sats:
            self.stop_service(sat.id, step)
            Metrics.metrics.set_interrupted(self.id)
            
        if not self.satellites:
            self.end = step
            self.status = 'finished'
            return
                
        self.provisioned_time -= 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "demand": self.demand,
            "start": self.start,
            "provisioned_time": self.provisioned_time,
            "status": self.status,
            "satellites": [sat.to_dict() for sat in self.satellites]
        }

    @classmethod
    def show_services(cls, id=None):
        for i in cls.instances:
            if id and i.id != id:
                continue
            print(f'id: ', i.id)
            print(f'duration: ', getattr(i, 'duration', None))
            print(f'demand: ', i.demand)
            print(f'satellites: ', [sat.id for sat in i.satellites])
            print(f'provisioned time: ', i.provisioned_time)
            print(f'start: ', i.start)
            print(f'end: ', i.end)
            print(f'history: ', i.history)
            print('\n')
            if id:
                break