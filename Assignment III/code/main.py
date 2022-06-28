import sys
import os
import tracemalloc
from time import time
from itertools import permutations

#returns a list of characters from a comma separated string
def convert(stringLine):
    array = []
    array = stringLine.replace("\n", '').split(",")
    return array

#function to parse the input file into a matrix
def matrix_superimpose(input_data):
    horizontal, vertical, row, column = input_data
    for i in range(row):
        for j in range(column):
            if horizontal[i][j] == '#':
                if vertical[i][j] != '#':
                    horizontal[i][j] = [int(vertical[i][j]), '']
            elif horizontal[i][j] != '0':
                if vertical[i][j] == '#':
                    horizontal[i][j] = ['', int(horizontal[i][j])]
                else:
                    horizontal[i][j] = [int(vertical[i][j]), int(horizontal[i][j])]
            else:
                horizontal[i][j] = 0
    return horizontal

#function to read the input file
def read_file(input_file):
    row = 0
    column = 0
    matrixInput = []
    with open(input_file, 'r') as file:
        for line in file:
            if "row" in line:
                line.replace("rows=", '')
                row = int(line.replace("rows=", ''))
            elif "column" in line:
                line.replace("columns=", '')
                column = int(line.replace("columns=", ''))
            elif "Horizontal" not in line and "Vertical" not in line:
                matrixInput.append(convert(line))
        #print (line)
    horizontal = matrixInput[0 : row]
    vertical = matrixInput[row : 2 * row]
    #return a tuple of the parsed data
    return (horizontal, vertical, row, column)

'''
function that finds the variables, domains, neighbours
does binarization of constraints and adds hidden variables
to convert n ary csp to binary csp
'''
def neighbours(matrix, row, col):
    variables = []
    domain = {}
    neighbours = {}
    for i in range(row):
        for j in range(col):
            if matrix[i][j] == 0:
                var = "X" + str(i) + "," + str(j)
                variables.append(var)

                domain[var] = list(map(str, list(range(1, 10))))

            #for rows
            if matrix[i][j] != 0 and matrix[i][j] != '#':

                if matrix[i][j][0] != '':
                    hidden_bin = "C_d" + str(i) + ',' + str(j)
                    variables.append(hidden_bin)

                    counter = 0
                    for m in range(i + 1, row):
                        if matrix[m][j] != 0:
                            break

                        nei = "X" + str(m) + "," + str(j)
                        if hidden_bin not in neighbours:
                            neighbours[hidden_bin] = []
                        neighbours[hidden_bin].append(nei)

                        if nei not in neighbours:
                            neighbours[nei] = []
                        neighbours[nei].append(hidden_bin)

                        counter += 1
                    perms = list(map("".join, permutations('123456789', counter)))
                    domain[hidden_bin] = [perm for perm in perms if sum(int(x) for x in perm) == matrix[i][j][0]]

                #for columns
                if matrix[i][j][1] != '':
                    hidden_bin = "C_r" + str(i) + "," + str(j)
                    variables.append(hidden_bin)

                    counter = 0
                    for k in range(j + 1, col):
                        if matrix[i][k] != 0:
                            break

                        nei = "X" + str(i) + "," + str(k)
                        if hidden_bin not in neighbours:
                            neighbours[hidden_bin] = []
                        neighbours[hidden_bin].append(nei)

                        if nei not in neighbours:
                            neighbours[nei] = []
                        neighbours[nei].append(hidden_bin)

                        counter += 1

                    perms = list(map("".join, permutations('123456789', counter)))
                    domain[hidden_bin] = [perm for perm in perms if sum(int(x) for x in perm) == matrix[i][j][1]]
    return (neighbours, domain, variables)

#compute the constraint matrix and a map to get the indices
def constraint(neighbour, variable, size):
    constraint = []
    m = []
    for i in range(size):
        for j in range(len(variables) - size):
            m.append(0)
        constraint.append(m)
        m = []

    key_map = {}
    i = 0
    j = 0
    for key in neighbour:
        if 'X' in key:
            key_map[key] = i
            i += 1
        elif 'C' in key:
            key_map[key] = j
            j += 1
    for variable in variables:
        if "X" in variable:
            for loc in neighbour[variable]:
                constraint[key_map[variable]][key_map[loc]] = 1
     
    return (constraint, key_map)

'''
function to find all the binary arcs and to add them to a list
'''
def all_arcs(domain, constraint, key_map):
    queue = set()
    for i in key_map:
        for j in key_map:
            if "X" in i and "C" in j:
                if constraint[key_map[i]][key_map[j]] == 1:
                    queue.add((j, i))
                    queue.add((i, j))
    return queue

