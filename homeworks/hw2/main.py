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
    return np.sum(np.absolute(left - right))


def load_data_from_file():
    with open(sys.argv[1], "r") as input_file:
        n, w, h = filter(None, input_file.readline().split())
        n = int(n)
        w = int(w)
        h = int(h)

        matrixes = []
        for i in range(n):
            line = input_file.readline().split()
            matrix = np.zeros((h*3, 2))
            for k in range(h):
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
            matrixes.append(np.transpose(matrix))
    dist_matrix = np.zeros((n+1, n+1))
    np.set_printoptions(threshold=sys.maxsize)
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = calculate_distance(matrixes[i][1], matrixes[j][0], h, w)
    return dist_matrix


def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        visited = np.zeros(n)
        cycles = []
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
        if len(cycles) > 1:
            max_len = np.inf
            cycle_to_block = None
            for c in cycles:
                if len(c) < max_len:
                    cycle_to_block = c
                    max_len = len(c)
            model.cbLazy(g.quicksum(x[i][j] for i in cycle_to_block for j in cycle_to_block if i != j) <= len(cycle_to_block)-1)


if __name__ == '__main__':
    model = g.Model()
    model.Params.lazyConstraints = 1

    dist_matrix = load_data_from_file()

    n = len(dist_matrix)
    x = ([[0 for i in range(n)] for j in range(n)])
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i][j] = model.addVar(vtype=g.GRB.BINARY)
            else:
                x[i][j] = model.addVar(vtype=g.GRB.BINARY, lb=0, ub=0)

    for i in range(n):
        model.addConstr(g.quicksum(x[i][j] for j in range(n)) == 1)
        model.addConstr(g.quicksum(x[j][i] for j in range(n)) == 1)

    optim = 0
    for i in range(n):
        for j in range(n):
            optim += x[i][j] * dist_matrix[i][j]
    model.setObjective(optim, g.GRB.MINIMIZE)
    model.optimize(my_callback)

    number_of_visited_nodes = 0

    line = n-1
    ret = ""
    while number_of_visited_nodes < n-1:
        for j in range(n):
            if x[line][j].x == 1:
                number_of_visited_nodes += 1
                line = j
                ret += str(j+1) + " "
                break
    with open(sys.argv[2], "w+") as output_file:
        output_file.write(ret)
