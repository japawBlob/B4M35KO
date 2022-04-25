#!/usr/bin/env python3

import gurobipy as g
import sys
import queue

#  model.cbGetSolution(x[current_node][j])


def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        x = model.cbGetSolution(used_edges)
        my_terminal = -1
        visited = [False for i in range(number_of_nodes)]
        for terminal in range(number_of_nodes):
            parent = [-1 for i in range(number_of_nodes)]
            if nodes[terminal] == 1 and not visited[terminal]:
                visited[terminal] = True
                my_terminal = terminal
                my_set = {my_terminal}
                local_queue = queue.Queue()
                q = queue.PriorityQueue()
                local_queue.put(my_terminal)
                while not local_queue.empty():
                    current_node = local_queue.get()
                    for i in range(number_of_nodes):
                        if visited[i]:
                            continue
                        if x[current_node, i] == 1:
                            visited[i] = True
                            local_queue.put(i)
                            parent[i] = current_node
                            my_set.add(i)
                        elif x[i, current_node] == 1:
                            visited[i] = True
                            local_queue.put(i)
                            parent[i] = current_node
                            my_set.add(i)
                        elif distance_matrix[current_node][i] is not sys.maxsize:
                            parent[i] = current_node
                            q.put((distance_matrix[current_node][i], i))
                terminal_count = g.quicksum(nodes[i] for i in my_set)
                if terminal_count is not number_of_terminals:
                    while not q.empty():
                        solution_found = False
                        cost, current_node = q.get()
                        visited[current_node] = True
                        if nodes[current_node] == 1:
                            model.cbLazy(used_edges[current_node, parent[current_node]] == 1)
                            solution_found = True
                            break
                        for i in range(number_of_nodes):
                            if distance_matrix[current_node][i] == sys.maxsize:
                                continue
                            if not visited[i]:
                                if nodes[i] == 1:
                                    # add path to constrains and beak to outer cycle
                                    parent[i] = current_node
                                    current_parent = parent[i]
                                    while nodes[current_parent] != 1:
                                        model.cbLazy(used_edges[current_parent, i] == 1)
                                        i = current_parent
                                        current_parent = parent[i]
                                    model.cbLazy(used_edges[current_parent, i] == 1)
                                    solution_found = True
                                    break
                                else:
                                    parent[i] = current_node
                                    q.put((distance_matrix[current_node][i]+cost, i))
                        if solution_found:
                            break
                else:
                    return
            # break
        if my_terminal == -1:
            print("some error happened")
            return


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
    m.Params.lazyConstraints = 1
    used_nodes = m.addVars(number_of_nodes, vtype=g.GRB.BINARY)
    used_edges = m.addVars(number_of_nodes, number_of_nodes, vtype=g.GRB.BINARY)

    # include all terminal nodes
    m.addConstr(g.quicksum(used_nodes[i] * nodes[i] for i in range(number_of_nodes)) == number_of_terminals)

    # all used nodes need to be connected
    for i in range(number_of_nodes):
        line = g.quicksum(used_nodes[i]*used_edges[i, j] for j in range(number_of_nodes))
        column = g.quicksum(used_nodes[i]*used_edges[j, i] for j in range(number_of_nodes))
        m.addConstr(line + column >= 1*nodes[i])

    # minimize cost of spanning tree
    m.setObjective(g.quicksum(used_edges[i, j] * distance_matrix[i][j] for i in range(number_of_nodes) for j in range (number_of_nodes)), g.GRB.MINIMIZE)

    m.optimize(my_callback)

    print(str(m.objVal))

    for i in range(number_of_nodes):
        print(int(used_nodes[i].x), end=" ")
    print()

    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            print(used_edges[i, j].x, end=" ")
        print()

    print(int(m.objVal))
    for i in range (number_of_nodes):
        for j in range (number_of_nodes):
            if ( int(used_edges[i ,j].x) == 1 ):
                print(i, j)

    #
    #
    # number_of_edges = g.Model()
    #
    # with open(sys.argv[2], "w+") as output_file:
    #     output_file.write(str(int(number_of_edges.objVal)) + "\n")
    #     for i in range(24):
    #         output_file.write(str(int(x[i].x)) + " ")
    #     output_file.write("\n")
