from Main import Ship
import Generator as g
import Algorithm1 as a1
import Algorithm2 as a2
from shutil import copyfile
import copy
import time as t


def own_testing():
    n = 10000
    max_xdim = 10  # i
    max_ydim = 10  # j
    min_xdim = 1  # i
    min_ydim = 1  # j

    s1 = Ship(1, [25, 30], 1)  # [i,j]
    s2 = Ship(2, [20, 28], 1)
    s3 = Ship(3, [25, 30], 1)
    s4 = Ship(4, [18, 23], 1)
    s5 = Ship(5, [20, 27], 1)
    ships = [s1, s2, s3, s4, s5]

    a1c = 'containers.csv'
    a2c = 'containers_cp.csv'
    a1r = 'reports.txt'
    a2r = 'reports2.txt'

    open(a1c, 'w').close()
    open(a2c, 'w').close()

    # generate data
    g1 = g.Generator(a1c, n, min_xdim, min_ydim, max_xdim, max_ydim)
    g1.start()
    copyfile(a1c, a2c)

    # run algorithm

    ships_cp = copy.copy(ships)

    open(a1r, 'w').close()
    open(a2r, 'w').close()

    t1 = a1.Algorithm1(a1c, ships, a1r)
    t2 = a2.Algorithm2(a2c, ships_cp, a2r)

    i_greed = 0
    i_brute = 0

    empty_ships_greed = 0
    empty_ships_brute = 0

    out = 0
    while out != 1337:
        out = t1.perform_algorithm()
        i_greed += 1
        if out != 1337:
            empty_ships_greed += out.empty_ships

    out = 0
    while out != 1337:
        out = t2.perform_algorithm()
        i_brute += 1
        if out != 1337:
            empty_ships_brute += out.empty_ships

    test_output = list()

    test_output.append('Liczba raportów: ')
    test_output.append('Algorytm zachłanny: ' + str(i_greed))
    test_output.append('Algorytm bruteforce: ' + str(i_brute))
    test_output.append('Liczba pustych statków: ')
    test_output.append('Algorytm zachłanny: ' + str(empty_ships_greed))
    test_output.append('Algorytm bruteforce: ' + str(empty_ships_brute))

    open('test_outputs\\'+str(int(t.time())) + '.txt', 'w').write('\n'.join(test_output))

    # t1.start()
    # t2.start()

    # while t1.is_alive() or t2.is_alive():
    #    pass


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

    ships_cp = ships

    open(a1r, 'w').close()
    open(a2r, 'w').close()

    t1 = a1.Algorithm1(a1c, ships, a1r)
    t2 = a2.Algorithm2(a2c, ships_cp, a2r)

    i_greed = 0
    i_brute = 0

    empty_ships_greed = 0
    empty_ships_brute = 0

    out = 0
    while out != 1337:
        out = t1.perform_algorithm()
        i_greed += 1
        if out != 1337:
            empty_ships_greed += out.empty_ships

    out = 0
    while out != 1337:
        out = t2.perform_algorithm()
        i_brute += 1
        if out != 1337:
            empty_ships_brute += out.empty_ships

    test_output = list()

    test_output.append(str(t.strftime("%Y-%m-%d %H:%M:%S", t.gmtime(t.time()))))
    test_output.append('Liczba raportów: ')
    test_output.append('Algorytm zachłanny: ' + str(i_greed))
    test_output.append('Algorytm bruteforce: ' + str(i_brute))
    test_output.append('Liczba pustych statków: ')
    test_output.append('Algorytm zachłanny: ' + str(empty_ships_greed))
    test_output.append('Algorytm bruteforce: ' + str(empty_ships_brute))

    open('test_outputs\\tests.txt', 'a',  encoding="utf-8").write('\n'.join(test_output))

    # t1.start()
    # t2.start()

    # while t1.is_alive() or t2.is_alive():
    #    pass

# client_data_testing('DataInputGroupPT1440_SHIPS.csv', 'DataInputGroupPT1440.csv')


for i in range(20):
    own_testing()
