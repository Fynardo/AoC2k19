# Load input data
with open("input.txt", 'r') as f:
    mass = f.readlines()

## each mass is read as string, lets parse it to int so we can operate with it.
mass = [int(m) for m in mass]

# Part One:
total_fuel = sum([m // 3 - 2 for m in mass])
print('Part 1: {}'.format(total_fuel))


# Part Two:
def calculate_fuel(module_mass):
    module_fuel = module_mass // 3 - 2
    remaining_fuel = module_fuel
    while remaining_fuel > 6:
        remaining_fuel = remaining_fuel // 3 - 2
        module_fuel += remaining_fuel
    return module_fuel

def fuel_rec(module_mass):
    fuel = module_mass // 3 - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + fuel_rec(fuel)


total_fuel = sum([calculate_fuel(m) for m in mass])
print('Part 2: {}'.format(total_fuel))
print('Part 2 (rec): {}'.format(sum([fuel_rec(m) for m in mass])))