'''
revise function 
deletes an inconsistent entry in the domain
'''
def revise(domain, var, neighbours):
    v1, v2 = var
    revised = False
    if "X" in v1 and "C" in v2:
        cpy = domain[v1].copy()
        for dom in cpy:
            nei = [n for n in neighbours[v2]]
            index = nei.index(v1)
            lst = []
            for d in domain[v2]:
                lst.append(d[index])
            if dom not in lst:
                domain[v1].remove(dom)
                revised = True
    elif "C" in v1 and "X" in v2:
        cpy = domain[v1].copy()
        for dom in cpy:
            nei = [n for n in neighbours[v1]]
            index = nei.index(v2)
            if dom[index] not in domain[v2]:
                domain[v1].remove(dom)
                revised = True
    return revised

'''
checks all arcs and appends new arcs into the list
'''
def AC3(domains, constraints, key_map, neighbours):
    arcs = list(all_arcs(domains, constraints, key_map))
    pending_arcs = set(arcs)
    while pending_arcs:
        x, y = pending_arcs.pop()
        if revise(domains, (x, y), neighbours):
            if len(domains[x]) == 0:
                return False
            pending_arcs = pending_arcs.union((x2, y2) for x2, y2 in arcs if y2 == x)
    return True


def AC3_2(domains, constraints, key_map, neighbours):
    arcs = list(all_arcs(domains, constraints, key_map))
    pending_arcs = set(arcs)
    while pending_arcs:
        x, y = pending_arcs.pop()
        if revise(domains, (x, y), neighbours):
            if len(domains[x]) == 0:
                return False
            pending_arcs = pending_arcs.union((x2, y2) for x2, y2 in arcs if y2 == x)
    return True

def AC3_(domains, constraints, key_map, neighbours, removals, var, val):
    # arcs = list(all_arcs(domains, constraints, key_map))
    arcs = set()
    for i in key_map:
        for j in key_map:
            if "X" in i and var == j and "C" in var:
                if constraint[key_map[i]][key_map[j]] == 1:
                    arcs.add((i, j))
    pending_arcs = arcs
    while pending_arcs:
        x, y = pending_arcs.pop()
        if revise(domains, (x, y), neighbours):
            if len(domains[x]) == 0:
                return False
            pending_arcs = pending_arcs.union((x2, y2) for x2, y2 in arcs if y2 == x)
    return True

def MAC(domains, constraints, key_map, neighbours, var, val, assignment, removals):
    return AC3_(domains, constraints, key_map, neighbours, removals, var, val) 

#counts the number of conflicts
def count(seq):
    return sum(map(bool, seq))

#returns the number of conflicts
def conflicts(var, val, assignment, neighbours):
    def conflict(var2):
        return var2 in assignment and not kakuro_constraint(var, val, var2, assignment[var2])
    # count = 0
    # for v in neighbours[var]:
    #     if conflict(v) == True:
    #         count += 1
    # return count
    return count(conflict(v) for v in neighbours[var])


# def backtracking(assignment, domains, constraints, key_map, neighbours, original_variables):
#     rem = original_variables.copy()
#     return rec_backtracking(assignment, domains, constraints, key_map, neighbours, original_variables, rem)

# def rec_backtracking(assignment, domains, constraints, key_map, neighbours, original_variables, rem):
#     #print(len(assignment))
#     if len(assignment) == len(original_variables):
#         return assignment
#     var = rem.pop()
#     #print(var)
#     for val in domains[var]:
#         #print(conflicts(var, val, assignment, neighbours))
#         if conflicts(var, val, assignment, neighbours) == 0:
#             assignment[var] = val
#             #print(assignment)
#             result = rec_backtracking(assignment, domains, constraints, key_map, neighbours, original_variables, rem)
#             if result != {}:
#                 return result
#             assignment.pop(var)

#         # if nei in assignment.keys():
#         #         if kakuro_constraint(var, val, nei, assignment[nei]) == True:
#         #             assignment[var] = val
#         #             result = rec_backtracking(assignment, domains, constraints, key_map, neighbours, original_variables, rem)
#         #             if result is not None:
#         #                 return result
#         #             assignment.pop(var)
#     return {}    

#BS with MAC
def BS_MAC(assignment, original_variables, constraints, key_map, neighbours, domains, rem):

    def backtrack(assignment, original_variables, constraints, key_map, neighbours, domains, rem):
        if len(assignment) == len(original_variables):
            return assignment
        var = rem.pop()
        copy = domains.copy()
        for value in domains[var]:
            if 0 == conflicts(var, value, assignment, neighbours):
                assignment[var] = value
                removals = [(var, a) for a in domains[var] if a != value]
                domains[var] = value
                if MAC(domains, constraints, key_map, neighbours, var, value, assignment, removals):
                    result = backtrack(assignment, original_variables, constraints, key_map, neighbours, domains, rem)
                    if result is not None:
                        return result
                for B, b in removals:
                    domains[B].append(b)
        for var in assignment:
            del assignment[var]
            domains = copy

        return None

    result = backtrack({}, original_variables, constraints, key_map, neighbours, domains, rem)
    return result

