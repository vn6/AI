import heapq
from time import time
import random

possible_moves = ["DR", "DLR", "DLR", "DL",
                  "UDR", "UDLR", "UDLR", "UDL",
                  "UDR", "UDLR", "UDLR", "UDL",
                  "UR", "ULR", "ULR", "UL"]
SIZE = 4
BLANK = "A"
GOAL = "ABCDEFGHIJKLMNOP"
UP, DOWN, LEFT, RIGHT = "U", "D", "L", "R"
GOAL_INDEXES = {}
for n in range(SIZE ** 2):
    GOAL_INDEXES[GOAL[n]] = n

class Node:
    def __init__(self, state, parent, move="", manhattan=-1):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = 1
        if parent is not None:
            self.depth += parent.depth
        self.move = move
        self.manhattan = manhattan
        if manhattan == -1:
            self.manhattan = manhattan_total(state)
# end class


def greedy(root):
    fringe = []
    heapq.heappush(fringe, (h(root.state), root))
    visited = set([])
    visited.add(root.state)
    while fringe:
        (score, p) = heapq.heappop(fringe)
        if p.state == GOAL:
            return p
        index = p.state.find(BLANK)
        for d in possible_moves[index]:
            s, index2 = make_move(p.state, d, index)
            if s not in visited:
                visited.add(s)
                heuristic = h(s, p.manhattan, index2, index)
                n = Node(s, p, d, heuristic)
                p.children += [n]
                heapq.heappush(fringe, (heuristic + n.depth + random.random(), n))
    return None


def h(s, parent_heuristic, index1, index2):
    m1 = manhattan(s, index1)
    m2 = manhattan(s, index2)
    if m1 < m2:
        return parent_heuristic + 1
    return parent_heuristic - 1


def manhattan_total(s):
    total = 0
    for x in range(len(s)):
        if s[x] != BLANK:
            total += manhattan(s, x)
    return total


def manhattan(s, n):
    i1, j1 = n_ij(n)
    i2, j2 = n_ij(GOAL_INDEXES[s[n]])
    return abs(i1 - i2) + abs(j1 - j2)


def manhattan100000(s):
    start = time()
    for x in range(100000):
        manhattan_total(s)
    end = time()
    print("Execution time: %5.2f seconds" % (end - start))


def tile_count(s):
    count = 0
    for x in range(len(s)):
        if s[x] != GOAL[x]:
            count += 1
    return count


def print_steps(node):
    s = ""
    t = node
    while t is not None:
        s = "\n" + t.move + " " + t.state + s
        t = t.parent
    print(s)


def make_move(s, d, index):
    index2 = index
    if d == UP:
        index2 -= SIZE
    elif d == DOWN:
        index2 += SIZE
    elif d == LEFT:
        index2 -= 1
    elif d == RIGHT:
        index2 += 1

    return swap(s, index, index2), index2


def swap(s, n1, n2):
    t = list(s)
    t[n1], t[n2] = t[n2], t[n1]
    return "".join(t)


def n_ij(n):
    return n // SIZE, n % SIZE


def gen_start():
    s = GOAL
    for x in range(random.randint(100, 150)):
        index = s.index(BLANK)
        d = possible_moves[index]
        s = make_move(s, d[random.randint(0, len(d) - 1)], index)
    print("Puzzle: " + s)
    return s


def solve_input(string):
    start = time()
    n = greedy(Node(string.strip(), None))
    end = time()
    print("Path length: " + str(n.depth))
    print("Execution time: %5.2f seconds" % (end - start))
    # print_steps(n)


def solve_file(filename):
    file = open(filename, "r")
    for line in file:
        start = time()
        n = greedy(Node(line.strip(), None))
        end = time()
        if n is not None:
            print("Puzzle: " + line)
            print("Path length: " + str(n.depth))
            print("Execution time: %5.2f seconds" % (end - start) + "\n")


def main():
    start = time()
    # solve_input("FEHCBGKDINOLAMPJ")
    manhattan100000("FEHCBGKDINOLAMPJ")
    end = time()
    print("Total execution time: %5.2f seconds" % (end - start))


if __name__ == "__main__":
    main()
