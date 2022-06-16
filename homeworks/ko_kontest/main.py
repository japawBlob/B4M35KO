#!/usr/bin/env python3

import gurobipy as g
import sys


sol1 = "82\n6 28\n17 27\n42 17\n19 6\n19 26\n47 19\n20 11\n19 21\n21 20\n21 42\n26 33\n27 23\n28 32\n32 34\n35 48\n21 40\n40 35\n40 46\n46 36\n"
sol2 = "83\n34 6\n6 38\n26 8\n35 18\n24 46\n25 48\n26 28\n26 34\n27 42\n28 5\n34 40\n19 35\n36 39\n39 27\n42 26\n42 43\n43 10\n44 19\n44 25\n44 36\n46 44\n48 22\n"


if __name__ == '__main__':
    with open(sys.argv[1], "r") as input_file:
        inp = input_file.readline().split()
        number_of_nodes, number_of_edges = int(inp[0]), int(inp[1])
        distance_matrix = [[sys.maxsize for j in range(number_of_nodes)] for i in range(number_of_nodes)]
        nodes = [0 for i in range(number_of_nodes)]
        for i in range(number_of_edges):
            inp = input_file.readline().split()
            distance_matrix[int(inp[0])][int(inp[1])] = int(inp[2])
            distance_matrix[int(inp[1])][int(inp[0])] = int(inp[2])
        for i in input_file.readline().split():
            nodes[int(i)] = 1
        number_of_terminals = sum(nodes)
    blob = 0
    for i in range(number_of_nodes):
        if nodes[i] == 1:
            blob += i

    m = g.Model()
    used_edges = m.addVars(number_of_nodes, number_of_nodes, vtype=g.GRB.BINARY)
    edge_flow = m.addVars(number_of_nodes, number_of_nodes, vtype=g.GRB.INTEGER, lb=0, ub=number_of_terminals-1)

    initial_terminal = 0
    for i in range(number_of_nodes):
        if nodes[i] == 1 and initial_terminal == 5:
            for j in range(number_of_nodes):
                m.addConstr(edge_flow[i, j] == (number_of_terminals-1))
            initial_terminal += 1
        elif nodes[i] == 1:
            m.addConstr(g.quicksum(edge_flow[i, j] * used_edges[i, j] for j in range(number_of_nodes)) == g.quicksum(edge_flow[j, i] * used_edges[j, i] for j in range(number_of_nodes)) - 1)
            initial_terminal += 1
        else:
            m.addConstr(g.quicksum(edge_flow[i, j] * used_edges[i, j] for j in range(number_of_nodes)) == g.quicksum(edge_flow[j, i] * used_edges[j, i] for j in range(number_of_nodes)))

    m.setObjective(g.quicksum(used_edges[i, j] * distance_matrix[i][j] for i in range(number_of_nodes) for j in range(number_of_nodes)), g.GRB.MINIMIZE)

    m.optimize()

    print(int(m.objVal))
    for i in range (number_of_nodes):
        for j in range (number_of_nodes):
            if int(used_edges[i, j].x) == 1:
                print(i, j)

    with open(sys.argv[2], "w+") as output_file:
        output_file.write(str(int(m.objVal)) + "\n")
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if int(used_edges[i, j].x) == 1:
                    output_file.write(str(i) + " " + str(j) + "\n")
        output_file.write("\n")
