from Components import ComponentManager
from general_utilities import num_satellites, num_services
from random import randint

if __name__ == "__main__":
    cm = ComponentManager()

    cm.create_satellites(num_satellites)
    cm.create_services(num_services, starts=[i for i in range(9, 0, -2)], demands=[{'cpu': 30 + randint(0, 20), 'memory': 50 + randint(0, 20)} for _ in range(10)], coordinates=[()], provisioned_times=[i for i in range(1, 10)])
    # cm.create_services(num_services, starts=[10], demands=[{}], coordinates=[()], provisioning_durations=[i for i in range(1, 10)])
    # cm.create_services(num_services)

    cm.initialize_simulator()
    cm.start_simulator()

    print('\nDONE!')