#!/usr/bin/env python3

import gurobipy as g
import sys


if __name__ == "__main__":
    d = []
    with open(sys.argv[1], "r") as input_file:
        inpt = input_file.read()
        for i in inpt.split():
            d.append(int(i))

    print(d)

    m = g.Model()

    x = m.addVars(24, vtype=g.GRB.INTEGER)
    z = m.addVars(24, vtype=g.GRB.INTEGER)

    small_sum = []

    for i in range(24):
        blob = 0
        for j in range(i-7, i+1):
            blob += x[j % 24]
        small_sum.append(blob)
        # z.append(d[i]-small_sum[i])

    for i in range(24):
        m.addConstr(small_sum[i]-d[i] <= z[i])
        m.addConstr(d[i]-small_sum[i] <= z[i])
        m.addConstr(z[i] >= 0)

    m.setObjective(g.quicksum(z), g.GRB.MINIMIZE)

    m.optimize()
    print()

    with open(sys.argv[2], "w+") as output_file:
        output_file.write(str(int(m.objVal)) + "\n")
        for i in range(24):
            output_file.write(str(int(x[i].x)) + " ")
        output_file.write("\n")

    print()