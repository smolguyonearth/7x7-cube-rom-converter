#convert from picture to ROM memory

'''
1  2  3  4  5  6  7
8  9  10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31 32 33 34 35
36 37 38 39 40 41 42
43 44 45 46 47 48 49
'''

from PIL import Image
import numpy as np
import json

def map_rgb_to_tensor(rgb):
    if rgb[0] > 100 and rgb[1] < 100 and rgb[2] < 100:
        return [0, 1, 1]
    elif rgb[0] < 100 and rgb[1] < 100 and rgb[2] > 100:
        return [1, 1, 0]
    elif rgb[0] < 100 and rgb[1] > 100 and rgb[2] < 100:
        return [1, 0, 1]
    else:
        return [1, 1, 1]

def layer():

    variable = ["layer0.png", "layer1.png", "layer2.png", "layer3.png", "layer4.png", "layer5.png", "layer6.png"]

    for i in range(7):
        image = Image.open("picture/" + variable[i]).convert("RGB")
        image_array = np.array(image)

        tensor = []

        for row in image_array:
            tensor_row = [map_rgb_to_tensor(pixel) for pixel in row]
            tensor.append(tensor_row)

        json_data = json.dumps(tensor)

        # print(json_data)

        with open("picture tensors/" + str(i) + "_tensor.json", "w") as json_file:
            json.dump(tensor, json_file)
            i+=1


def get_bits():
    for i in range(7):

        file_path = 'picture tensors/' + str(i) + '_tensor.json'

        with open(file_path, 'r') as file:
            data = json.load(file)

        def get_bits(data):
            bits = ''
            for row in data:
                for pixel in row:
                    bits += str(pixel)
            return bits

        def create_data(data):
            red = []
            for row in data:
                r = [item[0] for item in row] 
                red.append(r)
            red_bits = get_bits(red)

            green = []
            for row in data:
                r = [item[1] for item in row] 
                green.append(r)
            green_bits = get_bits(green)

            blue = []
            for row in data:
                r = [item[2] for item in row] 
                blue.append(r)
            blue_bits = get_bits(blue)

            return red_bits, green_bits, blue_bits

        red_bits, green_bits, blue_bits = create_data(data)
        print("red layer_" + str(i), red_bits)
        print("green layer_" + str(i), green_bits)
        print("blue layer_" + str(i), blue_bits)

        with open('rom/red.mem', 'a') as file:
            file.write(red_bits + "\n")
        with open('rom/green.mem', 'a') as file:
            file.write(green_bits + "\n")
        with open('rom/blue.mem', 'a') as file:
            file.write(blue_bits + "\n")

layer()
get_bits()