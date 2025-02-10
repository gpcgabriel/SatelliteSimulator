from Satellite import Satellite
from Controller import Controller
import requests
from collections import deque

class Region:
    # Chave de acesso à API -> (Pedro) KTWK48-4U9L6A-4CMGWN-583R
    _API_KEY_QUEUE = deque(['TMTGZD-B49AEL-YEHRTA-5897', 'KTWK48-4U9L6A-4CMGWN-583R'])

    def __init__(self,
        coordinates: tuple, search_radius: int, category_id: int
    ) -> object:
        self.coordinates = coordinates
        self.search_radius = search_radius # Em graus. Ex.:(45)
        self.category_id = category_id
        self.satellites = {} # Satellites na região
        self.satellite_stack=[]
        self.controller = Controller()

    def get_satellite(self, id:int) -> Satellite:
        return self.satellites.get(id) if id in self.satellites else None

    # Lista de coordenadas dos satélites
    def get_list_satellite_coordinates(self) -> list:
        coordinates = []
        for sat in self.satellites:
            coordinates.append({"satid":sat['satid'],"satlat":sat['satlat'],"satlng":sat['satlng'],"satalt":sat['satalt']})
        return coordinates

    # Adiciona satélites na região
    def set_satellites(self, satellites):
        self.satellites = satellites

    # Lista de satélites na resposta
    def get_satellite_list_in_response(self, response):
        return response.json().get('above')
    
    # Adiciona satélites na pilha (indices únicos)
    def set_different_satellite_in_stack(self, satellites):
        for satellite in satellites:
            if satellite not in self.satellite_stack:
                self.satellite_stack.append(satellite)

    def print_satellites_in_stack(self):
        for satellite in self.satellite_stack:
            print(f'{satellite}\n')

    def find_satellites(self, coordinates=''):
        self.coordinates = coordinates if coordinates != '' else self.coordinates
        try:
            response = requests.get(
                url=f'https://api.n2yo.com/rest/v1/satellite/above/{self.coordinates[0]}/{self.coordinates[1]}/{self.coordinates[2]}/{self.search_radius}/{self.category_id}/&apiKey={self.__class__._API_KEY_QUEUE[0]}'
            )
            return response
        except Exception as e:
            with open('Error.txt', 'a') as err:
                err.write(f'{self.controller.get_datetime()} -----> {e} \n')

    def change_key(self):
        if self._API_KEY_QUEUE:  # Verifica se a fila não está vazia
            rotated_key = self._API_KEY_QUEUE.popleft()
            self._API_KEY_QUEUE.append(rotated_key)
        else:
            return None  # Retorna None se a fila estiver vazia