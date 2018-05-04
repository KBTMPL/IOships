from Main import Ship
import Generator as g
import Algorithm1 as a1
import Algorithm2 as a2
from shutil import copyfile
from random import shuffle

# input data

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

# Algorithm 1

# generate data

g1 = g.Generator('containers.csv', n, min_xdim, min_ydim, max_xdim, max_ydim)
g1.start()
copyfile('containers.csv', 'containers_cp.csv')

# run algorithm

p1 = a1.Algorithm1('containers.csv', ships)
p1.start()

p2 = a2.Algorithm2('containers_cp.csv', ships)
p2.start()
