"""
Geometry related information:

M = Monitor
# = Asteroid
. = Empty

Axis:
    X: >
    Y: v

 x-,y-       x+,y-
    # . . . #
    . . . . .
    . a M . .
    . . . . b
    # . . . #
 x-,y+       x+,y+

let a = (1,2)
let b = (4,3)

slope(a, b) = (4-1) / (3-2) = 2 / 1 = 2
angle(a, b) = arctan(2) ~ 1.107 rad ~ 63.43 grad

With this axis, 63 grad is in fourth quarter, but we need it in first quarter.
So, for this 63.43 grad  what we want is 2-> 360 - 63.43 = 296,57
"""

from math import atan, pi


def rad_to_grad(rad):
    return rad * 180 / pi

def grad_to_rad(grad):
    return grad * pi / 180


def calculate_angle(p1, p2):
    """ For the angle I calculate the slope of the line between the points, with that slope: angle = arctan(slope). Thing is that axis are pretty messed up so I need to rotate the map"""

    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    angle = None
    if delta_x == 0:
        return 90 if delta_y < 0 else 270
    if delta_y == 0:
        return 0 if delta_x > 0 else 180 

    slope = abs(delta_y / delta_x)
    angle = rad_to_grad(atan(slope))
    if delta_x > 0 and delta_y < 0:
        angle = angle
    if delta_x > 0 and delta_y > 0:
        angle = 360 - angle
    elif delta_x < 0 and delta_y > 0:
        angle = 270 - angle
    elif delta_x < 0 and delta_y < 0:
        angle = 180 - angle
    return angle


def detect_asteroids(asteroids_map, x, y):
    angles = set()
    for i, row in enumerate(asteroids_map):
        for j, pos in enumerate(row):            
            if pos == '#' and (x,y) != (j,i):
                a = calculate_angle((x,y),(j,i))
                angles.add(a)   
    return len(angles)
            

def detect_all_asteroids(asteroids_map):
    """ For every astroid in the map, count how many asteroids are in LoS. Yes, it is O(n^2).""" 
 
    monitor = {}
    for i, row in enumerate(asteroids_map):
        for j, pos in enumerate(row):
            if pos == '#':
                monitor[(j,i)] = detect_asteroids(asteroids_map, j, i)
   
    detected = max(monitor.values())
    coords = [k for k,v in monitor.items() if v == detected][0]
    return coords, detected


# Part One
test_maps = [
    ['......#.#.',
    '#..#.#....',
    '..#######.',
    '.#.#.###..',
    '.#..#.....',
    '..#....#.#',
    '#..#....#.',
    '.##.#..###',
    '##...#..#.',
    '.#....####'],
    ['#.#...#.#.',
    '.###....#.',
    '.#....#...',
    '##.#.#.#.#',
    '....#.#.#.',
    '.##..###.#',
    '..#...##..',
    '..##....##',
    '......#...',
    '.####.###.'], 
    ['.#..#..###',
    '####.###.#',
    '....###.#.',
    '..###.##.#',
    '##.##.#.#.',
    '....###..#',
    '..#.#..#.#',
    '#..#.#.###',
    '.##...##.#',
    '.....#.#..'],
    ['.#..##.###...#######',
    '##.############..##.',
    '.#.######.########.#',
    '.###.#######.####.#.',
    '#####.##.#.##.###.##',
    '..#####..#.#########',
    '####################',
    '#.####....###.#.#.##',
    '##.#################',
    '#####.##.###..####..',
    '..######..##.#######',
    '####.##.####...##..#',
    '.#####..#.######.###',
    '##...#.##########...',
    '#.##########.#######',
    '.####.#.###.###.#.##',
    '....##.##.###..#####',
    '.#.#.###########.###',
    '#.#.#.#####.####.###',
    '###.##.####.##.#..##',]
]


test_detected = [33, 35, 41, 210]
test_spots = [(5,8), (1,2), (6,3), (11,13)]

print("Part One. Testing")

for i, test in enumerate(test_maps):
    best_spot, detected = detect_all_asteroids(test)
    assert best_spot == test_spots[i]
    assert detected == test_detected[i]
    

with open('input','r') as f:
    asteroids_map = f.read().splitlines()

best_spot, detected = detect_all_asteroids(asteroids_map)
print('Part One. Best location for monitor discovered at {}, with {} asteroids in LoS'.format(best_spot, detected))


# Part Two
def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def target_asteroids(asteroids_map, spot):
    """ Detects all asteroids with angle of sight """

    angles = {}
    for i, row in enumerate(asteroids_map):
        for j, pos in enumerate(row):            
            if pos == '#' and spot != (j,i):
                a = calculate_angle(spot, (j,i))
                if a in angles:
                    angles[a].append((j,i))
                else:
                    angles[a] = [(j,i)] 
                angles[a] = sorted(angles[a], key=lambda x: distance(x, spot))
    return angles


def initialize_vaporizer(target_angles, init_angle):
    i = 0
    while target_angles[i] > init_angle:
        i += 1
    return i
    
def vaporize_targets(targets):
    """ Sets the vaporizer to 90 grad, then rotates clockwise vaporizing every asteroid. Finishes when 200th asteroid is vaporized"""

    n = len(targets)
    target_angles = sorted(targets.keys(), reverse=True)
    init_angle = 90
    pointer = initialize_vaporizer(target_angles, init_angle)
    vaporized_count = 0
    while vaporized_count < 200:
        target_angle = target_angles[pointer]
        #print('\nTargetin angle {}. targets: {}'.format(target_angle, targets[target_angle]))
        if len(targets[target_angle]) > 0:
            vaporized_asteroid = targets[target_angle].pop(0)
            vaporized_count += 1
            #print('Vaporizing: {}'.format(vaporized_asteroid))
            #print('Vaporized {} asteroids'.format(vaporized_count))
            #print('Targets left: {}'.format(targets[target_angle]))
 
        pointer = (pointer + 1) % n
    return vaporized_asteroid


monitor_location = (23, 19)
targets = target_asteroids(asteroids_map, monitor_location)
print('Vaporizing Asteroids...')
print('Asteroid vaporized in 200th position is... {}!!!'.format(vaporize_targets(targets)))










