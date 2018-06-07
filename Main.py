import numpy as np
import time as t
import collections


class Ship:
    def __init__(self, ids, space, capacity = np.random.randint(1000, 2000)):
        self.ids = ids
        self.space = space
        self.floor_area = space[0] * space[1]
        self.floor = np.zeros((space[0], space[1]))
        self.capacity = capacity
        self.containers_loaded = 0
        self.area_taken = 0

    def clear_floor(self):
        self.floor = np.zeros((self.space[0], self.space[1]))
        self.containers_loaded = 0
        self.area_taken = 0


class Container:
    def __init__(self, idc, timestamp, space, capacity = np.random.randint(1, 10)):  # do poprawy generacja timestampu
        self.idc = idc
        self.timestamp = timestamp
        self.space = space
        self.floor = np.zeros((space[0], space[1]))
        self.floor_area = space[0] * space[1]
        self.is_placed = False
        self.is_placeable = False
        self.capacity = capacity


class Report:
    def __init__(self, data, path, algorithm_name):
        self.ships = data[0]
        self.containers_num = data[1]

        self.path = path
        self.algorithm_name = algorithm_name
        self.overall_area = 0
        self.timezone_offset = 2*3600
        self.timestamp = t.time() + self.timezone_offset
        self.sum_containers_loaded = 0
        self.sum_area_taken = 0

        self.empty_ships = 0

        for ship in self.ships:
            self.overall_area += ship.floor_area
            self.sum_area_taken += ship.area_taken
            self.sum_containers_loaded += ship.containers_loaded
            if ship.area_taken == 0:
                self.empty_ships += 1

        lines_to_write = list()
        sort_buffer = dict()

        lines_to_write.append('Raport wygenerowano: ' + str(self.timestamp) + ' (' + str(t.strftime("%Y-%m-%d %H:%M:%S", t.gmtime(self.timestamp))) + ')')
        lines_to_write.append('Przy pomocy: ' + self.algorithm_name)
        for ship in self.ships:
            sort_buffer[ship.ids] = 'Na statek o id = ' + str(ship.ids) + ' załadowano:\n' + str(int(ship.containers_loaded)) + ' kontenerów, zajmując przy tym ' + str("%.2f" % (ship.area_taken / ship.floor_area * 100)) + '%'
        sorted_buffer = collections.OrderedDict(sorted(sort_buffer.items()))
        for key, val in sorted_buffer.items():
            lines_to_write.append(val)
        lines_to_write.append('Łącznie zapakowano ' + str(int(self.sum_containers_loaded)) + ' kontenerów z dostępnych ' + str(int(self.containers_num)) + ' kontenerów')
        lines_to_write.append('Średnia zajętość wyniosła: ' + str("%.2f" % (self.sum_area_taken / self.overall_area * 100)) + '%')
        open(self.path, 'a',  encoding="utf-8").write('\n'.join(lines_to_write) + '\n\n')
        # print(lines_to_write[0] + ' | ' + lines_to_write[1])

