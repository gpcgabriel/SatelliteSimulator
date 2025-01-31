from general_utilities import default_coordinates, num_steps, earth_radius
from Components.Metrics import Metrics
from random import randint
import math

class Satellite():
    instances = []
    num_satellites = 0
    
    def __init__(self, name: str='', coordinates: tuple=(), capacity: dict={}) -> None:
        self.coordinates = []
        if coordinates:
            self.coordinates = coordinates
        else:
            self.coordinates.append(self.create_coordinates())

        if capacity:
            self.capacity = capacity
        else:
            self.capacity = {'cpu': 100, 'memory': 100}

        self.total_capacity = self.capacity.copy()
        self.services = {}

        self.id = __class__.num_satellites + 1
        self.name = name if name else f'SAT_{self.id}'

        __class__.instances.append(self)
        __class__.num_satellites += 1

    @classmethod
    def get_satellite(cls, id: int) -> object:
        """
        Retrieves a satellite instance by its ID.

        Args:
            id (int): The ID of the satellite.

        Returns:
            object: The satellite instance with the specified ID, or None if not found.
        """
        return next((sat for sat in cls.get_all() if sat.id == id), None)

    @classmethod
    def get_all(cls):
        """
        Retrieves all satellite instances.

        Returns:
            list: A list of all satellite instances.
        """
        return cls.instances.copy()

    def calcular_distancia_haversine(self, lat1, lon1, lat2, lon2):
        """
        Calcula a distância entre dois pontos geográficos usando a fórmula do haversine.
        
        :param lat1: Latitude do ponto 1 (em graus).
        :param lon1: Longitude do ponto 1 (em graus).
        :param lat2: Latitude do ponto 2 (em graus).
        :param lon2: Longitude do ponto 2 (em graus).
        :return: Distância entre os dois pontos (em quilômetros).
        """

        # Converte diferenças de latitude e longitude de graus para radianos
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        # Fórmula do haversine
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return earth_radius * c

    def generate_initial_coordinates(self):
        lat_alvo, lon_alvo = default_coordinates
        # Velocidade do satélite em km/h
        sat_vel_km_h = 27000  # km/h
        
        # Conversão de graus para radianos
        lat_alvo_rad = math.radians(lat_alvo)
        lon_alvo_rad = math.radians(lon_alvo)

        # Escolhendo um ponto inicial simples (oposto ao alvo para simplificação)
        lat_inicial = -lat_alvo
        lon_inicial = (lon_alvo + 180) % 360 - 180  # Ajusta para intervalo [-180, 180]
        
        # Calculando a distância total
        distancia_total = self.calcular_distancia_haversine(lat_inicial, math.radians(lon_inicial), lat_alvo_rad, lon_alvo_rad)
        
        # Calculando o tempo total e o tempo por deslocamento
        tempo_total = distancia_total / sat_vel_km_h
        tempo_por_deslocamento = tempo_total / num_steps
        
        # Calculando a distância percorrida por deslocamento
        distancia_por_deslocamento = sat_vel_km_h * tempo_por_deslocamento
        angulo_por_deslocamento = distancia_por_deslocamento / (2 * math.pi * earth_radius) * 360  # graus
        
        # Calculando a longitude inicial ajustada
        lon_inicial_ajustada = (lon_alvo - num_steps * angulo_por_deslocamento) % 360
        if lon_inicial_ajustada > 180:  # Ajusta para intervalo [-180, 180]
            lon_inicial_ajustada -= 360
        
        return lat_alvo, lon_inicial_ajustada # A latitude é fixa

    def create_coordinates(self):
        # Coordenadas iniciais (um ponto real no mapa, ajustável)
        inicial = self.generate_initial_coordinates()
        
        # Coordenadas alvo
        alvo = (-24.7875286, -55.768967)
        
        # Calcula a distância total entre o ponto inicial e o alvo
        distancia_total = self.calcular_distancia_haversine(inicial[0], inicial[1], alvo[0], alvo[1])
        
        # Número de deslocamentos até atingir o alvo (máximo de 5)
        deslocamentos_ate_alvo = min(num_steps, randint(0,num_steps+1))
        
        # Trajetória inicial
        trajetoria = [inicial]
        
        # Incrementos em latitude e longitude até o alvo
        if deslocamentos_ate_alvo != 0:
            delta_lat = (alvo[0] - inicial[0]) / deslocamentos_ate_alvo
            delta_lon = (alvo[1] - inicial[1]) / deslocamentos_ate_alvo
        else:
            delta_lat = 0
            delta_lon = 0
        
        # Calcula os deslocamentos até o alvo
        for i in range(1, deslocamentos_ate_alvo + 1):
            nova_lat = inicial[0] + i * delta_lat
            nova_lon = inicial[1] + i * delta_lon
            trajetoria.append((nova_lat, nova_lon))
        
        # Continuar o movimento após atingir o alvo
        deslocamentos_restantes = num_steps - deslocamentos_ate_alvo
        for i in range(1, deslocamentos_restantes + 1):
            nova_lat = alvo[0] + i * delta_lat
            nova_lon = alvo[1] + i * delta_lon
            trajetoria.append((nova_lat, nova_lon))
        
        return trajetoria

    def provision_service(self, service):
        if service.demand['cpu'] > self.capacity['cpu'] or service.demand['memory'] > self.capacity['memory']:
            raise ValueError("Valor acima da capacidade")
        
        self.services.update({service.id : {
            'start' : service.history[self.id]['start'],
            'end' : None
        }})

        self.capacity['cpu'] -= service.demand['cpu']
        self.capacity['memory'] -= service.demand['memory']

        Metrics.metrics.set_demand(self.id, service.demand)

    def stop_service(self, service_id, demand, end):
        self.services[service_id]['end'] = end

        # Atualizando a capacidade do satélite
        self.capacity['cpu'] += demand['cpu']
        self.capacity['memory'] += demand['memory']

        Metrics.metrics.remove_demand(self.id, demand)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            #"coordinates": self.coordinates.copy(),
            "available_capacity": self.capacity.copy(),
            "total_capacity": self.total_capacity.copy()
        }
    
    @classmethod
    def show_satellites(cls, id = None):
        for i in cls.instances:
            if id and i.id == id:
                print(f'id: ',i.id)
                print(f'name: ',i.name)
                print(f'coordinates: ',i.coordinates)
                print(f'capacity: ',i.capacity)
                print(f'services: ',i.services)
                print('\n')
                break
            else:
                print(f'id: ',i.id)
                print(f'name: ',i.name)
                print(f'coordinates: ',i.coordinates)
                print(f'capacity: ',i.capacity)
                print(f'services: ',i.services)
                print('\n')