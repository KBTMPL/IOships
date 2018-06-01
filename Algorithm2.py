from Main import Container
from Main import Report
from random import shuffle
import operator
import numpy as np
import threading


class Algorithm2(threading.Thread):
    ships = []
    containers = []

    def __init__(self, path, ships, report_path):
        threading.Thread.__init__(self)
        self.path = path
        self.ships = ships
        self.report_path = report_path
        self.timestamps = list()
        self.timestamp_elements = set()
        self.max_containers = 100
        self.algorithm_name = 'bruteforce'
        self.clear_ships()

    def run(self):
        out = 0
        while out != 1337:
            out = self.perform_algorithm()

    def clear_ships(self):
        for ship in self.ships:
            ship.clear_floor()

    def load_containers_data(self):
        self.containers = []
        containers_data = open(self.path).read().splitlines()
        for line in containers_data:
            try:
                buffer = line.split(',')
                ids = int(buffer[1])
                timestamp = float(buffer[0])
                space_i = int(buffer[2].lstrip('['))
                space_j = int(buffer[3].rstrip(']'))
                capacity = int(buffer[4])
            except ValueError as verr:
                print('Uszkodzony linia:')
                print(line)
                break
            except Exception as ex:
                print('Uszkodzony linia:')
                print(line)
                break
            self.containers.append(
                Container(ids, timestamp, [space_i, space_j], capacity))

    def write_whats_left(self):
        containers_data = []
        for container in self.containers:
            if not container.is_placed:
                containers_data.append(','.join(
                    [str(container.timestamp), str(container.idc), '[' + str(container.space[0]), str(container.space[1]) + ']',
                     str(container.capacity)]))
        if len(containers_data) != 0:
            open(self.path, 'w').write('\n'.join(containers_data) + '\n')
        else:
            open(self.path, 'w').close()

    def shuffle_containers_and_sort_stamp(self):
        # keyfun1 = operator.attrgetter('floor_area')
        # self.containers.sort(key=keyfun1, reverse=True)
        shuffle(self.containers)
        keyfun2 = operator.attrgetter('timestamp')
        self.containers.sort(key=keyfun2, reverse=False)

    def sort_containers_floor_area(self):
        keyfun1 = operator.attrgetter('floor_area')
        self.containers.sort(key=keyfun1, reverse=True)

    def sort_ships_capacity(self):
        keyfun1 = operator.attrgetter('floor_area')
        self.ships.sort(key=keyfun1, reverse=True)

    def make_placeable(self):
        for i in range(self.max_containers):
            self.containers[i].is_placeable = True

    def put_containers_to_ship(self):
        count = np.zeros(len(self.ships))
        surface_taken = np.zeros(len(self.ships))
        containers_num = len(self.containers)

        for n, ship in enumerate(self.ships):
            iship = ship.space[0]
            jship = ship.space[1]
            for container in self.containers:
                if container.is_placeable:
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
                                surface_taken[n] += container.floor_area
                            j += 1
                        i += 1

        return [count, surface_taken, self.ships, containers_num]

    def perform_algorithm(self):
        self.clear_ships()
        self.load_containers_data()
        if self.containers.__len__() >= self.max_containers:
            self.shuffle_containers_and_sort_stamp()
            self.make_placeable()
            self.sort_ships_capacity()
            data = self.put_containers_to_ship()
            self.write_whats_left()

            return Report(data, self.report_path, self.algorithm_name)
        else:
            print('Nie dostarczono ' + str(self.max_containers) + ' kontenerów')
            return 1337
