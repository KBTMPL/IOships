from Main import Ship
import Generator as g
import Algorithm1 as a1
import Algorithm2 as a2
from shutil import copyfile
import threading


def own_testing():
    n = 100
    max_xdim = 10  # i
    max_ydim = 10  # j
    min_xdim = 1  # i
    min_ydim = 1  # j

    s1 = Ship(1, [25, 30])  # [i,j]
    s2 = Ship(2, [20, 28])
    s3 = Ship(3, [25, 30])
    s4 = Ship(4, [18, 23])
    s5 = Ship(5, [20, 27])
    ships = [s1, s2, s3, s4, s5]

    # generate data
    g1 = g.Generator('containers.csv', n, min_xdim, min_ydim, max_xdim, max_ydim)
    g1.start()
    copyfile('containers.csv', 'containers_cp.csv')

    # run algorithm
    p1 = a1.Algorithm1('containers.csv', ships, 'reports.csv')
    p1.perform_algorithm()
    p2 = a2.Algorithm2('containers_cp.csv', ships, 'reports2.csv')
    p2.perform_algorithm()


def client_data_testing(ships_path, containers_path):
    a1c = 'client_containers_for_a1.csv'
    a2c = 'client_containers_for_a2.csv'
    a1r = 'client_reports_a1.txt'
    a2r = 'client_reports_a2.txt'

    ships = []
    ships_data = open(ships_path).read().splitlines()
    for line in ships_data:
        buffer = line.split(',')
        ships.append(
            Ship(int(buffer[0]), [int(buffer[1].lstrip('[')), int(buffer[2].rstrip((']')))], int(buffer[3])))

    copyfile(containers_path, a1c)
    copyfile(containers_path, a2c)

    # run algorithm

    out1 = 0
    out2 = 0

    open(a1r, 'w').close()
    open(a2r, 'w').close()

#    while out1 != 1337:
#        p1 = a1.Algorithm1(a1c, ships, a1r)
#        out1 = p1.perform_algorithm()

#    while out2 != 1337:
#        p2 = a2.Algorithm2(a2c, ships, a2r)
#        out2 = p2.perform_algorithm()

    ships_cp = ships

    open(a1r, 'w').close()
    open(a2r, 'w').close()

    t1 = a1.Algorithm1(a1c, ships, a1r)
    t2 = a2.Algorithm2(a2c, ships_cp, a2r)

    t1.start()
    t2.start()

    while t1.is_alive() or t2.is_alive():
        pass

client_data_testing('DataInputGroupPT1440_SHIPS.csv', 'DataInputGroupPT1440.csv')

