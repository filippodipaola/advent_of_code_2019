import math
from copy import deepcopy
import json
import pprint
from anytree import Node, RenderTree

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

def generate_line_dict(pos_1, pos_2, running_dist_start=0, running_dist_end=0):
    return {
        'x1': pos_1[0],
        'x2': pos_2[0],
        'y1': pos_1[1],
        'y2': pos_2[1],
        'running_dist_start': deepcopy(running_dist_start),
        'running_dist_end': deepcopy(running_dist_end)
    }

def generate_new_coordinate(current_pos, index, distance):
    new_position = deepcopy(current_pos)
    new_position[index] += distance
    return new_position

def convert_directions_to_coorinates(directions):

    coordinates = []
    last_coordinate = [0,0]
    line_list = []
    running_dist = 0
    for instr in directions:
        direction = instr[0]
        dist = int(instr[1:])
        if direction == 'U':
            pos = generate_new_coordinate(last_coordinate, 1, dist)
        elif direction == 'D':
            pos = generate_new_coordinate(last_coordinate, 1, -dist)
        elif direction == 'R':
            pos = generate_new_coordinate(last_coordinate, 0, dist)
        elif direction == 'L':
            pos = generate_new_coordinate(last_coordinate, 0, -dist)
        else:
            raise ValueError
        line_list.append(generate_line_dict(last_coordinate, pos, running_dist, running_dist+dist))
        last_coordinate = deepcopy(pos)
        running_dist += dist

    return line_list

def calculate_intersections(line_list_1, line_list_2):
    intersect_points = []
    intersect_distance = []
    for l1 in line_list_1:
        for l2 in line_list_2:
            y1 = l1['y1']; y2 = l1['y2']; y3 = l2['y1']; y4 = l2['y2']
            x1 = l1['x1']; x2 = l1['x2']; x3 = l2['x1']; x4 = l2['x2']
            try:
                t_a = ((y3 - y4) * (x1 - x3) + (x4 - x3) * (y1 - y3)) / ((x4 - x3) * (y1 -y2) - (x1 - x2) * (y4 - y3))
                t_b = ((y1 - y2) * (x1 - x3) + (x2 - x1) * (y1 - y3)) / ((x4 - x3) * (y1 - y2) - (x1 - x2) * (y4 - y3))
            except ZeroDivisionError:
                continue

            if (0 <= t_a <= 1) and (0 <= t_b <= 1):
                intersection_point = [x1 + t_a * (x2 - x1), y1+ t_a * (y2 - y1)]
                if intersection_point == [0.0, 0.0]:
                    pass
                else:
                    intersect_points.append(intersection_point)
                    xt = intersection_point[0]; yt = intersection_point[1]
                    d_a = abs((abs(xt) - abs(x1)) + (abs(yt) - abs(y1)))
                    d_b = abs((abs(xt) - abs(x3)) + (abs(yt) - abs(y3)))
                    intersect_distance.append(l1['running_dist_start'] + l2['running_dist_start'] + d_a + d_b)

    return intersect_points, intersect_distance

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
    wire_set_1 = convert_directions_to_coorinates(wire_1)
    wire_set_2 = convert_directions_to_coorinates(wire_2)
    intersections, intersect_distance = calculate_intersections(wire_set_1, wire_set_2)
    manhatten_dists = [abs(x[0]) + abs(x[1]) for x in intersections]
    return f"CLOSEST BY MANHATTEN {min(manhatten_dists)}, CLOSEST BY STEPS {min(intersect_distance)}"


def check_password_for_doubles(pass_str):
    prev_num = None
    for num in pass_str:
        if prev_num == num:
            return True
        prev_num = num

def check_pass_for_single_doubles(pass_str):
    # unique_nums = set(pass_str)
    # for num in unique_nums:
    #     if pass_str.count(num+num) == 2 and pass_str.count(num+num+num) == 0:
    #         return True
    prev_num = None
    double_count = 0
    for num in pass_str:

        if prev_num == num:
            double_count += 1
        elif double_count == 1:
            return True
        else:
            double_count = 0

        prev_num = num

    if double_count == 1:
        return True
def check_for_decending(pass_str):
    prev_num = 0
    for num in pass_str:
        int_num = int(num)
        if prev_num > int_num:
            return False
        prev_num = int_num

    return True

def question_4_a(range_start, range_end):
    no_of_combinations = 0
    for password in range(range_start, range_end):
        pass_str = str(password)
        # Check for doubles
        if check_password_for_doubles(pass_str):
            if check_for_decending(pass_str):
                no_of_combinations += 1

    return no_of_combinations

def question_4_b(range_start, range_end):
    no_of_combinations = 0
    for password in range(range_start, range_end):
        pass_str = str(password)
        # Check for doubles
        if check_pass_for_single_doubles(pass_str):
            if check_for_decending(pass_str):
                no_of_combinations += 1

    return no_of_combinations


def get_tree(puzzle_input):
    nodes = {}
    trees = []
    for input in puzzle_input:
        parent, child = input.split(')')
        if parent in nodes:
            if child in nodes:
                nodes[child].parent = nodes[parent]
            else:
                nodes[child] = Node(child, parent=nodes[parent])
        else:
            nodes[parent] = Node(parent)
            if child in nodes:
                nodes[child].parent = nodes[parent]
                #nodes[parent].children = nodes[child]
            else:
                nodes[child] = Node(child, parent=nodes[parent])




    return [nodes['COM'], nodes['YOU'], nodes['SAN']]



def question_6(puzzle_input):
    COM, YOU, SANTA = get_tree(puzzle_input)
    total_orbits = 0

    for pre, file, node in RenderTree(COM):
        orbits = str(node.parent).count('/')
        total_orbits += orbits
        print(f"{pre}{node.name} - Orbits: {orbits}")

    you_parents = set(str(YOU.parent).split('/')[1:])
    santa_parents = set(str(SANTA.parent).split('/')[1:])
    you_parents.symmetric_difference(santa_parents)



    return f"A: {total_orbits} B: {len(you_parents.symmetric_difference(santa_parents))}"

if __name__ == "__main__":
    check_pass_for_single_doubles("111122")
    puz_in = load_puzzle_input("puzzle_input.txt")
    #print(f"Q1a: {question_1_a(puz_in)}")
    #print(f"Q1b: {question_1_b(puz_in)}")
    puz_in = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0,
              3, 2, 1, 9, 19 ,1 ,19, 5, 23, 2, 23, 13, 27,
              1, 10, 27, 31, 2, 31, 6, 35, 1, 5, 35, 39, 1,
              39, 10, 43, 2, 9, 43, 47, 1, 47, 5, 51, 2, 51,
              9, 55, 1, 13, 55, 59, 1, 13, 59, 63, 1, 6, 63,
              67, 2, 13, 67, 71, 1, 10, 71, 75, 2, 13, 75,
              79, 1, 5, 79, 83, 2, 83, 9, 87, 2, 87, 13, 91,
              1, 91, 5, 95, 2, 9, 95, 99, 1, 99, 5, 103, 1,
              2, 103, 107, 1, 10, 107, 0, 99, 2, 14, 0, 0]
    #print(f"Q2a: {question_2_a(puz_in)}")
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
    #print(f"Q3a: {question_3_a(wire_1, wire_2)}")

    #print(f"Q4a: {question_4_a(153517, 630395)}")
    #print(f"Q4b: {question_4_b(153517, 630395)}")
    puzzle_input_6 =[]
    with open("puzzle_input_6.txt", "r") as pz_in_6:
        for line in pz_in_6:
            puzzle_input_6.append(line.strip())

    print(f"Q6: {question_6(puzzle_input_6)}")