# Day 12. N-Body Problem

"""
    -1   0   2
A =  2 -10  -7
     4  -8   8
     3   5  -1


     3  -1  -1 
B =  1   3   3
    -3   1  -3
    -1  -3   1


         1 if x < y
f(x,y):  0 if x = y
        -1 if y > x


B(i,j) = sum_k(f(A(i,j), A(k,j))


On step i:
    Position (Pi)
    Gravity (Gi)
    Velocity (Vi)
    Velocity in step i-1 (Vi')

    update_moons_gravity() : Pi -> Gi
    apply_gravity()        : Vi' + Gi -> Vi
    apply_velocity()       : Pi  + Vi -> Pi

"""

import copy
import math
from functools import reduce


# Part One
def f(x, y):
    if x < y:
        return 1
    elif x == y:
        return 0
    elif x > y:
        return -1  

def update_moons_gravity(pos, n=4, m=3):
    gravity = [[0]*m for i in range(n)]    
    for i in range(n):
        for j in range(m):
            gravity[i][j] = sum([f(pos[i][j], pos[k][j]) for k in range(n)]) 
    return gravity


def apply_gravity(velocity, gravity, n=4, m=3):
    for i in range(n):
        for j in range(m):
            velocity[i][j] += gravity[i][j]        


def apply_velocity(velocity, position, n=4, m=3):
    for i in range(n):
        for j in range(m):
            position[i][j] = position[i][j] + velocity[i][j]


def simulate(position, velocity, steps=10):
    for step in range(steps):
        gravity = update_moons_gravity(position)
        apply_gravity(velocity, gravity)
        apply_velocity(velocity, position)
  

def calculate_energy(position, velocity, n=4, m=3):
    total_energy = 0
    for i in range(n):
        potential = sum([abs(position[i][j]) for j in range(m)])
        kinetic = sum([abs(velocity[i][j]) for j in range(m)])
        total_energy += potential * kinetic
    return total_energy


print('Part One. Testing')
# Part One: Test 1
position = [[-1,0,2],[2,-10,-7],[4,-8,8],[3,5,-1]]
velocity = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
steps = 10
simulate(position, velocity, steps)
total_energy = calculate_energy(position, velocity)
assert total_energy == 179


# Part One: Test 2
position = [[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]]
velocity = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
steps = 100
simulate(position, velocity, steps)
total_energy = calculate_energy(position, velocity)
assert total_energy == 1940


# Part One: Total Energy
def read_input():
    position = []
    with open('input','r') as f:
        for line in f:
            x,y,z = line.split(', ')
            x = int(x.split('=')[1])
            y = int(y.split('=')[1])
            z = int(z.split('=')[1][:-2]) # Remove > and \n
            position.append([x,y,z])
    return position
            
            
position = read_input()
velocity = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
steps = 1000
simulate(position, velocity, steps)
total_energy = calculate_energy(position, velocity)
print('Part One. Calculating Total Energy in 1000 iterations: {}'.format(total_energy))



# Part Two

def update_axis_gravity(positions):
    gravity = [0]*len(positions)
    for i, _ in enumerate(positions):
        gravity[i] = sum([f(positions[i], positions[k]) for k in range(len(positions))]) 
    return gravity
    

def apply_axis_gravity(velocity, gravity):
    for i in range(len(velocity)):
        velocity[i] += gravity[i]


def apply_axis_velocity(velocity, positions):
    for i in range(len(velocity)):
        positions[i] = positions[i] + velocity[i]


def simulate_axis(positions, velocity, steps):
    for step in range(steps):
        gravity = update_axis_gravity(positions)
        apply_axis_gravity(velocity, gravity)
        apply_axis_velocity(velocity, positions)

    return positions


def predict_axis_loop(axis_positions, axis_velocity):
    initial_positions = axis_positions[:]
    initial_velocity = axis_velocity[:]

    cicles = 1
    while True:
        simulate_axis(axis_positions, axis_velocity, steps=1)
        if axis_positions == initial_positions and axis_velocity == initial_velocity:
            return cicles
        cicles += 1    


def predict_universe_loop(position, velocity):
    cicles = [0,0,0]
    for i in range(len(cicles)):
        cicles[i] = predict_axis_loop([p[i] for p in position], [v[i] for v in velocity])
    return cicles


def lcm(x, y):
    return x * y // math.gcd(x, y)



print('Part Two. Testing')
# Part Two. Test #1
position = [[-1,0,2],[2,-10,-7],[4,-8,8],[3,5,-1]]
velocity = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

cicles = predict_universe_loop(position, velocity)
prediction = reduce(lambda x,y: lcm(x,y), cicles)
assert prediction == 2772


# Part Two. Test #2
position = [[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]]
velocity = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

cicles = predict_universe_loop(position, velocity)
prediction = reduce(lambda x,y: lcm(x,y), cicles)
assert prediction == 4686774924



# Part Two. Predicting
print('Part Two. Predicting universe loop...')

position = read_input()
velocity = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

cicles = predict_universe_loop(position, velocity)
prediction = reduce(lambda x,y: lcm(x,y), cicles)

print('Found! {}'.format(prediction))
















