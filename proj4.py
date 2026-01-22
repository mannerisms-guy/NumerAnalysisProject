#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:49:35 2022

@author: michaelcarter
"""
import numpy as np
from matplotlib import pyplot as plt

# variables to check program works
# first entry: ballType
# second entry: throwStrength
# third entry: throwAngle
# ballTypes = ["0: Ping Pong Ball","1: Tennis Ball","2: Golf Ball","3: Baseball",
#              "4: Soccer Ball","5: Basketball","6: Shot Put","7: 25 Pound Medicine Ball"]
# throwStrengths = ["1: Gentle Toss","2: Moderate Toss","3: Backyard Game Of Catch",
#                   "4: Medium","5: Typical Person Max Effort","6: Great Athlete",
#                   "7: Typical D1 College Pitcher","8: Typical Pro Baseball Pitch",
#                   "9: Record Baseball Pitch","10: Transcending Human Biomechanics"]
#entries = [6,10, 30]
L = ["0", "0", "0"]

for i in range(len(entries)):
    L[i] = str(entries[i])+" \n"

# Writing to a file
file1 = open('myfile.txt', 'w')
file1.writelines((L))
file1.close()
file1 = open('myfile.txt', 'r')

print("Welcome to Thrower! \n")

ballTypes = ["0: Ping Pong Ball","1: Tennis Ball","2: Golf Ball","3: Baseball",
             "4: Soccer Ball","5: Basketball","6: Shot Put","7: 25 Pound Medicine Ball"]

print("0: Ping Pong Ball")
print("1: Tennis Ball")
print("2: Golf Ball")
print("3: Baseball")
print("4: Soccer Ball")
print("5: Basketball")
print("6: Shot Put")
print("7: 15 Kilogram Medicine Ball\n")

# Array of text to print after selecting throw strength
throwStrengths = ["1: Gentle Toss","2: Moderate Toss","3: Backyard Game Of Catch",
                  "4: Medium","5: Typical Person Max Effort","6: Great Athlete",
                  "7: Typical D1 College Pitcher","8: Typical Pro Baseball Pitch",
                  "9: Record Baseball Pitch","10: Transcending Human Biomechanics"]

ballType = file1.readline()
ballType = int(ballType)
print("You selected "+ballTypes[ballType])
print("\n")

throwStrength = file1.readline()
throwStrength = int(throwStrength)-1
print("You selected "+ throwStrengths[throwStrength])

# Throw strengths use a baseball throw as reference.
# The speeds for a baseball throw for the given throw strength are as follows:
# mph on left, m/s on right:
# 10, 4.5
# 20, 9
# 30, 13.5
# 40, 18
# 50, 23
# 75, 34
# 85, 38
# 95, 42.5
# 105, 47
# 120, 54

referenceBaseballSpeeds = [4.5, 9, 13.5, 18, 23, 34, 38, 42.5, 47, 54]
mass = [.0027,.057, .045, .142, .43, .75, 7.26, 15]

# This function finds the kinetic energy of a body in motion
def kineticEnergy(mass, speed):
    return(.5*mass*speed**2)

# Objects are thrown with an initial kinetic energy. I find that energy using the reference
# speeds and the mass of a baseball
initialEnergy = kineticEnergy(mass[3], referenceBaseballSpeeds[throwStrength])

# This function finds the speed of an object in motion given its kinetic energy and mass
def speedGivenEnergy(energy, mass):
    return(np.sqrt(2*energy/mass))

# Earlier, I found the kinetic energy that would be present if the individual was throwing a baseball.
# However, there are other objects being thrown; using the mass of the object and the determined KE
# I find the initial speed
initialSpeed = speedGivenEnergy(initialEnergy, mass[ballType])
print("\n")

throwAngle = file1.readline()
throwAngle = int(throwAngle)
# Assume that the projectile is a perfect sphere
Cd = .5
# Air density: 20 degrees C, 101.325 kPa. Units are kg/m^3
rho = 1.2

# Typical diameters of the different projectiles. 
diameter = [.039, .067, .043, .073, .22, .24, .128, .305]

# In order to calculate air resistance, the frontal area of the projectiles must be determined.
frontalArea = [0]*8
for i in range(len(diameter)):
    frontalArea[i] = (diameter[i]/2)**2*np.pi

# Constant used in projectile motion equations
D = rho*Cd*frontalArea[ballType]/2

# release height of 1.5 meters
initialHeight = 1.5
# 100 measurements per second
deltaT = .01
# sufficiently large max time that the projectile will have time to touch down
maxT = 30

# x and y vectors; main items of interest
x = [0]*int(maxT/deltaT)
y = [initialHeight]*int(maxT/deltaT)
# acceleration in x and y components
ax = 0
ay = 0
# speed/magnitude of velocity
v = initialSpeed
# velocity components
vx = np.cos(np.pi/180*throwAngle)*v
vy = np.sin(np.pi/180*throwAngle)*v

for i in range(len(x)-1):
    # determine ax, ay at each step
    ax = -(D/mass[ballType])*v*vx
    ay = -9.8-(D/mass[ballType])*v*vy
    # using ax, ay, determine vx, vy
    vx = vx + ax*deltaT
    vy = vy + ay*deltaT
    v = np.sqrt(vx**2+vy**2)
    # find next x, y locations
    x[i+1] = x[i] + vx*deltaT + 1/2*ax*deltaT**2
    y[i+1] = y[i] + vy*deltaT + 1/2*ay*deltaT**2
    
# the x and y arrays have a bunch of meaningless numbers that follow touchdown. 
# This function finds the place in the array when touchdown haooens.
def zeroFinder(y):
    for i in range(len(y)):
        if y[i] < 0:
            return i

# Get rid of all the Xs and Ys that follow touchdown
relevantXs = x[0:zeroFinder(y)+1]
relevantYs = y[0:zeroFinder(y)+1]

# Duration of "air time" without air resistance
noAirTFinal = (-1*initialSpeed*np.sin(np.pi/180*throwAngle)-np.sqrt((initialSpeed*np.sin(np.pi/180*throwAngle))**2+4*4.9*initialHeight))/(-9.8)
# Distance without air resistance
noAirDist = noAirTFinal*initialSpeed*np.cos(np.pi/180*throwAngle)
airDist = relevantXs[len(relevantXs)-1]
distanceDecreased = 1-airDist/noAirDist

print("\n")
print("Air resistance decreases the distance of this throw by " + str(100*round(distanceDecreased, 4)) + " percent.\n")
print("Distance with air resistance: " + str(round(airDist, 2))+" meters.")
print("Distance without air resistance: " + str(round(noAirDist, 2)) +" meters.")
# print(initialSpeed)
plt.scatter(relevantXs, relevantYs)
plt.ylabel("Height (m)")
plt.xlabel("Ground Covered (m)")
plt.show()