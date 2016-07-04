# This python program based on a BASIC program Written by Jordan d. Marche
# and explained by him in Sky & Telescope for July, 1990, page 71.
# Source: http://www.skyandtelescope.com/wp-content/uploads/marche.bas
 
import numpy as np
import math

dr = math.pi/180
L = 0.030 # camera focal length
N = 4 # number of stars, must be >=4


# Test Data set for Major Ursa const. stars: Dubhe, Merak, Phad, Alkaid

a = [ 11.062155*15*dr, 	11.030677*15*dr, 	11.897168*15*dr, 	13.792354*15*dr ] # converted to radians
d = [ 61.751033*dr, 	56.382427*dr, 		53.69476*dr, 		49.313265*dr ]    # converted to radians
x = [ 574.518737793, 	458.241729736, 		713.016113281, 		1445.30236816 ]
y = [ 968.822937012, 	769.926208496, 		546.142456055, 		302.151184082 ]
x1=[]
y1=[]

# Target (center of the image)
xt = 1999/2 
yt = 1199/2

a0 = np.mean(a) # R.a. of plate center approx. 
d0 = np.mean(d)	# dec. of plate center approx.

sd = math.sin(d0)
cd = math.cos(d0)

for star in range(N):
	sj = math.sin(d[star])
	cj = math.cos(d[star])
	h = sj*sd+cj*cd*math.cos(a[star]-a0)
	x1 = x1 + [cj*math.sin(a[star]-a0)/h]
	y1 = y1 + [(sj*cd-cj*sd*math.cos(a[star]-a0))/h]

r1 = 0
r2 = 0
r3 = 0
r7 = 0
r8 = 0
r9 = 0
xs = 0
ys = 0
r =  [[0 for i in range(9)] for j in range(N)] 
for star in range(4):
	xs = xs + x[star]
	ys = ys + y[star]
	r[star][0] = x[star]*x[star]
	r1 = r1 + r[star][0]
	r[star][1] = y[star]*y[star]
	r2 = r2 + r[star][1]
	r[star][2] = x[star]*y[star]
	r3	= r3 + r[star][2]
	r[star][6] = y1[star] - y[star] / L
	r7 = r7 + r[star][6]
	r[star][7] = r[star][6]*x[star]
	r8 = r8 + r[star][7]
	r[star][8] = r[star][6]*y[star]
	r9 = r9 + r[star][8]

# Now solve for d, E, f, by cramer's Rule
dd = r1*(r2*N-ys*ys)-r3*(r3*N-xs*ys)+xs*(r3*ys-xs*r2)
d = r8*(r2*N-ys*ys)-r3*(r9*N-r7*ys)+xs*(r9*ys-r7*r2)
e = r1*(r9*N-r7*ys)-r8*(r3*N-xs*ys)+xs*(r3*r7-xs*r9)
f = r1*(r2*r7-ys*r9)-r3*(r3*r7-xs*r9)+r8*(r3*ys-xs*r2)
d = d/dd
e = e/dd
f = f/dd

#
r4=0
r5=0
r6=0

for star in range(N):
	r[star][3] = x1[star]-x[star]/L
	r4=r4+r[star][3]
	r[star][4]=r[star][3]*x[star]
	r5=r5+r[star][4]
	r[star][5]=r[star][3]*y[star]
	r6=r6+r[star][5]

# Now solve for a ,b, c, by cramer's Rule
a = r5*(r2*N-ys*ys)-r3*(r6*N-r4*ys)+xs*(r6*ys-r4*r2)
b = r1*(r6*N-r4*ys)-r5*(r3*N-xs*ys)+xs*(r3*r4-xs*r6)
c = r1*(r2*r4-ys*r6)-r3*(r3*r4-xs*r6)+r5*(r3*ys-xs*r2)
a = a/dd
b = b/dd
c = c/dd

#print a, b, c, d, e, f


# Now fINd RESIdUaLS
As = 0
Ds = 0
ra = [0 for i in range(N)]
rd = [0 for i in range(N)]
for star in range(N):
	ra[star] = x[star]-L*(x1[star]-(a*x[star]+b*y[star]+c))
	rd[star] = y[star]-L*(y1[star]-(d*x[star]+e*y[star]+f))
	As = As + ((ra[star]/L)*3600/(dr*15*math.cos(d0)))**2
	Ds = Ds + ((rd[star]/L)*3600/dr)**2

s1 = math.sqrt(As/(N-3))
s2 = math.sqrt(Ds/(N-3))

#print
#print "Residuals        R.a.     dec."
#for star in range(4):
#	print ra[star], rd[star]

#print

# find standard coordinates of target
xx = a*xt + b*yt + c + xt/L
yy = d*xt + e*yt + f + yt/L
b = cd - yy*sd
g = math.sqrt(xx*xx + b*b)

#   find right ascension of target
a5 = math.atan(xx/b)
if b<0:
	a5 = a5 + math.pi
a6 = a5 + a0
if a6>2*math.pi:
	a6 = a6 - 2*math.pi
if a6<0:
	a6 = a6 + 2*math.pi
at = a6/(dr*15)

# find declination of target
d6 = math.atan((sd + yy*cd)/g)
dt = d6/dr

#
print "for target:"
print
print "Right ascension "
print at
#print "Std. dev. " + str(s1)
print
print "declination       "
print dt
#print " Std. dev." + str(s2)




