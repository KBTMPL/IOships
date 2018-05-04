from Main import Container
from Main import Report
from random import shuffle
import operator
import numpy as np


class Algorithm2:
    ships = []
    containers = []

    def __init__(self, path, ships):
        self.path = path
        self.ships = ships
        self.timestamps = list()
        self.timestamp_elements = set()
        for ship in ships:
            ship.clear_floor()

    def load_containers_data(self):
        self.containers = []
        containers_data = open(self.path).read().splitlines()
        for line in containers_data:
            buffer = line.split(';')
            self.containers.append(
                Container(int(buffer[0]), float(buffer[1]), [int(buffer[2]), int(buffer[3])], int(buffer[4])))

    def write_whats_left(self):
        containers_data = []
        for container in self.containers:
            if not container.is_placed:
                containers_data.append(';'.join(
                    [str(container.idc), str(container.timestamp), str(container.space[0]), str(container.space[1]),
                     str(container.capacity)]))
        if len(containers_data) != 0:
            open(self.path, 'w').write('\n'.join(containers_data) + '\n')
        else:
            open(self.path, 'w').close()

    def sort_containers_capacity_stamp(self):
        # keyfun1 = operator.attrgetter('capacity')
        # self.containers.sort(key=keyfun1, reverse=True)
        shuffle(self.containers)
        keyfun2 = operator.attrgetter('timestamp')
        self.containers.sort(key=keyfun2, reverse=False)

    def sort_containers_capacity(self):
        keyfun1 = operator.attrgetter('capacity')
        self.containers.sort(key=keyfun1, reverse=True)

    def sort_ships_capacity(self):
        keyfun1 = operator.attrgetter('capacity')
        self.ships.sort(key=keyfun1, reverse=True)

    def put_containers_to_ship(self):
        count = np.zeros(len(self.ships))
        capacity_taken = np.zeros(len(self.ships))
        containers_num = len(self.containers)

        for container in self.containers:
            self.timestamps.append(container.timestamp)
        self.timestamp_elements = list(set(self.timestamps))
        #print(self.timestamp_elements)

        for n, ship in enumerate(self.ships):
            for ts in self.timestamp_elements:
                for container in self.containers:
                    if container.timestamp == ts and not container.is_placed:
                        iship = ship.space[0]
                        jship = ship.space[1]
                        icont = container.space[0]
                        jcont = container.space[1]
                        i = 0
                        while not container.is_placed and i + icont <= iship:
                            j = 0
                            while not container.is_placed and j + jcont <= jship:
                                if np.array_equal(ship.floor[i:i + icont, j:j + jcont], np.zeros((icont, jcont))):
                                    ship.floor[i:i + icont, j:j + jcont] = np.ones((icont, jcont))
                                    container.is_placed = True
                                    count[n] += 1
                                    capacity_taken[n] += container.capacity
                                j += 1
                            i += 1
            self.sort_containers_capacity_stamp()

        return [count, capacity_taken, self.ships, containers_num]

    def start(self):
        self.load_containers_data()
        self.sort_containers_capacity_stamp()
        self.sort_ships_capacity()
        data = self.put_containers_to_ship()
        self.write_whats_left()

        return Report(data, 'reports2.txt')

