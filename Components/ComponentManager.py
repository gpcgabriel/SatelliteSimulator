from Components import *
from Components.Output import Output
from json import dump, load
from general_utilities import path_dataset
from os import path, mkdir

class ComponentManager():
    instance = None
    simulator = None
    satellites = []
    services = []

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(ComponentManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            # Inicialização da instância
            self.initialized = True
    
    @classmethod
    def initialize_simulator(cls) -> None:
        # Importação tardia de Simulator para evitar dependência circular
        from .Simulator import Simulator
        cls.simulator = Simulator()
        cls.simulator.initialize(cls.satellites, cls.services)

    @classmethod
    def start_simulator(cls) -> None:
        cls.simulator.run()

    @classmethod
    def get_coordinates(cls, num_satellites) -> dict:
        dataset = cls.read_document(path_dataset)
        sat_ids = []
        for satellite in dataset[0]["satellites"]:
            if len(sat_ids) >= num_satellites:
                break
            if satellite["satid"] not in sat_ids:
                sat_ids.append(satellite["satid"])
        
        coordinates = {}
        for entry in dataset:
            for satellite in entry["satellites"]:
                sat_id = satellite["satid"]
                if sat_id in sat_ids:
                    coords = (satellite["satlat"], satellite["satlng"])
                    if sat_id not in coordinates:
                        coordinates[sat_id] = []
                    coordinates[sat_id].append(coords)
        
        return coordinates

    @classmethod
    def create_satellites(cls, num_satellites) -> None:
        coordinates = cls.get_coordinates(num_satellites)
        for i in coordinates:
            cls.satellites.append(Satellite('', coordinates[i], {}))
    
    @staticmethod
    def complete_list_cyclically(lst, target_length):
        if not lst:
            return [None] * target_length
        
        return [lst[i % len(lst)] for i in range(target_length)]

    @classmethod
    def create_services(cls, num_services, starts: list[int]=[0], demands: list[dict]=[{}], coordinates: list[tuple]=[()], provisioned_times: list[int]=[1]) -> None:

        starts = ComponentManager.complete_list_cyclically(starts, num_services)
        demands = ComponentManager.complete_list_cyclically(demands, num_services)
        coordinates = ComponentManager.complete_list_cyclically(coordinates, num_services)
        provisioned_times = ComponentManager.complete_list_cyclically(provisioned_times, num_services)
        
        for i in range(0, num_services):
            cls.services.append(Service(starts[i], demands[i], coordinates[i], provisioned_times[i]))

    @staticmethod
    def write_log(data: dict, filename: str='log', indent: int=4) -> None:
        """"
        Writes a dictionary to a log file in JSON format.

        Args:
            data (dict): The data to write to the log file.
            filename (str): The name of the file to write to. Defaults to 'log'.
            indent (int): The indentation level for the JSON file. Defaults to 4.

        Returns:
            None
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        if not path.exists('./data'):
            mkdir('./data')

        with open(filename, 'w') as file:
            dump(data, file, indent=indent)
            file.write('\n')

    @staticmethod
    def read_document(directory: str) -> dict:
        """
        Reads and parses a JSON file.

        Args:
            directory (str): The file path of the JSON file.

        Returns:
            dict: The parsed data from the JSON file.
        """
        with open(directory, 'r') as file:
            data = load(file)
            return data
        
    @classmethod
    def plot_graphics(cls, path) -> None:
        data = cls.read_document(path)
        Output.plot_graphics(data)
            