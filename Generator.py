import random as r
import time as t
from Main import Container


class Generator:
    containers = []
    current_containers = 0
    idc = 0

    def __init__(self, path, max_containers, min_xdim, min_ydim, max_xdim, max_ydim):
        self.path = path
        self.max_containers = max_containers
        self.min_xdim = min_xdim
        self.min_ydim = min_ydim
        self.max_xdim = max_xdim
        self.max_ydim = max_ydim
        idc = open('id.txt', 'r').readline()
        if idc.isnumeric():
            self.idc = int(idc)

    def generate_containers(self):
        self.containers = []
        file = open(self.path).read().splitlines()
        file = list(filter(None, file))
        self.current_containers = len(file)
        for i in range(1, self.max_containers - self.current_containers + 1):
            space = [r.randint(self.min_xdim, self.max_xdim), r.randint(self.min_ydim, self.max_ydim)]
            self.containers.append(Container(self.idc, t.time(), space, space[0] * space[1]))
            self.idc += 1

    def write_to_file(self):
        containers_data = []
        for container in self.containers:
            containers_data.append(';'.join(
                [str(container.idc), str(container.timestamp), str(container.space[0]), str(container.space[1]),
                 str(container.capacity)]))
        open(self.path, 'a').write('\n'.join(containers_data))
        open('id.txt', 'w').write(str(self.idc))

    def clean_file(self):
        open(self.path, 'w').close()

    def start(self):
        self.generate_containers()
        self.write_to_file()
        return self.current_containers