#Backtracking search
def BS(assignment, original_variables, variables, rem, domain, key_map, count_BS):
    count_BS[0] += 1
    if len(assignment) == len(variables) - len(original_variables):
        return True
    var = rem.pop()

    for val in domain[var]:
        as_list = assignment[len(assignment) - 1].copy()
        nei = neighbours[var]

        flag = 0
        for n in nei:
            index = nei.index(n)
            if val[index] == as_list[n] or as_list[n] == 0:
                flag += 1
        if flag == len(val):
            for n in nei:
                index = nei.index(n)
                as_list[n] = val[index]
            assignment.append(as_list)

            result = BS(assignment, original_variables, variables, rem, domain, key_map, count_BS)
            if result != False:
                return result
            assignment.pop()
    return False

#function to print the file
def file_print(input_file, row, col, assignment):
    current_dir = os.getcwd()
    final_dir = os.path.join(current_dir, r'evaluation')
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    string = input_file.replace("input", "")
    output_file = string[0] + ".txt"
    dict_ = assignment.pop()
    with open(os.path.join(final_dir, "output_%s.txt" %(string[0])), "w") as f:
        with open(input_file, 'r') as file:
            for line in file:
                if "row" in line:
                    f.write(line)
                elif "column" in line:
                    f.write(line)
                elif "Horizontal" in line:
                    f.write(line)
                    break
        for i in range(row):
            for j in range(col):
                if matrix[i][j] == "#":
                    f.write("#")
                elif matrix[i][j] == 0:
                    f.write(str(dict_["X" + str(i) + "," + str(j)]))
                elif matrix[i][j][0] == "" and matrix[i][j][1] != "":
                    f.write(str(matrix[i][j][1]))
                else:
                    f.write("#")

                if j == col - 1:
                    f.write("\n")
                else:
                    f.write(",")

        f.write("Vertical\n")

        for i in range(row):
            for j in range(col):
                if matrix[i][j] == "#":
                    f.write("#")
                elif matrix[i][j] == 0:
                    f.write(dict_["X" + str(i) + "," + str(j)])
                elif matrix[i][j][0] != "" and matrix[i][j][1] == "":
                    f.write(str(matrix[i][j][0]))
                else:
                    f.write("#")

                if j == col - 1:
                    f.write("\n")
                else:
                    f.write(",")


if __name__ == '__main__':
    horizontal, vertical, row, column = read_file(sys.argv[1])
    input_data = (horizontal, vertical, row, column)
    
    
    matrix = matrix_superimpose(input_data)
    neighbours, domain, variables = neighbours(matrix, row, column)
    original_var_size = 0
    for var in variables:
        if "X" in var:
            original_var_size += 1

    original_variables = []
    for var in variables:
        if "X" in var:
            original_variables.append(var)
    constraint, key_map = constraint(neighbours, variables, original_var_size)
    # # start_time = time()
    # # tracemalloc.start()
    # # AC3(domain, constraint, key_map, neighbours)
    # assignment = []
    # # dict_ = {}
    # # for var in variables:
    # #     if "X" in var:
    # #         dict_[var] = 0
    # rem = [var for var in variables if "X" in var]
    # # assignment.append(dict_)
    # # count_BS = [0]
    # # BS(assignment, original_variables, variables, rem, domain, key_map, count_BS)
    # # end_time = time()
    # # print(tracemalloc.get_traced_memory())
    # # print(end_time - start_time)
    # # tracemalloc.stop()
    # assignment = {}
    # BS_MAC(assignment, original_variables, constraint, key_map, neighbours, domain, rem)
    # print(assignment)
    # #print(neighbours)
    # #print("\n")
    # #print(variables)
    # #print("\n")
    # #print(constraint)
    # # print(matrix)
    # # print("\n")
    # # print(domain)
    # # print("\n")
    # # print(assignment.pop())
    # # print("\n")
    # # print(count_BS)

    if sys.argv[2] == "BS":
        AC3(domain, constraint, key_map, neighbours)
        assignment = []
        dict_ = {}
        for var in variables:
            if "X" in var:
                dict_[var] = 0
        rem = [var for var in variables if "C" in var]
        assignment.append(dict_)
        count_BS = [0]
        BS(assignment, original_variables, variables, rem, domain, key_map, count_BS)
    elif sys.argv[2] == "AC3":
        AC3(domain, constraint, key_map, neighbours)
    elif sys.argc[2] == "BS_MAC":
        BS_MAC(assignment, original_variables, constraint, key_map, neighbours, domain)

    if sys.argv[2] != "AC3":
        file_print(sys.argv[1], row, column, assignment)
