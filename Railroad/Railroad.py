import heapq
from math import pi, acos, sin, cos
import pickle
import time
from tkinter import *

SCALE = 7
SHIFT_X = 950
SHIFT_Y = 500
MASTER = Tk()
W = Canvas(MASTER, width=600, height=500, bg="black")
W.pack()


# ----------------classes--------------------- #
class Graph:
    def __init__(self, graph):
        self.data = graph

    def get_neighbors(self, v):
        return self.data[v].keys()

    def get_edge_length(self, v1, v2):
        return self.data[v1][v2]


class Node:
    def __init__(self, state, parent, edge_length=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.edge_length = edge_length
        self.g = edge_length
        if self.parent is not None:
            self.g += parent.g


# ----------------make graph----------------------- #
def make_graph(node_file, edges_file, cities_file):
    graph = {}
    lat = {}
    long = {}
    city2node = {}

    file = open(node_file, "r")
    for line in file:
        t = line.split(" ")
        p = t[0].strip()
        graph[p] = {}
        lat[p] = float(t[1].strip())
        long[p] = float(t[2].strip())

    file = open(edges_file, "r")
    for line in file:
        t = line.split(" ")
        p1 = t[0].strip()
        p2 = t[1].strip()
        dist = calc_dist(lat[p1], long[p1], lat[p2], long[p2])
        graph[p1][p2] = dist
        graph[p2][p1] = dist

    file = open(cities_file, "r")
    for line in file:
        t = line.split(" ")
        city = t[1].strip()
        node = t[0].strip()
        if len(t) > 2:
            city += " " + t[2].strip()
        city2node[city] = node

    g = Graph(graph)

    pickle.dump(g, open("graph", "wb"))
    pickle.dump(lat, open("lat", "wb"))
    pickle.dump(long, open("long", "wb"))
    pickle.dump(city2node, open("city2node", "wb"))


# -------------------A*--------------------------- #
GRAPH = pickle.load(open("graph", "rb"))
CITY2NODE = pickle.load(open("city2node", "rb"))
LAT = pickle.load(open("lat", "rb"))
LONG = pickle.load(open("long", "rb"))

def a_star(start_city, goal_city, animate=False):
    goal_state = CITY2NODE[goal_city]
    goal_lat = LAT[goal_state]
    goal_long = LONG[goal_state]
    root = Node(CITY2NODE[start_city], None)
    fringe = []
    closed = set()
    heapq.heappush(fringe, (calc_dist(LAT[root.state], LONG[root.state], LAT[goal_state], LONG[goal_state]), root))
    while fringe:
        (f, p) = heapq.heappop(fringe)
        if animate:
            y = SHIFT_Y - SCALE * LAT[p.state]
            x = LONG[p.state] * SCALE + SHIFT_X
            W.create_line(x - 0.5, y - 0.5, x + 0.5, y + 0.5, fill="magenta")
        if p.state == goal_state:
            return p
        if p.state not in closed:
            closed.add(p.state)
            for c in GRAPH.get_neighbors(p.state):
                n = Node(c, p, GRAPH.get_edge_length(c, p.state))
                p.children += [n]
                heapq.heappush(fringe, (n.g + calc_dist(LAT[c], LONG[c], LAT[goal_state], LONG[goal_state]), n))
                if animate:
                    y = SHIFT_Y - SCALE * LAT[c]
                    x = LONG[c] * SCALE + SHIFT_X
                    W.create_line(x - 0.5, y - 0.5, x + 0.5, y + 0.5, fill="cyan")
        if animate:
            MASTER.update()
    return None


def calc_dist(y1, x1, y2, x2):
    # y1 = float(y1)
    # x1 = float(x1)
    # y2 = float(y2)
    # x2 = float(x2)
    r = 3958.76  # miles
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * r  # approx great circle dist with law of cos


# -------------------display------------------------- #
def draw_graph():
    for n1 in GRAPH.data:
        for n2 in GRAPH.get_neighbors(n1):
            y1 = SHIFT_Y - SCALE * LAT[n1]
            x1 = LONG[n1] * SCALE + SHIFT_X
            y2 = SHIFT_Y - SCALE * LAT[n2]
            x2 = LONG[n2] * SCALE + SHIFT_X
            W.create_line(x1, y1, x2, y2, fill="white")


def display_path(node):
    while node.parent is not None:
        y1 = SHIFT_Y - SCALE * LAT[node.state]
        x1 = LONG[node.state] * SCALE + SHIFT_X
        y2 = SHIFT_Y - SCALE * LAT[node.parent.state]
        x2 = LONG[node.parent.state] * 7 + SHIFT_X
        W.create_line(x1, y1, x2, y2, fill="yellow")
        node = node.parent
    mainloop()


def main():
    # make_graph("rrNodes.txt", "rrEdges.txt", "rrNodeCity.txt")
    draw_graph()
    city1 = input("Enter start city: ")
    city2 = input("Enter goal city: ")
    start = time.time()
    node = a_star(city1, city2)
    end = time.time()
    print("Path Length: " + str(node.g))
    print("Execution time: %5.2f seconds" % (end - start))
    display_path(node)

if __name__ == "__main__":
    main()
