import math
from copy import deepcopy
import json

def load_puzzle_input(file_loc):
    with open(file_loc, "r") as in_file:
        puz_input = in_file.read()
        return [float(x) for x in puz_input.splitlines()]

def load_puzzle_input_3(file_name):
    with open(file_name, "r") as in_file:
        wire_1 = in_file.readline().split(",")
        wire_2 = in_file.readline().split(",")

    return wire_1, wire_2

def calculate_fuel_requirement(mass):
    return math.floor(mass / 3.0) - 2

def calculate_fuel_requirement_recursive(mass):
    f_req = calculate_fuel_requirement(mass)
    sum = f_req
    while True:
        f_req = calculate_fuel_requirement(f_req)
        if f_req > 0:
            sum += f_req
        else:
            break

    return sum

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def end(a, b):
    return None

def process_int_code(int_code, array):
    instr, in_a, in_b, out = int_code
    opt = {1: add, 2: multiply, 99: end}
    result = opt[instr](array[in_a], array[in_b])
    if result:
        array[out] = result

    return array

def process_int_code_w_breakpoint(int_code, array, breakpoint):
    instr, in_a, in_b, out = int_code
    opt = {1: add, 2: multiply, 99: end}
    result = opt[instr](array[in_a], array[in_b])
    if result:
        if result == breakpoint:
            return in_a, in_b
        array[out] = result

    return array

def add_points_to_set(pos, i, dist, set_point):

    if dist < 0:
        point_list = list(range(dist-1, pos[i]))
    else:
        point_list = list(range(pos[i]+1, dist))

    temp_pos = list(deepcopy(pos))
    for x in point_list:
        temp_pos[i] = x
        temp_pos = temp_pos
        set_point.add(json.dumps(tuple(temp_pos)))

    pos = list(pos)
    pos[i] = pos[i] + dist
    print(f"POS FOR WHATEVER: {pos}")
    return tuple(pos)



def process_wire_to_set(wire):
    path = set()
    origin = (0,0)
    pos = (0,0)
    for instr in wire:
        direction = instr[0]
        dist = int(instr[1:])
        if direction == 'U':
            pos = add_points_to_set(pos, 1, dist, path)
        elif direction == 'D':
            pos = add_points_to_set(pos, 1, -dist, path)
        elif direction == 'R':
            pos = add_points_to_set(pos, 0, dist, path)
        elif direction == 'L':
            pos = add_points_to_set(pos, 0, -dist, path)
        else:
            raise ValueError
    return path

def question_1_a(puz_in):
    sum = 0
    for x in puz_in:
        sum += calculate_fuel_requirement(x)
    return sum

def question_1_b(puz_in):
    sum = 0
    for x in puz_in:
        sum += calculate_fuel_requirement_recursive(x)
    return sum

def question_2_a(puz_in):

    array = deepcopy(puz_in)
    for x in range(int((len(puz_in) + 1) / 4)):
        i = x * 4
        array = process_int_code(array[i:i + 4], array)


    return array


def question_2_b(puz_in):
    for x in range(99):
        for y in range(99):
            array = deepcopy(puz_in)
            array[1] = x; array[2] = y
            result = question_2_a(array)[0]
            if result == 19690720:
                return 100 * x + y


def question_3_a(wire_1, wire_2):
    wire_set_1 = process_wire_to_set(wire_1)
    wire_set_2 = process_wire_to_set(wire_2)
    print(f"WIRE_SET 1: {wire_set_1}")
    print(f"WIRE_SET 2: {wire_set_2}")
    crosses = wire_set_1.intersection(wire_set_2)
    coords = [json.loads(x) for x in crosses]
    print(coords)
    man_dist = [abs(tup[0])+abs(tup[1]) for tup in coords]
    print(man_dist)
    return coords[man_dist.index(min(man_dist))]


if __name__ == "__main__":
    puz_in = load_puzzle_input("puzzle_input.txt")
    print(f"Q1a: {question_1_a(puz_in)}")
    print(f"Q1b: {question_1_b(puz_in)}")
    puz_in = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0,
              3, 2, 1, 9, 19 ,1 ,19, 5, 23, 2, 23, 13, 27,
              1, 10, 27, 31, 2, 31, 6, 35, 1, 5, 35, 39, 1,
              39, 10, 43, 2, 9, 43, 47, 1, 47, 5, 51, 2, 51,
              9, 55, 1, 13, 55, 59, 1, 13, 59, 63, 1, 6, 63,
              67, 2, 13, 67, 71, 1, 10, 71, 75, 2, 13, 75,
              79, 1, 5, 79, 83, 2, 83, 9, 87, 2, 87, 13, 91,
              1, 91, 5, 95, 2, 9, 95, 99, 1, 99, 5, 103, 1,
              2, 103, 107, 1, 10, 107, 0, 99, 2, 14, 0, 0]
    print(f"Q2a: {question_2_a(puz_in)}")
    puz_in = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0,
              3, 2, 1, 9, 19, 1, 19, 5, 23, 2, 23, 13, 27,
              1, 10, 27, 31, 2, 31, 6, 35, 1, 5, 35, 39, 1,
              39, 10, 43, 2, 9, 43, 47, 1, 47, 5, 51, 2, 51,
              9, 55, 1, 13, 55, 59, 1, 13, 59, 63, 1, 6, 63,
              67, 2, 13, 67, 71, 1, 10, 71, 75, 2, 13, 75,
              79, 1, 5, 79, 83, 2, 83, 9, 87, 2, 87, 13, 91,
              1, 91, 5, 95, 2, 9, 95, 99, 1, 99, 5, 103, 1,
              2, 103, 107, 1, 10, 107, 0, 99, 2, 14, 0, 0]
    #print(f"Q2b: {question_2_b(puz_in)}")

    wire_1, wire_2 = load_puzzle_input_3("puzzle_input_3.txt")
    print(f"Q3a: {question_3_a(wire_1, wire_2)}")