class Metrics:
    metrics = None
    
    def __init__(self) -> None:
        self.total_demand = {"cpu": 0, "memory": 0}
        self.used_capacity = {}
        self.migrations = {}
        self.provisioned = []
        self.provisioning = []
        self.unprovisioned = []
        self.end_services = []

        if not __class__.metrics:
            __class__.metrics = self

    def set_total_demand(self, demand) -> None:
        self.total_demand["cpu"] += demand['cpu']
        self.total_demand['memory'] += demand['memory']

    def set_demand(self, id, capacity) -> None:
        if id in self.used_capacity:
            self.used_capacity[id]['cpu'] += capacity['cpu']
            self.used_capacity[id]['memory'] += capacity['memory']
        else:
            self.used_capacity[id] = {"cpu": capacity['cpu'], "memory": capacity['memory']}
        
        self.set_total_demand(capacity)

    def remove_demand(self, id, capacity) -> None:
        if id in self.used_capacity:
            self.used_capacity[id]['cpu'] -= capacity['cpu']
            self.used_capacity[id]['memory'] -= capacity['memory']

    def clear_migrations(self) -> None:
        self.migrations = {}

    def set_migration(self, id) -> None:
        if id in self.migrations:
            self.migrations[id] += 1
        else:
            self.migrations[id] = 1

    def set_provisioned(self, service_id: int) -> None:
        if service_id in self.end_services:
            return
        if service_id in self.unprovisioned:
            self.unprovisioned.remove(service_id)
        if service_id in self.provisioning:
            self.provisioning.remove(service_id)
        if service_id not in self.provisioned:
            self.provisioned.append(service_id)

    def set_unprovisioned(self, service_id: int) -> None:
        if service_id in self.end_services:
            return
        if service_id in self.provisioning:
            self.provisioning.remove(service_id)
        if service_id in self.provisioned:
            self.provisioned.remove(service_id)
        if service_id not in self.unprovisioned:
            self.unprovisioned.append(service_id)
        
    def set_provisioning(self, service_id: int) -> None:
        if service_id in self.end_services:
            return
        if service_id in self.provisioned:
            self.provisioned.remove(service_id)
        if service_id in self.unprovisioned:
            self.unprovisioned.remove(service_id)
        if service_id not in self.provisioning:
            self.provisioning.append(service_id)

    def set_end_service(self, service_id) -> None:
        if service_id in self.provisioned:
            self.provisioned.remove(service_id)
        if service_id in self.unprovisioned:
            self.unprovisioned.remove(service_id)
        if service_id in self.provisioning:
            self.provisioning.remove(service_id)

        if service_id not in self.end_services:
            self.end_services.append(service_id)

    def get_metrics(self, services=[]) -> dict:
        return {
            # "total": {
            #     "total_cpu": self.total_demand['cpu'],
            #     "total_memory": self.total_demand['memory'],
            # },
            # "used_capacity": [{'cpu': self.used_capacity[i]['cpu'], 'memory': self.used_capacity[i]['memory']} for i in self.used_capacity],
            "data": {
                "provisioned": self.provisioned.copy(),
                "unprovisioned": self.unprovisioned.copy(),
                "provisioning": self.provisioning.copy(),
                "end_services": self.end_services.copy(),
            },
            "migrations": self.migrations.copy(),
            "services": [svc.to_dict() for svc in services]
        }

    def clear_metrics(self) -> None:
        self.total_demand = {"cpu": 0, "memory": 0}
        self.used_capacity = {}
        self.migrations = {}
        self.provisioned.clear()
        self.provisioning.clear()
        self.unprovisioned.clear()
        self.end_services.clear()
        __class__.metrics = None