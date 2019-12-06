puzzle_input = (272091, 815432)

"""
Part One constraints
  1 It is a six-digit number. 
  2 The value is within the range given in your puzzle input.
  3 Two adjacent digits are the same (like 22 in 122345).
  4 Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

  No need to check 1 and 2, puzzle input range assures those.
"""


def has_adjacent_digits(s):
    return any(map(lambda x: x[0] == x[1], zip(s, s[1:])))


def increases(s):
    return all(map(lambda x: x[0] <= x[1], zip(s, s[1:])))


# Part One:
valid_count = 0
for i in range(*puzzle_input):
    s = str(i)
    if has_adjacent_digits(s) and increases(s):
        valid_count += 1

print('Part One. Total count of valid numbers: {}'.format(valid_count))

"""
Part Two additional constraint
    * At least one group of digits must be a pair
"""

def just_one_pair(s):
    table = {i: [] for i in range(len(s))}
    reps = 0
    retval = False
    for p in zip(s, s[1:]):
        if p[0] == p[1]:
            reps += 1
        else:
            table[reps] += p[0]
            reps = 0
    table[reps] += p[0]
    return True if table[1] else False


# Part Two:
valid_count = 0
for i in range(*puzzle_input):
    s = str(i)
    if just_one_pair(s) and increases(s):
        valid_count += 1

print('Part Two. Total count of valid numbers: {}'.format(valid_count))

