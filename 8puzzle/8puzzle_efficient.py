from collections import deque
from time import time


possible_moves = ["DR", "DLR", "DL",
                  "UDR", "UDLR", "UDL",
                  "UR", "ULR", "UL"]
SIZE = 3
GOAL = "012345678"
BLANK = "0"
UP, DOWN, LEFT, RIGHT = "U", "D", "L", "R"


class Node:
    def __init__(self, state, parent, move=""):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = 1
        if parent is not None:
            self.depth += parent.depth
        self.move = move
# end class


def bfs(root):
    fringe = deque([root])
    visited = set([])
    visited.add(root.state)
    while fringe:
        p = fringe.popleft()
        if p.state == GOAL:
            return p
        index = p.state.find(BLANK)
        for d in possible_moves[index]:
            s = make_move(p.state, d, index)
            if s not in visited:
                visited.add(s)
                n = Node(s, p, d)
                p.children += [n]
                fringe.append(n)
    return None


def print_steps(node):
    s = ""
    t = node
    while t is not None:
        s += "\n" + t.state
        t = t.parent
    print("Steps:" + s)


def make_move(s, d, index):  # 1:up 2:down, 3:left, 4:right
    index2 = index
    if d == UP:
        index2 -= SIZE
    elif d == DOWN:
        index2 += SIZE
    elif d == LEFT:
        index2 -= 1
    elif d == RIGHT:
        index2 += 1

    return swap(s, index, index2)


def swap(s, n1, n2):
    t = list(s)
    t[n1], t[n2] = t[n2], t[n1]
    return "".join(t)


def solve_input(string):
    start = time()
    n = bfs(Node(string.strip(), None))
    end = time()
    print("Path length: " + str(n.depth))
    print_steps(n)
    print("Execution time: %5.2f seconds" % (end - start))


def solve_file(filename):
    file = open(filename, "r")
    for line in file:
        start = time()
        n = bfs(Node(line.strip(), None))
        end = time()
        if n is not None:
            print("Puzzle: " + line)
            print("Path length: " + str(n.depth))
            print("Execution time: %5.2f seconds" % (end - start)+"\n")


def main():
    start = time()
    solve_file("sample_puzzles.txt")
    end = time()
    print("Total execution time: %5.2f seconds" % (end - start))

if __name__ == "__main__":
    main()
