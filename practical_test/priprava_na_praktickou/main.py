#!/usr/bin/env python3

import gurobipy as g
import sys


def coord_to_xy(coord):
    return ord(coord[0])-97+2, int(coord[1])-1+2


def xy_to_coord(x, y):
    return chr(x-2+97)+str(y-2+1)


rooks = []


def read_input():
    with open(sys.argv[1], "r") as input_file:
        number_of_rooks = int(input_file.readline())
        for i in range(number_of_rooks):
            rooks.append(coord_to_xy(input_file.readline()))


model = g.Model()
board_dimensions = 12

if __name__ == '__main__':
    read_input()
    print(rooks)

    occupied_tiles = model.addVars(board_dimensions, board_dimensions, vtype=g.GRB.BINARY)
    endangered_tiles = model.addVars(board_dimensions, board_dimensions, vtype=g.GRB.BINARY)

    for x, y in rooks:
        print(x, y)
        model.addConstr(occupied_tiles.sum(x, "*") + occupied_tiles.sum("*", y) == 0)

    for i in range(2, board_dimensions-2):
        for j in range(2, board_dimensions-2):
            model.addConstr(occupied_tiles[i, j] + endangered_tiles[i, j] <= 1)
            model.addConstr(occupied_tiles[i, j] * (endangered_tiles[i+1, j+2] + endangered_tiles[i+2, j+1] +
                                                    endangered_tiles[i-1, j+2] + endangered_tiles[i-2, j+1] +
                                                    endangered_tiles[i+1, j-2] + endangered_tiles[i+2, j-1] +
                                                    endangered_tiles[i-1, j-2] + endangered_tiles[i-2, j-1]) == occupied_tiles[i, j] * 8)

    model.addConstr(occupied_tiles.sum(0,"*") + occupied_tiles.sum(1,"*") +
                    occupied_tiles.sum(board_dimensions-1,"*") + occupied_tiles.sum(board_dimensions-2,"*")
                    + occupied_tiles.sum("*",0) + occupied_tiles.sum("*",1) +
                    occupied_tiles.sum("*", board_dimensions-1) + occupied_tiles.sum("*", board_dimensions-2) == 0)

    model.setObjective(g.quicksum(occupied_tiles), g.GRB.MAXIMIZE)

    model.optimize()

    optimum = int(g.quicksum(occupied_tiles).getValue())
    ret = []
    for i in range (2, board_dimensions-2):
        for j in range (2, board_dimensions-2):
            print(occupied_tiles[i, j].X, end=" ")
            if occupied_tiles[i, j].X == 1:
                ret.append(xy_to_coord(i, j))
        print()

    print(ret)
    print(g.quicksum(occupied_tiles).getValue())

    print(occupied_tiles)

    with open(sys.argv[2], "w+") as output_file:
        output_file.write(str(optimum)+'\n')
        for i in ret:
            output_file.write(i+'\n')
