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
        # path to containers
        self.path = path
        # ships that are meant to be loaded
        self.ships = ships
        # path to store reports
        self.report_path = report_path
        # project condition
        self.max_containers = 100
        # name of the algorithm
        self.algorithm_name = 'Algorytm bruteforce'
        # clear ship floors in case of object reusing
        self.clear_ships()
        # buffer for maximum floor area of ships
        self.max_ships_floor_area = 0

    def run(self):
        out = 0
        while out != -1:
            out = self.perform_algorithm()

    def clear_ships(self):
        for ship in self.ships:
            ship.clear_floor()

    def check_max_floor_area_ship(self):
        floor_areas = list()
        for ship in self.ships:
            floor_areas.append(ship.floor_area)
        floor_areas.sort(reverse=True)
        self.max_ships_floor_area = floor_areas[0]

    def load_containers_data(self):
        self.containers = []
        containers_data = open(self.path).read().splitlines()
        for line in containers_data:
            space_i = 1
            space_j = 1
            flag = False
            try:
                buffer = line.split(',')
                if buffer.__len__() != 5:
                    print('Zła ilość parametrów')
                    print('Kontener:')
                    print(line)
                    print()
                    continue
                idc = int(buffer[1])
                timestamp = float(buffer[0])
                space_i = int(buffer[2].lstrip('['))
                space_j = int(buffer[3].rstrip(']'))
                capacity = int(buffer[4])
            except ValueError as verr:
                print('Uszkodzona linia (zły typ danych)')
                flag = True
            except Exception as ex:
                print('Uszkodzona linia (zły typ danych)')
                flag = True
            if space_j * space_i > self.max_ships_floor_area:
                print('Ten kontener jest większy niż największy posiadany statek')
                flag = True
            if flag:
                print('Kontener:')
                print(line)
                print()
                continue
            self.containers.append(Container(idc, timestamp, [space_i, space_j], capacity))

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

    def sort_ships_capacity(self):
        keyfun1 = operator.attrgetter('floor_area')
        self.ships.sort(key=keyfun1, reverse=True)

    def make_placeable(self):
        for i in range(self.max_containers):
            self.containers[i].is_placeable = True

    def put_containers_to_ship(self):
        containers_num = len(self.containers)

        for ship in self.ships:
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
                                ship.containers_loaded += 1
                                ship.area_taken += container.floor_area
                            j += 1
                        i += 1

        return [self.ships, containers_num]

    def perform_algorithm(self):
        # clear ship floors in case of object reusing
        self.clear_ships()
        # find biggest ship
        self.check_max_floor_area_ship()
        # load containers from file
        self.load_containers_data()
        # check if the basic project condition is true (minimum 100 containers)
        if self.containers.__len__() >= self.max_containers:
            # shuffle than sort containers by stamp
            self.shuffle_containers_and_sort_stamp()
            # make containers (100 of them) placeable
            self.make_placeable()
            # sort ships by floor area
            self.sort_ships_capacity()
            # start loading containers
            data = self.put_containers_to_ship()
            # save containers that weren't shipped
            self.write_whats_left()

            # make and save report
            return Report(data, self.report_path, self.algorithm_name)
        else:
            # alert end user about not meeting the condition stated above
            print('Nie dostarczono ' + str(self.max_containers) + ' kontenerów | ' + self.algorithm_name)
            return -1
