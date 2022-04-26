#!/usr/bin/env python3


import sys
import queue


class Edge:
    def __init__(self, dest_from, dest_to, cost):
        self.dest_from = dest_from
        self.dest_to = dest_to
        self.cost = cost

    def __str__(self):
        ret = str(self.dest_from) + " -> " + str(self.dest_to) + " cost: " + str(self.cost)
        # ret = str(self.dest_from) + " " + str(self.dest_to)
        return ret

    def __lt__(self, other):
        return self.cost < other.cost


class Node:
    def __init__(self, name, cost=10000, terminal=False, parent=None, edge_to_parent=None):
        self.name = name
        self.cost = cost
        self.is_terminal = terminal
        self.neighbour_edges = []
        self.parent = parent
        self.edge_to_parent = edge_to_parent
        self.visited = False
        self.in_q = False

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        ret = ""
        ret += str(self.name) + "\n"
        for e in self.neighbour_edges:
            ret += str(e) + "\n"
        return ret


if __name__ == '__main__':
    with open(sys.argv[1], "r") as input_file:
        inp = input_file.readline().split()
        number_of_nodes, number_of_edges = int(inp[0]), int(inp[1])
        distance_matrix = [[sys.maxsize for j in range(number_of_nodes)] for i in range(number_of_nodes)]
        nodes = [Node(i) for i in range(number_of_nodes)]
        for i in range(number_of_edges):
            inp = input_file.readline().split()
            f = int(inp[0])
            t = int(inp[1])
            c = int(inp[2])

            distance_matrix[f][t] = c
            distance_matrix[t][f] = c
            e = Edge(f, t, c)
            nodes[f].neighbour_edges.append(e)
            e = Edge(t, f, c)
            nodes[t].neighbour_edges.append(e)
        for i in input_file.readline().split():
            nodes[int(i)].is_terminal = True
        number_of_terminals = sum(nodes[i].is_terminal for i in range(number_of_nodes))

    print("DISTANCE MATRIX")
    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            print(distance_matrix[i][j], end=" ")
        print()
    print("-----------------")
    print("NODES")
    for nod in nodes:
        print(nod)
    print("-----------------")
    blob = -1
    for nod in nodes:
        if nod.is_terminal:
            blob = nod
            break
    my_set = {blob}
    new_tree = []
    q = queue.PriorityQueue()
    q.put(blob)
    # new_tree.append(blob)
    used_edges = []
    used_nodes = []
    total_cost = 0
    while len(my_set) != number_of_terminals:
        if q.empty():
            print("Fokin error ")
            break
        current_node = q.get()
        used_nodes.append(current_node)
        current_node.visited = True
        current_node.in_q = False
        if current_node.is_terminal:
            my_set.add(current_node)
            current_node.cost = 0
            # if current_node.edge_to_parent is not None:
            #     total_cost += current_node.edge_to_parent.cost
            #     used_edges.append(current_node.edge_to_parent)
            i = current_node.parent
            # new_tree.clear()
            new_tree.append(current_node)
            if i is not None:
                total_cost += current_node.edge_to_parent.cost
                used_edges.append(current_node.edge_to_parent)
                while i.cost != 0:
                    new_tree.append(i)
                    if i.cost != 0:
                        used_edges.append(i.edge_to_parent)
                        total_cost += current_node.edge_to_parent.cost
                    i.cost = 0
                    i = i.parent
            while not q.empty():
                blob = q.get()
                blob.in_q = False
                blob.visited = False
            for i in new_tree:
                for e in i.neighbour_edges:
                    if (nodes[e.dest_to].cost != 0 and not nodes[e.dest_to].in_q) or nodes[e.dest_to].cost > e.cost :
                        nodes[e.dest_to].cost = e.cost
                        nodes[e.dest_to].visited = False
                        nodes[e.dest_to].parent = i
                        nodes[e.dest_to].edge_to_parent = e
                        if not nodes[e.dest_to].in_q:
                            nodes[e.dest_to].in_q = True
                            q.put(nodes[e.dest_to])
            continue
        for e in current_node.neighbour_edges:
            if (not nodes[e.dest_to].visited and not nodes[e.dest_to].in_q) or nodes[e.dest_to].cost > current_node.cost + e.cost:
                nodes[e.dest_to].cost = current_node.cost + e.cost
                nodes[e.dest_to].parent = current_node
                nodes[e.dest_to].edge_to_parent = e
                # used_edges.append(e)
                if not nodes[e.dest_to].in_q:
                    nodes[e.dest_to].in_q = True
                    q.put(nodes[e.dest_to])
    # print("SET:  -------------")
    # for i in my_set:
    #     print(i)
    # print("EDGES:    -------------")
    # for i in used_edges:
    #     print(i)
    # print("-------------")
    # for i in new_tree:
    #     print(i)
    # print("-------------")
    # for i in new_tree:
    #     print(i.edge_to_parent)

    total_cost = 0

    for e in used_edges:
        total_cost += e.cost

    print(total_cost)
    for i in used_edges:
        print(i)


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
