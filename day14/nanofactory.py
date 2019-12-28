import math


def load_input(path='input'):
    with open(path, 'r') as f:
        data = f.read().splitlines()
    reaction_table = {}
    for d in data:
        inputs, outputs = d.split(' => ')
        output_count, output_chemical = outputs.split(' ')
        recipe = {'IN': [], 'OUT': int(output_count)}
        for reagent in inputs.split(', '):
            q, ch = reagent.split(' ')
            recipe['IN'].append((ch, int(q)))
        reaction_table[output_chemical] = recipe
    return reaction_table


def accumulate_chemicals(r1, r2):
    for k, v in r1.items():
        if k in r2:
            r2[k] += v
        else:
            r2[k] = v
    return r2


def calculate_primitive_chemicals(wanted='FUEL', quantity=1):
    reaction = reaction_table[wanted]
    inputs = reaction['IN']
    output = reaction['OUT']
    primitives = {}

    if len(inputs) == 1 and inputs[0][0] == 'ORE':  # Puf
        pass
    else:
        if wanted in stock_table and stock_table[wanted] > 0:
            quantity -= stock_table[wanted]
            stock_table[wanted] = 0
        fabricate = math.ceil(quantity / output) * output
        if fabricate > quantity:
            stock_table[wanted] = fabricate - quantity

    for chemical, count in inputs:
        if chemical == 'ORE':
            primitives[wanted] = quantity
        else:
            primitives = accumulate_chemicals(primitives, calculate_primitive_chemicals(chemical, math.ceil(quantity/output)*count))
    return primitives


def calculate_needed_ores(chemicals):
    acc = 0
    for chemical, quantity in chemicals.items():
        ores = reaction_table[chemical]['IN'][0][1]
        output = reaction_table[chemical]['OUT']
        needed = math.ceil(quantity / output) * ores
        acc += needed
    return acc


# PART 1
stock_table = {}
reaction_table = load_input('input')
chemicals = calculate_primitive_chemicals()
part1 = calculate_needed_ores(chemicals)
print('Part #1. Factory needs {} ORE to produce 1 FUEL'.format(part1))


# PART 2
trillion = 1000000000000
ores = 0
fuel = 1
incr = trillion // part1

while incr >= 1:
    fuel += incr
    stock_table = {}
    chemicals = calculate_primitive_chemicals(quantity=fuel)
    ores = calculate_needed_ores(chemicals)
    # print(incr)
    if ores > trillion:
        fuel -= incr
        incr //= 10


print('Part #2. With one trillion ORE, {} units of fuel can be produced'.format(fuel))


