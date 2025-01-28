from matplotlib import pyplot as plt
from general_utilities import num_steps
import numpy as np
from json import dump
from os import path, mkdir

class Output:
    time = [i for i in range(0, num_steps)]
    colors = [
            'blue',     # Azul
            'red',      # Vermelho
            'green',    # Verde
            'cyan',     # Ciano
            'magenta',  # Magenta
            'yellow',   # Amarelo
            'black',    # Preto
            'white',    # Branco
            'gray',     # Cinza
            'orange',   # Laranja
            'purple',   # Roxo
            'brown',    # Marrom
            'pink',     # Rosa
            'gold',     # Ouro
            'beige',    # Bege
            'olive',    # Oliva
            'aqua',     # Aqua
            'navy'      # Navy
        ]

    @staticmethod
    def create_directory(directory: str) -> None:
        if not path.exists(directory):
            mkdir(directory)

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
        with open(filename, 'w') as file:
            dump(data, file, indent=indent)
            file.write('\n')

    @classmethod
    def get_end_services(cls, steps, step):
        return steps[step]['end_services']

    @classmethod
    def get_data(cls, algs):
        total_resources = []
        used_resources = []
        provisioned = []
        unprovisioned = []
        provisioning = []
        end_services = []
        migrations = []
        algorithms = {}

        for alg in algs:
            print(algs[alg])
            
        exit(1)
            # for steps in algs[alg]:
            #     total_resources.append(algs[alg][steps]['total'])
            #     used_resources.append(algs[alg][steps]['used_capacity'])
            #     provisioned.append(algs[alg][steps]['data']['provisioned'])
            #     unprovisioned.append(algs[alg][steps]['data']['unprovisioned'])
            #     provisioning.append(algs[alg][steps]['data']['provisioning'])
            #     end_services.append(algs[alg][steps]['data']['end_services'])
            #     migrations.append(algs[alg][steps]['migrations'])
            
            # algorithms[alg] = {'total_resources': total_resources, 'used_resources': used_resources, 'provisioned': provisioned,
            #                    'unprovisioned': unprovisioned, 'provisioning': provisioning, 'end_services': end_services, 
            #                    'migrations': migrations}
        
        return algorithms

    @classmethod
    def plot(cls, name, x_label, y_label, title):
        plt.xlabel(x_label)# Define o rótulo do eixo x
        plt.ylabel(y_label) # Define o rótulo do eixo y
        plt.title(title) # Define o título do gráfico
        plt.xticks(cls.time) # Fixa os índices do eixo x
        plt.tight_layout() # Ajusta o layout para evitar sobreposição de elementos
        
        title = title.lower().replace(' ', '_')
        cls.create_directory(f'./graphics/{name}') if name != '' else None
        
        plt.legend()
        plt.savefig(f'graphics/{name}/{title}', dpi=300)
        
    @classmethod
    def plot_total_resources(cls, data):
        pass        

    @classmethod
    def plot_used_resources(cls, data):
        pass

    @classmethod
    def plot_provisioned(cls, data):
        provisioned = []
        for alg in data:
            for value in data[alg]['provisioned']:
                provisioned.append(len(value))

        i=0
        plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
        for alg in data:
            plt.plot(cls.time, provisioned, color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)
            i+=1
        cls.plot('', 'Steps', 'Number of services', 'provisioned')

    @classmethod
    def plot_data(cls, data, name):
        i=0
        plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
        for alg in data:
            to_plot = []
            for step in data[alg]:
                to_plot.append(len(data[alg][step]['data'][name]))
            plt.plot(cls.time, to_plot.copy(), color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)
            i+=1
        cls.plot('', 'Steps', 'Number of services', name)
            
    @classmethod
    def plot_migrations(cls, data):
        migrations = []
        for alg in data:
            for mig in data[alg]['migrations']:
                migrations.append(len(mig))

        i=0
        plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
        for alg in data:
            plt.plot(cls.time, migrations, color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)
            i+=1
        cls.plot('', 'Steps', 'Number of services', 'migrations')

    @classmethod
    def plot_graphics(cls, data):
        #data = cls.get_data(algs)

        # Total de recursos
        # cls.plot_total_resources(algs)
        # Recursos utilizados (por step)
        # cls.plot_used_resources(data)

        # Dados de provisionamento
        cls.plot_data(data, 'unprovisioned')
        cls.plot_data(data, 'provisioned')
        cls.plot_data(data, 'provisioning')
        cls.plot_data(data, 'end_services')  

        # # Migrações
        # cls.plot_migrations(data)