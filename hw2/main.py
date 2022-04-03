#!/usr/bin/env python3

import sys
import gurobipy as g
import numpy as np
import time


def print_matrix(matrix, w, h):
    for i in range(h):
        for j in range(w):
            print(matrix[i][j][0], ".", matrix[i][j][1], ".", matrix[i][j][2], end=' | ')
        print()

def calculate_distance(left, right, h, w):
    # print("l:")
    # print (left)
    # print("r:")
    # print (right)
    return np.sum(np.absolute(left - right))

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

        # print("a")
        # print(time.time() - start)
        # print("a")

        #matrixes = [[] for i in range(n)]
        matrixes = []
        for i in range(n):
            # print("3")
            line = input_file.readline().split()
            #print(line)
            append = False
            matrix = np.zeros((h*3, 2))
            for k in range(h):
                # row = []
                # for j in range(k*w, k*w+w):
                #     pixel = []
                #     pixel.append(int(line[j*3]))
                #     pixel.append(int(line[j*3+1]))
                #     pixel.append(int(line[j*3+2]))
                #     row.append(pixel)
                # matrix.append(row)
                # print(line)
                # print(matrix)
                # for j in range(k * w, k * w + w):
                for j in range(w):
                    if 0 == w-1:
                        matrix[k * 3][0] = int(line[k * w * 3 + j * 3])
                        matrix[k * 3 + 1][0] = int(line[k * w * 3 + j * 3 + 1])
                        matrix[k * 3 + 2][0] = int(line[k * w * 3 + j * 3 + 2])
                        matrix[k * 3][1] = matrix[k * 3][0]
                        matrix[k * 3 + 1][1] = matrix[k * 3 + 1][0]
                        matrix[k * 3 + 2][1] = matrix[k * 3 + 2][0]
                    elif j == 0 or j == w-1:
                        if j == w-1:
                            y = 1
                        else:
                            y = 0
                        matrix[k*3][y] = int(line[k*w*3+j*3])
                        matrix[k*3+1][y] = int(line[k*w*3+j*3 + 1])
                        matrix[k*3+2][y] = int(line[k*w*3+j*3 + 2])
                    else:
                        continue
            #print(matrix)
            #     pixel = []
            #     pixel.append(int(line[j*3]))
            #     pixel.append(int(line[j*3+1]))
            #     pixel.append(int(line[j*3+2]))
            #     row.append(pixel)
            matrixes.append(np.transpose(matrix))

        # print("b")
        # print(time.time() - start)
        # print("b")
        # for matrix in matrixes:
        #     print(matrix)
    # print(matrixes)
    # for i in matrixes:
    #     print_matrix(i, w, h)
    #     print('--------')

    #dist_matrix = np.array([ [0 for i in range(n+1)] for i in range(n+1)])
    dist_matrix = np.zeros((n+1, n+1))

    # print(dist_matrix)
    np.set_printoptions(threshold=sys.maxsize)
    for i in range(n):
        for j in range(n):
            if i != j :
                # if i == int(n/2) and j == int(n/2)+1:
                #     print("l:")
                #     print(matrixes[i][1])
                #     print("r:")
                #     print(matrixes[j][0])
                dist_matrix[i][j] = calculate_distance(matrixes[i][1], matrixes[j][0], h, w)
    #print(dist_matrix)
    # print("c")
    # print(time.time() - start)
    # print("c")
    # for i in range(len(dist_matrix)):
    #     for j in range(len(dist_matrix[i])):
    #         print(dist_matrix[i][j], end=".")
    #     print()
    return dist_matrix


def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        number_of_visited_nodes = 0
        #lazy_x = model.cbGetSolution(x)
        line = 0
        myset = set()
        visited = np.zeros(n)
        cycle_found = False
        cycles = []
        #matrix = model.cbGetSolution(x)
        # while number_of_visited_nodes < n:
        #     for j in range(n):
        #         if model.cbGetSolution(x[line][j]) == 1:
        #             number_of_visited_nodes += 1
        #             line = j
        #             if j in myset:
        #                 cycle_found = True
        #             myset.add(j)
        #             break
        for i in range(n):
            if visited[i] == 1:
                continue
            else:
                cycle = []
                current_node = i
                while visited[current_node] != 1:
                    visited[current_node] = 1
                    cycle.append(current_node)
                    for j in range(n):
                        if model.cbGetSolution(x[current_node][j]) == 1:
                            current_node = j
                            break
                cycles.append(cycle)
        # print(cycles)
        if len(cycles) > 1:
            max_len = np.inf
            cycle_to_block = None
            for c in cycles:
                if len(c) < max_len:
                    cycle_to_block = c
                    max_len = len(c)
            model.cbLazy(g.quicksum(x[i][j] for i in cycle_to_block for j in cycle_to_block if i != j) <= len(cycle_to_block)-1)

        #value = model.cbGetSolution()

model = g.Model()
model.Params.lazyConstraints = 1

if __name__ == '__main__':
    # start = time.time()
    # print("000000000000000000000")
    # print(time.time() - start)
    # print("00000000000000000000")
    dist_matrix = load_data_from_file()
    # print(dist_matrix)
    # print("1111111111111111111111111")
    # print(time.time()-start)
    # print("1111111111111111111111111")

    n = len(dist_matrix)
    # print("222222222222222222222222")
    # print(time.time()-start)
    # print("22222222222222222222222")
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
    # print("333333333333333333")
    # print(time.time() - start)
    # print("333333333333333333")

    model.optimize(my_callback)
    # print("44444444444444444")
    #
    # print(time.time() - start)
    # print("44444444444444444")

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
    # print()
    # for i in range(n):
    #     for j in range(n):
    #         print(x[j][i].x, end=" ")
    #     print()
    # print()
    # print()
    # print(dist_matrix)
    # print()
    # for i in range(n):
    #     for j in range(n):
    #         print(x[i][j].x, end=" ")
    #     print()
    # print(ret)

    with open(sys.argv[2], "w+") as output_file:
        output_file.write(ret)
    # print("55555555555555555555")
    #
    # print(time.time() - start)
    # print("55555555555555555555")








