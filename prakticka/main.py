#!/usr/bin/env python3

import gurobipy as g
import sys

model = g.Model()

n = 9

if __name__ == '__main__':
    A = []
    prefiled_numbers = []
    with open(sys.argv[1], "r") as input_file:
        for i in range(n):
            line = input_file.readline()
            for j in range(n):
                if line[j] != '.':
                    if line[j] == 'A':
                        A.append((i+1, j+1))
                    elif line[j].isdigit():
                        prefiled_numbers.append((i+1, j+1, int(line[j])))

    print(A)
    print(prefiled_numbers)

    x = model.addVars(n+2, n+2, vtype=g.GRB.INTEGER, lb=0, ub=8)

    model.addConstr(x.sum(0,"*") + x.sum(n+1, "*") + x.sum("*", n+1) + x.sum("*", 0) == 0)

    y = model.addVars(n+2, n+2, vtype=g.GRB.BINARY)

    for i, j, val in prefiled_numbers:
        model.addConstr(x[i, j] == val)

    M = 1000

    for i in range (1, n+1):
        # row = []
        # for j in range (1, n+1):
        #     row.append(x[i, j])
        # model.addConstrs(row.count(j) == 1 for j in range (0, 9))
        # model.addConstr()
        # model.addConstr()

        # model.addConstr(x.sum(i, "*") == 36)
        # model.addConstr(x.sum("*", i) == 36)
        for j in range(1, n+1):
            for k in range(j, n+1):
                b = model.addVar(vtype=g.GRB.BINARY)
                model.addConstr((x[i, j]-x[i, k]) * b >= 1)
                model.addConstr((x[i, j]-x[i, k]) * b <= 1)
        # for i in range (0, 9):
        # model.addConstr((x.sum(x, y) == 36 for x in range(i*3+1, i*3+1+3)) for y in range(i*3+1, i*3+1+3))

    # for i in range (1, n+1):
    #     x[i, j].keys().count(i)
    #     model.addConstr( == 1 for i in range(0, 9))


    diag_sum = 0

    for i in range (n+1):
        for j in range (n+1):
            diag_sum += x[i, j]

    model.setObjective(diag_sum, g.GRB.MAXIMIZE)

    model.optimize()

    # optimum = g.quicksum(x).getValue()

    ret = []

    for i in range(1, n+1):
        for j in range(1, n+1):
            print(x[i, j].X, end=" ")
        print()


    # with open(sys.argv[2], "w+") as output_file:
    #     output_file.write(str(optimum)+'\n')
    #     for i in ret:
    #         output_file.write(i+'\n')
