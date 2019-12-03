class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def shift(self, direction, distance):
        if direction == 'U':
            return Point(self.x, self.y + distance)
        elif direction == 'R':
            return Point(self.x + distance, self.y)
        elif direction == 'D':
            return Point(self.x, self.y - distance)
        elif direction == 'L':
            return Point(self.x - distance, self.y)

    def intermediate_points(self, direction, distance):
        points = set()
        for i in range(1, abs(distance)+1):
            points.add(self.shift(direction, i))
        return points

    def manhattan(self, other):
        return (abs(self.x - other.x) + abs(self.y- other.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))


def decode(cmd):
    return cmd[0], int(cmd[1:])


def create_wire_set(wire_path, base_coord):
    actual_coord = base_coord
    wire_set = set()
    for hop in wire_path:
        direction, distance = decode(hop)
        for ip in actual_coord.intermediate_points(direction, distance):
            wire_set.add(ip)
        actual_coord = actual_coord.shift(direction, distance)
    return wire_set


def find_crosses(wire_paths):
    wire_sets = [create_wire_set(path, base_coord) for path in wire_paths]
    crosses = wire_sets[0].intersection(wire_sets[1])
    return crosses


def calculate_min_distance(crosses):
    min_distance = min([base_coord.manhattan(c) for c in crosses])
    return min_distance


### Part One ###
base_coord = Point(0,0)

# Tests
print("Testing Part One:")

wire_paths = [['R8','U5','L5','D3'],['U7','R6','D4','L4']]
crosses = find_crosses(wire_paths)
assert 6 == calculate_min_distance(crosses)

wire_paths = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'], ['U62','R66','U55','R34','D71','R55','D58','R83']]
crosses = find_crosses(wire_paths)
assert 159 == calculate_min_distance(crosses)

wire_paths = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'], ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]
crosses = find_crosses(wire_paths)
assert 135 == calculate_min_distance(crosses)


# Fix input circuit
with open('input','r') as f:
    wire_paths = [l.split(',') for l in f.read().splitlines()]

crosses = find_crosses(wire_paths)
print('Part One: Minimum distance is {}'.format(calculate_min_distance(crosses)))


### Part Two ###
def calculate_steps(wire_paths, crosses):
    crosses_table = {c:0 for c in crosses}
    #print(crosses_table)
    for wire_path in wire_paths:
        actual_coord = base_coord
        distance_acum = 0
        for hop in wire_path:
            direction, distance = decode(hop)        
            segment = actual_coord.intermediate_points(direction, distance)
            intersections = filter(lambda x: x in crosses, segment)
            for i in intersections:
                partial_distance = actual_coord.manhattan(i)
                crosses_table[i] += distance_acum + partial_distance
            distance_acum += abs(distance)
            actual_coord = actual_coord.shift(direction, distance)
    return crosses_table

# Tests
print("Testing Part Two:")
wire_paths = [['R8','U5','L5','D3'],['U7','R6','D4','L4']]
crosses = find_crosses(wire_paths)
steps = calculate_steps(wire_paths, crosses)
min_steps = min([v for v in steps.values()])
assert 30 == min_steps
    

wire_paths = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'], ['U62','R66','U55','R34','D71','R55','D58','R83']]
crosses = find_crosses(wire_paths)
steps = calculate_steps(wire_paths, crosses)
min_steps = min([v for v in steps.values()])
assert 610 == min_steps

wire_paths = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'], ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]
crosses = find_crosses(wire_paths)
steps = calculate_steps(wire_paths, crosses)
min_steps = min([v for v in steps.values()])
assert 410 == min_steps


# Fix input circuit
with open('input','r') as f:
    wire_paths = [l.split(',') for l in f.read().splitlines()]

crosses = find_crosses(wire_paths)
steps = calculate_steps(wire_paths, crosses)
min_steps = min([v for v in steps.values()])
print('Part Two: Minimum number of steps is {}'.format(min_steps))







