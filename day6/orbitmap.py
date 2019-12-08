# Day 6: Universal Orbit Map

def generate_orbit_map(data):
    orbit_map = {}
    for pair in data:
        o1, o2 = pair.split(')')
        # Construyo el arbol        
        if o1 not in orbit_map:
            orbit_map[o1] = []
        if o2 not in orbit_map:
            orbit_map[o2] = []

        orbit_map[o1].append(o2)
    return orbit_map


def calculate_orbit_checksum(orbit_map):
    orbit_checksum = 0
    root = 'COM'
    current_level = 0
    frontier = ['COM']
    explored = set()
    while frontier:
        node = frontier[0]
        if node not in explored:
            orbit_checksum += current_level
            explored.add(node)    
            frontier = orbit_map[node] + frontier
            current_level += 1                               
        else:
            current_level -= 1
            frontier.pop(0)        
    return orbit_checksum

# Part One: Testing
print('Part One: Testing')
with open('test', 'r') as f:
    test_data = f.read().splitlines()

orbit_map = generate_orbit_map(test_data)
chk = calculate_orbit_checksum(orbit_map)
assert chk == 42

# Part One: Orbit Count
with open('input', 'r') as f:
    data = f.read().splitlines()

orbit_map = generate_orbit_map(data)
chk = calculate_orbit_checksum(orbit_map)
print('Part One: Orbit Checksum: {}'.format(chk))


# Part Two
def path_to_node(target, orbit_map):
    root = 'COM'
    frontier = ['COM']
    explored = set()
    path = []
    while frontier:
        node = frontier[0]
        if node == target:
            return path
        if node not in explored:
            explored.add(node)
            path.append(node) 
            frontier = orbit_map[node] + frontier
        else:
            path.remove(node)
            frontier.pop(0)        

path_to_you = path_to_node('YOU', orbit_map)
path_to_san = path_to_node('SAN', orbit_map)

print("Part Two: Distance from YOU to SAN: {}".format(len(set(path_to_you).union(set(path_to_san)) - set(path_to_you).intersection(set(path_to_san)))))


