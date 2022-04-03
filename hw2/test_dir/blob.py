#!/usr/bin/env python3

import sys
import gurobipy as g
import numpy as np


def print_matrix(matrix, w, h):
    for i in range(h):
        for j in range(w):
            print(matrix[i][j][0], ".", matrix[i][j][1], ".", matrix[i][j][2], end=' | ')
        print()

def calculate_distance(left, right, h, w):
    # print("l:")
    # print(left)
    # print("r:")
    # print(right)
    ret = 0
    if left == right: return 0
    for i in range(h):
        for j in range(3):
            ret += abs(left[i][w-1][j] - right[i][0][j])
    return ret

def load_data_from_file():
    d = []
    # print("1")
    with open(sys.argv[1], "r") as input_file:
        # print("2")
        n, w, h = filter(None, input_file.readline().split())
#        print(input_file.read().split())
        n = int(n)
        w = int(w)
        h = int(h)

        #matrixes = [[] for i in range(n)]
        matrixes = []
        for i in range(n):
            # print("3")
            line = input_file.readline().split()
            #print(line)
            matrix = []
            for k in range(h):
                row = []
                for j in range(k*w, k*w+w):
                    pixel = []
                    pixel.append(int(line[j*3]))
                    pixel.append(int(line[j*3+1]))
                    pixel.append(int(line[j*3+2]))
                    row.append(pixel)
                matrix.append(row)
            matrixes.append(matrix)
    # print(matrixes)
    # for i in matrixes:
    #     print_matrix(i, w, h)
    #     print('--------')

    dist_matrix = np.array([ [0 for i in range(n+1)] for i in range(n+1)])

    # print(dist_matrix)

    for i in range(n):
        for j in range(n):
            if i == n/2 and j == n/2 +1:
                print("l:")
                print(matrixes[i])
                print("r:")
                print(matrixes[j])
            dist_matrix[i][j] = calculate_distance(matrixes[i], matrixes[j], h, w)
    print(dist_matrix)
    # for i in range(len(dist_matrix)):
    #     for j in range(len(dist_matrix[i])):
    #         print(dist_matrix[i][j], end=".")
    #     print()
    return dist_matrix


def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        number_of_visited_nodes = 0
        line = 0
        myset = set()
        cycle_found = False
        #matrix = model.cbGetSolution(x)
        while number_of_visited_nodes < n and not cycle_found:
            for j in range(n):
                if model.cbGetSolution(x[line][j]) == 1:
                    number_of_visited_nodes += 1
                    line = j
                    if j in myset:
                        cycle_found = True
                    myset.add(j)
                    break
        if number_of_visited_nodes < n:
            model.cbLazy(g.quicksum(x[i][j] for i in myset for j in myset if i != j) <= len(myset)-1)

        #value = model.cbGetSolution()

model = g.Model()
model.Params.lazyConstraints = 1

if __name__ == '__main__':
    dist_matrix = load_data_from_file()
    print(dist_matrix)
    n = len(dist_matrix)

    x = ([[0 for i in range(n)] for j in range(n)])
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i][j] = model.addVar(vtype=g.GRB.BINARY)
            else:
                x[i][j] = model.addVar(vtype=g.GRB.BINARY, lb=0, ub=0)
#            x[i][j] = 14#model.addVar(vtype=g.GRB.BINARY)

    for i in range(n):
        model.addConstr(g.quicksum(x[i][j] for j in range(n)) == 1)
        model.addConstr(g.quicksum(x[j][i] for j in range(n)) == 1)


    #x = np.zeros((n, n))

    # x = model.addVars(n, n, vtype=g.GRB.BINARY)
    #
    # for i in range(n):
    #     model.addConstr(g.quicksum(x[i, j] for j in range(n)) == 1)
    #     model.addConstr(g.quicksum(x[j, i] for j in range(n)) == 1)



    # for i in range(n+1):
    #     model.addConstr(g.quicksum(x[]))
    # print("-------")
    # print(x)
    # print("-------")
    # x = list(x)


    # x1 = np.array(x)

    # optim = np.sum(np.matmul(x1, dist_matrix))
    optim = 0
    for i in range(n):
        for j in range(n):
            optim += x[i][j] * dist_matrix[i][j]
    model.setObjective(optim, g.GRB.MINIMIZE)

    model.optimize(my_callback)

    # for i in range(n):
    #     for j in range(n):
    #         print(x[i][j].x, end=" ")
    #     print()
    #
    #  print(str(int(model.objVal)))

    number_of_visited_nodes = 0

    line = n-1
    ret = ""
    while number_of_visited_nodes < n-1:
        for j in range(n):
            # print("====", line, j, x[line][j].x)
            if x[line][j].x == 1:
                number_of_visited_nodes += 1
                line = j
                ret += str(j+1) + " "
                break
    print()
    print(dist_matrix)
    print()
    for i in range(n):
        for j in range(n):
            print(x[j][i].x, end=" ")
        print()
    print()
    # for i in range(n):
    #     for j in range(n):
    #         print(x[i][j].x, end=" ")
    #     print()
    print(ret)

    with open(sys.argv[2], "w+") as output_file:
        output_file.write(ret)











