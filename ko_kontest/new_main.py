#!/usr/bin/env python3

import gurobipy as g
import sys
import queue


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

    print("DISTANCE MATRIX")
    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            print(distance_matrix[i][j], end=" ")
        print()
    print("-----------------")
    print("NODES")
    print(nodes)

    m = g.Model()
    used_edges = m.addVars(number_of_nodes, number_of_nodes, vtype=g.GRB.BINARY)

    # include all terminal nodes
    # m.addConstr(g.quicksum(used_nodes[i] * nodes[i] for i in range(number_of_nodes)) == number_of_terminals)

    # all used nodes need to be connected
    for i in range(number_of_nodes):
        line = g.quicksum(nodes[i]*used_edges[i, j] for j in range(number_of_nodes))
        column = g.quicksum(nodes[i]*used_edges[j, i] for j in range(number_of_nodes))
        m.addConstr(line + column >= 1*nodes[i])

    # minimize cost of spanning tree
    m.setObjective(g.quicksum(used_edges[i, j] * distance_matrix[i][j] for i in range(number_of_nodes) for j in range (number_of_nodes)), g.GRB.MINIMIZE)

    m.optimize()

    print(str(m.objVal))

    for i in range(number_of_nodes):
        print(int(nodes[i]), end=" ")
    print()

    # used_matrix = [[0 for i in range(number_of_nodes)] for j in range(number_of_nodes)]
    #
    # sol = int(m.objVal)
    # for i in range(number_of_nodes):
    #     for j in range(number_of_nodes):
    #         if int(used_edges[i, j].x) == 1 and int(used_edges[j, i].x) == 1:
    #             used_matrix[i][j] = 1
    #             sol -= 1
    #         else:
    #             used_matrix[i][j] = int(used_edges[i, j].x)



    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            print(used_edges[i, j].x, end=" ")
        print()

    print(int(m.objVal))
    for i in range (number_of_nodes):
        for j in range (number_of_nodes):
            if ( int(used_edges[i ,j].x) == 1 ):
                print(i, j)

    # print(int(sol))
    # for i in range(number_of_nodes):
    #     for j in range(number_of_nodes):
    #         if used_matrix[i][j] == 1:
    #             print(i, j)

    #
    #
    # number_of_edges = g.Model()
    #
    # with open(sys.argv[2], "w+") as output_file:
    #     output_file.write(str(int(number_of_edges.objVal)) + "\n")
    #     for i in range(24):
    #         output_file.write(str(int(x[i].x)) + " ")
    #     output_file.write("\n")
