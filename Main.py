import numpy as np
import time as t
import operator


class Ship:
    def __init__(self, ids, space, capacity = np.random.randint(1000, 2000)):
        self.ids = ids
        self.space = space
        self.floor_area = space[0] * space[1]
        self.floor = np.zeros((space[0], space[1]))
        self.capacity = capacity

    def clear_floor(self):
        self.floor = np.zeros((self.space[0], self.space[1]))


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
        self.count = data[0]
        self.surface_taken = data[1]
        self.ships = data[2]
        self.containers_num = data[3]
        self.path = path
        self.algorithm_name = algorithm_name
        self.overall_area = 0
        self.timezone_offset = 2*3600
        self.timestamp = t.time() + self.timezone_offset

        for ship in self.ships:
            self.overall_area += ship.floor_area

        # print(self.ships)
        # keyfun1 = operator.attrgetter('ids')
        # self.ships.sort(key=keyfun1, reverse=False)

        lines_to_write = list()

        lines_to_write.append('Raport wygenerowano: ' + str(self.timestamp) + ' (' + str(t.strftime("%Y-%m-%d %H:%M:%S", t.gmtime(self.timestamp))) + ')')
        lines_to_write.append('Przy pomocy algorytmu: ' + self.algorithm_name)
        for x in range(0, len(self.count)):
            lines_to_write.append('Na statek o id = ' + str(self.ships[x].ids) + ' załadowano:')
            lines_to_write.append(str(int(self.count[x])) + ' kontenerów, zajmując przy tym ' + str("%.2f" % (self.surface_taken[x] / self.ships[x].floor_area * 100)) + '%')
        lines_to_write.append('Łącznie zapakowano ' + str(int(self.count.sum())) + ' kontenerów z dostępnych ' + str(int(self.containers_num)) + ' kontenerów')
        lines_to_write.append('Średnia zajętość wyniosła: ' + str("%.2f" % (self.surface_taken.sum() / self.overall_area * 100)) + '%')
        open(self.path, 'a',  encoding="utf-8").write('\n'.join(lines_to_write) + '\n\n')
        print(lines_to_write[0] + ' | ' + lines_to_write[1])

