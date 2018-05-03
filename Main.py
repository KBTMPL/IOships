import numpy as np
import time as t


class Ship:
    def __init__(self, ids, space):
        self.ids = ids
        self.space = space
        self.capacity = space[0] * space[1]
        self.floor = np.zeros((space[0], space[1]))


class Container:
    def __init__(self, idc, timestamp, space, capacity):  # do poprawy generacja timestampu
        self.idc = idc
        self.timestamp = timestamp
        self.space = space
        self.floor = np.zeros((space[0], space[1]))
        self.capacity = capacity
        self.is_placed = False


class Report:
    def __init__(self, data, path):
        self.count = data[0]
        self.capacity_taken = data[1]
        self.ships = data[2]
        self.containers_num = data[3]
        self.path = path
        self.overall_capacity = 0
        self.timezone_offset = 2*3600
        self.timestamp = t.time() + self.timezone_offset

        for ship in self.ships:
            self.overall_capacity += ship.capacity

        lines_to_write = []

        lines_to_write.append('Raport wygenerowano: ' + str(self.timestamp) + ' (' + str(t.strftime("%Y-%m-%d %H:%M:%S", t.gmtime(self.timestamp))) + ')')
        for x in range(0,len(self.count)):
            lines_to_write.append('Na statek o id = ' + str(self.ships[x].ids) + ' załadowano:')
            lines_to_write.append(str(int(self.count[x])) + ' kontenerów, zajmując przy tym ' + str("%.2f" % (self.capacity_taken[x]/self.ships[x].capacity*100)) + '%')
        lines_to_write.append('Łącznie zapakowano ' + str(int(self.count.sum())) + ' kontenerów z dostępnych ' + str(int(self.containers_num)) + ' kontenerów')
        lines_to_write.append('Średnia zajętość wyniosła: ' + str("%.2f" % (self.capacity_taken.sum()/self.overall_capacity*100)) + '%')
        open(self.path, 'a',  encoding="utf-8").write('\n'.join(lines_to_write) + '\n\n')

