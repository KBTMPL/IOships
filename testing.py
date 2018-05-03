from Main import Ship
import Generator as g
import Algorithm1 as a1

# dane wejściowe

n = 100
max_xdim = 12  # i
max_ydim = 6  # j
min_xdim = 4  # i
min_ydim = 2  # j

s1 = Ship(1, [25, 30])  # [i,j]
s2 = Ship(2, [20, 28])
s3 = Ship(3, [25, 30])
s4 = Ship(4, [18, 23])
s5 = Ship(5, [20, 27])

ships = [s1, s2, s3, s4, s5]

# generacja danych

g1 = g.Generator('containers.csv', n, min_xdim, min_ydim, max_xdim, max_ydim)
g1.start()

# wywołanie algorytmu

p1 = a1.Algorithm1('containers.csv', ships)
p1.start()
