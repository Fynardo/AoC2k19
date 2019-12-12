from dataclasses import dataclass
from typing import List


# Shared Utilites and functions

@dataclass
class Layer:
    start: int
    data: List[int]
    zeros: int
    ones: int
    twos: int
    check: int


def read_block(image, start, offset):
    return image[start: start + offset]


def decode_layers(image, width, height):
    layer_size = width * height
    layers = []

    pos = 0
    while pos < len(image):
        #print(pos)
        block = read_block(image, pos, layer_size)
        l = Layer(pos, block, 0,0,0,0)
        for pixel in block:
            if pixel == '0':
                l.zeros += 1
            elif pixel == '1':
                l.ones += 1
            elif pixel == '2':
                l.twos += 1
        l.check = l.ones * l.twos
        layers.append(l)
        pos += layer_size
    return layers
    


# Part One
with open('input', 'r') as f:
    image_data = f.read()[:-1] # Remember to remove \n

width = 25
height = 6

    
layers = decode_layers(image_data, width, height)

wanted = min(layers, key=lambda x: x.zeros)

print('Part One: Looking for layer with fewest zeros...')
print(wanted)
print('Part One: Image check: {}'.format(wanted.check))


# Part Two:
def drop_while(f, l):
    for i in l:
        if not f(i):
            return i
               

def decode_colors(layers, width, height):
    image = ''
    layer_size = width * height
    for pixel in range(layer_size):
        color = drop_while(lambda x: x.data[pixel] == '2', layers).data[pixel]
        image +=  color
    return image


print('\nPart Two: Decoding pixel colors...')
decoded_image = decode_colors(layers, width, height)

print('Part Two: Recovering image...')
coded_colors = '01'
decoded_colors = ''.join([' ','#'])
transtable = str.maketrans(coded_colors, decoded_colors)

recovered_image = decoded_image.translate(transtable)
   
pos = 0
while pos < len(recovered_image):    
    print(read_block(recovered_image, pos, width))
    pos += width


























