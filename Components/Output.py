from matplotlib import pyplot as plt
from general_utilities import num_steps
from json import dump
from os import path, makedirs

class Output:
    time = None
    colors = [
            'blue',
            'red',
            'green',
            'cyan',
            'magenta',
            'yellow',
            'black',
            'white',
            'gray',
            'orange',
            'purple',
            'brown',
            'pink',
            'gold',
            'beige',
            'olive',
            'aqua',
            'navy'
        ]

    @staticmethod
    def create_directory(directory: str) -> None:
        if not path.exists(directory):
            makedirs(directory)

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

    @staticmethod
    def average(data: any) -> int:
        if len(data) == 0:
            return 0
        
        if type(data) is list:
            return sum(data) / len(data)
        
        if type(data) is dict:
            return sum([data.values()]) / len(data)

    @classmethod
    def plot(cls, name, x_label, y_label, title):
        plt.xlabel(x_label)# Define o rótulo do eixo x
        plt.ylabel(y_label) # Define o rótulo do eixo y
        plt.title(title) # Define o título do gráfico
        plt.xticks(cls.time) # Fixa os índices do eixo x
        plt.tight_layout() # Ajusta o layout para evitar sobreposição de elementos
        
        title = title.lower().replace(' ', '_')
        cls.create_directory(f'./graphics/{name}') if name != '' else cls.create_directory('./graphics')
        
        plt.legend()
        plt.savefig(f'graphics/{name}/{title}', dpi=300)

    @classmethod
    def plot_data(cls, data, name):
        i=0
        plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
        for alg in data[0]:
            to_plot = []
            for step in data[0][alg]:
                to_plot.append(cls.average([ len(execution[alg][step]['data'][name]) for execution in data ]))
            plt.plot(cls.time, to_plot.copy(), color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)
            i+=1
        cls.plot('', 'Steps', 'Number of services', name)
            
    @classmethod
    def plot_migrations(cls, data):
        i=0
        plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
        for alg in data[0]:
            migrations = []
            for step in data[0][alg]:
                migrations.append(cls.average([ sum(execution[alg][step]['migrations'].values()) for execution in data ]))
            plt.plot(cls.time, migrations, color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)
            i+=1
        cls.plot('', 'Steps', 'Number of migrations', 'migrations')

    @classmethod
    def plot_available_satellites(cls, data):
        i=0
        plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
        for alg in data[0]:
            available_satellites_average = []
            for step in data[0][alg]:
                available_satellites = [ cls.average([ srv['number_of_available_satellites'] for srv in execution[alg][step]['available_satellites'].values() ]) for execution in data ]             
                if len(available_satellites) > 0:
                    available_satellites_average.append(cls.average(available_satellites))
                else:
                    # Hiding values when no services are searching for allocation
                    available_satellites_average.append(None)
            plt.plot(cls.time, available_satellites_average, color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)
            i+=1
        cls.plot('', 'Steps', 'Number of available satellites', 'available satellites average')

    @classmethod
    def plot_satellite_demand_parameters_availability(cls, data, parameters):
        for param in parameters:
            i=0
            plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
            for alg in data[0]:
                param_availability_average = []
                for step in data[0][alg]:
                    param_availability = [
                        cls.average([ srv['total_availability'][param]/srv['number_of_available_satellites'] if srv['total_availability'].get(param) else 0 for srv in execution[alg][step]['available_satellites'].values() ]) for execution in data
                    ]
                    if len(param_availability) > 0:
                        param_availability_average.append(sum(param_availability)/len(param_availability))
                    else:
                        # Hiding values when no services are searching for allocation
                        param_availability_average.append(None)
                plt.plot(cls.time, param_availability_average, color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)

                # Forcing to plot in the right range
                plt.ylim(0, 110)
                i+=1
            cls.plot('', 'Steps', f'{param} availability average', f'{param} availability average')

    @classmethod
    def plot_service_demand_parameters(cls, data, parameters):
        for param in parameters:
            i=0
            plt.figure(figsize=(10, 6)) # Criando o gráfico com um tamanho de figura específico
            for alg in data[0]:
                param_demand_average = []
                for step in data[0][alg]:
                    param_demand = [
                        cls.average([ srv['demand'][param] for srv in execution[alg][step]['services'] if srv['status'] in ['migrating', 'unprovisioned', 'created'] and srv['start'] <= int(step) ]) for execution in data
                    ]
                    if len(param_demand) > 0:
                        param_demand_average.append(sum(param_demand)/len(param_demand))
                    else:
                        param_demand_average.append(0)

                plt.plot(cls.time, param_demand_average, color=cls.colors[i], linestyle='-', linewidth=2, markersize=6, label=alg)

                # Forcing to plot the maximum values
                plt.ylim(0, 100)
                i+=1
            cls.plot('', 'Steps', f'{param} demand average', f'{param} demand average')

    @classmethod
    def plot_graphics(cls, data):

        # Determining graphic dimensions if necessary
        cls.time = cls.time or [ i for i in range(0, max([ len(alg) for alg in data[0].values() ])) ]

        # Provisioning data
        cls.plot_data(data, 'unprovisioned')
        cls.plot_data(data, 'provisioned')
        cls.plot_data(data, 'provisioning')
        cls.plot_data(data, 'end_services')   
        cls.plot_data(data, 'interrupted')   

        # Migrations
        cls.plot_migrations(data)

        # Resources availability
        cls.plot_available_satellites(data)
        cls.plot_satellite_demand_parameters_availability(data, ['cpu', 'memory'])
        
        # Services demand
        cls.plot_service_demand_parameters(data, ['cpu', 'memory'])