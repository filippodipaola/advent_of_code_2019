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
    raise ValueError("I HIT A 99 HERE")
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

def format_layer(layer, width=25, length=6):
    fmt_str = ""
    for x in range(length):
        start = x * width
        end = start + width
        line = ["█" if x == '1' else " " for x in layer[start: end]]
        fmt_str = fmt_str + "".join(line) + "\n"
    return fmt_str

def process_pixel(index, layers, depth):
    if layers[depth][index] == "2":
        return process_pixel(index, layers, depth+1)
    else:
        return layers[depth][index]

def process_image(image_layers):
    return_image = [x for x in image_layers[0]]
    for pixel_index in range(len(return_image)):
        depth = 0
        return_image[pixel_index] = process_pixel(pixel_index, image_layers, depth)

    return return_image
def question_8(puzzle_input):
    width = 25
    length = 6
    size = width * length
    layers = {}
    lowest_zeros = 150
    lowest_zero_index = None
    for x in range(len(puzzle_input) // size):
        index = x * size
        end = index + size
        substring = puzzle_input[index:end]
        no_of_zeros = substring.count('0')
        no_of_ones= substring.count('1')
        no_of_twos = substring.count('2')
        layers[x] = {"layer": substring, "0s": no_of_zeros, '1s': no_of_ones, '2s': no_of_twos}
        if no_of_zeros < lowest_zeros:
            lowest_zeros = no_of_zeros
            lowest_zero_index = x

    answer = layers[lowest_zero_index]['1s'] * layers[lowest_zero_index]['2s']
    image_layers = [v['layer'] for k, v in layers.items()]
    final_image = process_image(image_layers)
    binary_format_image = []
    for x in range(len(final_image)):
        binary_format_image.append(final_image[x])
        if (x+1) % 8 == 0:
            binary_format_image.append(" ")

    full_final = "".join(final_image)
    full_binary = "".join(binary_format_image)

    return f"A: {answer}\nB: \n\n{format_layer(full_final)}"




def process_addition_instruction(p, array, param_1, param_2, param_3):

    if param_3:
        array[p + 3] = param_1 + param_2
    else:
        array[array[p + 3]] = param_1 + param_2
    return p + 4, array


def process_multiplication_instruction(p, array, param_1, param_2, param_3):
    if param_3:
        array[p + 3] = param_1 * param_2
    else:
        array[array[p + 3]] = param_1 * param_2
    return p + 4, array


def process_input_instructions(p, array, param_1, usr_in):
    usr_input = usr_in
    array[param_1] = usr_input
    return p + 2, array

def process_out_instruction(p, array, param_1):
    print(param_1)
    return p + 2, array


def jump_if_true(p, param_1, param_2,):

        if param_1 != 0:
            return param_2
        else:
            return p + 3


def jump_if_false(p, param_1, param_2, ):
    if param_1 == 0:
        return param_2
    else:
        return p + 3


def if_less_than(p, array, param_1, param_2, param_3):
    if param_1 < param_2:
        array[param_3] = 1
        return p + 4, array
    else:
        array[param_3] = 0
        return p + 4, array

def if_equal(p, array, param_1, param_2, param_3):
    if param_1 == param_2:
        array[param_3] = 1
        return p + 4, array
    else:
        array[param_3] = 0
        return p + 4, array


def process_optcode(p, array, usr_in):

    C = 0
    B = 0
    A = 0
    whole_optcode = str(array[p])[::-1]
    if len(str(array[p])) > 1:
        optcode = int(whole_optcode[:2][::-1])
        try:
            C = int(whole_optcode[2])
        except IndexError:
            pass

        try:
            B = int(whole_optcode[3])
        except IndexError:
            pass

        try:
            A = int(whole_optcode[4])
        except IndexError:
            pass
    else:
        optcode = array[p]

    if optcode == 1:
        param_1 = array[p+1] if C else array[array[p+1]]
        param_2 = array[p+2] if B else array[array[p+2]]

        return process_addition_instruction(p, array, param_1, param_2, A)
    elif optcode == 2:
        param_1 = array[p + 1] if C else array[array[p + 1]]
        param_2 = array[p + 2] if B else array[array[p + 2]]

        return process_multiplication_instruction(p, array, param_1, param_2, A)
    elif optcode == 3:
        param_1 = array[p + 1]
        return process_input_instructions(p, array, param_1, usr_in)
    elif optcode == 4:
        param_1 = array[p + 1] if A else array[array[p+1]]
        return process_out_instruction(p, array, param_1)
    elif optcode == 5:
        param_1 = array[p + 1] if C else array[array[p + 1]]
        param_2 = array[p + 2] if B else array[array[p + 2]]
        return jump_if_true(p, param_1, param_2), array
    elif optcode == 6:
        param_1 = array[p + 1] if C else array[array[p + 1]]
        param_2 = array[p + 2] if B else array[array[p + 2]]
        return jump_if_false(p, param_1, param_2), array
    elif optcode == 7:
        param_1 = array[p + 1] if C else array[array[p + 1]]
        param_2 = array[p + 2] if B else array[array[p + 2]]
        param_3 = p + 3 if A else array[p + 3]
        return if_less_than(p, array, param_1, param_2, param_3)
    elif optcode == 8:
        param_1 = array[p + 1] if C else array[array[p + 1]]
        param_2 = array[p + 2] if B else array[array[p + 2]]
        param_3 = p + 3 if A else array[p + 3]
        return if_equal(p, array, param_1, param_2, param_3)
    elif optcode == 99:
        return 999999, array
    else:
        raise ValueError(f"UNRECOGNISED OPTCODE: {optcode}")

def intcode_computer_2(input_arr, phase):

    array = input_arr
    p = 0
    phase_count = 0
    output_stat = 0
    while p < len(array):
        #print(f"INDEX: {i}, VALUE: {input_arr[i]}")

        C = 0
        B = 0
        A = 0
        whole_optcode = str(array[p])[::-1]
        if len(str(array[p])) > 1:
            optcode = int(whole_optcode[:2][::-1])
            try:
                C = int(whole_optcode[2])
            except IndexError:
                pass

            try:
                B = int(whole_optcode[3])
            except IndexError:
                pass

            try:
                A = int(whole_optcode[4])
            except IndexError:
                pass
        else:
            optcode = array[p]

        if optcode == 1:
            param_1 = array[p + 1] if C else array[array[p + 1]]
            param_2 = array[p + 2] if B else array[array[p + 2]]

            p, array = process_addition_instruction(p, array, param_1, param_2, A)
        elif optcode == 2:
            param_1 = array[p + 1] if C else array[array[p + 1]]
            param_2 = array[p + 2] if B else array[array[p + 2]]

            p, array = process_multiplication_instruction(p, array, param_1,
                                                      param_2, A)
        elif optcode == 3:
            param_1 = array[p + 1]

            p, array = process_input_instructions(p, array, param_1, phase[phase_count])

            phase_count += 1
        elif optcode == 4:
            param_1 = array[p + 1] if A else array[array[p + 1]]
            output_stat = param_1
            p = p + 2
        elif optcode == 5:
            param_1 = array[p + 1] if C else array[array[p + 1]]
            param_2 = array[p + 2] if B else array[array[p + 2]]
            p = jump_if_true(p, param_1, param_2)
        elif optcode == 6:
            param_1 = array[p + 1] if C else array[array[p + 1]]
            param_2 = array[p + 2] if B else array[array[p + 2]]
            p = jump_if_false(p, param_1, param_2)
        elif optcode == 7:
            param_1 = array[p + 1] if C else array[array[p + 1]]
            param_2 = array[p + 2] if B else array[array[p + 2]]
            param_3 = p + 3 if A else array[p + 3]
            p, array = if_less_than(p, array, param_1, param_2, param_3)
        elif optcode == 8:
            param_1 = array[p + 1] if C else array[array[p + 1]]
            param_2 = array[p + 2] if B else array[array[p + 2]]
            param_3 = p + 3 if A else array[p + 3]
            p, array = if_equal(p, array, param_1, param_2, param_3)
        elif optcode == 99:
            return output_stat, array
        else:
            raise ValueError(f"UNRECOGNISED OPTCODE: {optcode}")


def intcode_computer(input_arr, usr_in):

    i = 0
    while i < len(input_arr):
        #print(f"INDEX: {i}, VALUE: {input_arr[i]}")

        val = input_arr[i]
        return_statements = process_optcode(i, input_arr, usr_in)
        i = return_statements[0]
        input_arr = return_statements[1]
        if len(return_statements) == 3:
            return return_statements[2]





def question_5(puzzle_input, usr_in):
    return intcode_computer([int(x) for x in puzzle_input.split(",")], usr_in)



def question_7_a(puzzle_input):
    biggest_val = 0
    for a in range(0, 5):
        for b in range(0,5):
            for c in range(0,5):
                for d in range(0, 5):
                    for e in range(0, 5):
                        phase_values = [a, b, c, d, e]
                        if len(phase_values) == len(set(phase_values)):
                            return_val = 0
                            for value in phase_values:
                                puz_copy = deepcopy(puzzle_input)
                                return_val, array = intcode_computer_2([int(x) for x in puz_copy.split(",")], [value, return_val])

                            if return_val > biggest_val:
                                biggest_val = return_val
                                # print(f"PHASE INPUT: {phase_values}, RESULT: {return_val}")

    return biggest_val


def question_7_b(puzzle_input):
    biggest_val = 0
    bot = 5
    top = 10
    for a in range(bot, top):
        for b in range(bot, top):
            for c in range(bot, top):
                for d in range(bot, top):
                    for e in range(bot, top):
                        phase_values = [a, b, c, d, e]
                        if len(phase_values) == len(set(phase_values)):
                            return_val = 0
                            puz_dict = {}
                            while True:
                                phase_values
                                for value in phase_values:
                                    if value in puz_dict:
                                        process_puz = puz_dict[value]

                                    else:
                                        puz_in = deepcopy(puzzle_input)
                                        process_puz = [int(x) for x in
                                                       puz_in.split(",")]
                                        puz_dict[value] = process_puz


                                    return_val, array = intcode_computer_2(process_puz, [value, return_val])
                                    puz_dict[value] = array
                                    print(puz_dict[5])

                                    if return_val == "EXIT":
                                        break

                            if return_val > biggest_val:
                                biggest_val = return_val
                                #print(f"PHASE INPUT: {phase_values}, RESULT: {return_val}")

    return biggest_val


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

    with open("puzzle_input_5.txt", "r") as read_in:
        puzzle_input_5 = read_in.read()

    #print("Q5_a")
    #question_5(puzzle_input_5, 1)

    #print("Q5_b")
    #question_5(puzzle_input_5, 5)

    puzzle_input_6 =[]
    with open("puzzle_input_6.txt", "r") as pz_in_6:
        for line in pz_in_6:
            puzzle_input_6.append(line.strip())

    #print(f"Q6: {question_6(puzzle_input_6)}")


    with open("puzzle_input_7.txt", "r") as pz_in_7:
        puzzle_input_7 = pz_in_7.read()
    print(f"Q7a: {question_7_a(puzzle_input_7)}")
    print(f" Q7b {question_7_b(puzzle_input_7)}")




    with open("puzzle_input_8.txt", "r") as pz_in_8:

        puzzle_input_8 = pz_in_8.read()

    #print(f"Q8: {question_8(puzzle_input_8)}")