# This python program based on a BASIC program Written by Jordan d. Marche
# and explained by him in Sky & Telescope for July, 1990, page 71.
# Source: http://www.skyandtelescope.com/wp-content/uploads/marche.bas
 
import numpy as np
import math
import startracker_lib as st

dr = math.pi/180

# Test Data set for Major Ursa const. stars: Dubhe, Merak, Phad, Alkaid

a = [ 11.062155*15*dr, 	11.030677*15*dr, 	11.897168*15*dr, 	13.792354*15*dr ] # converted to radians
d = [ 61.751033*dr, 	56.382427*dr, 		53.69476*dr, 		49.313265*dr ]    # converted to radians
x = [ 574.518737793, 	458.241729736, 		713.016113281, 		1445.30236816 ]
y = [ 968.822937012, 	769.926208496, 		546.142456055, 		302.151184082 ]

xt = 1999/2
yt = 1199/2

[at, dt] = st.coordinates(xt, yt, a, d, x, y)

print "Right ascension: " + str(at)
print "Declination:     " + str(dt)





