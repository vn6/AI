from collections import deque
from time import time
import random


possible_moves = ["24", "234", "23", "124", "1234", "123", "14", "134", "13"]
SIZE = 3
GOAL = "012345678"
BLANK = "0"



class Node:
    def __init__(self, state, parent, move=""):
        self.state = state
        self.parent = parent
        self.children = []
        self.prev_states = ""
        self.prev_moves = move
        if parent is not None:
            self.prev_states = parent.prev_states + parent.state + "\n"
            self.prev_moves = parent.prev_moves + " " + move

# end class


def bfs(root):
    count = 1
    fringe = deque([root])
    visited = set([])
    visited.add(root.state)
    left_node = root
    while fringe:
        p = fringe.popleft()
        if p.state == GOAL:
            return p, count

        index0 = p.state.find(BLANK)
        for x in possible_moves[index0]:
            sn = make_move(p.state, x, index0)
            if sn != p.state and sn not in visited:
                visited.add(sn)
                n = Node(sn, p, str(x))
                p.children += [n]
                fringe.append(n)

        if p == left_node:
            count += 1
            if fringe:
                left_node = fringe[-1]
    return None, 0


def make_move(s, d, index0):  # 1:up 2:down, 3:left, 4:right
    index2 = index0
    if d == "1":
        index2 -= 3
    elif d == "2":
        index2 += 3
    elif d == "3":
        index2 -= 1
    elif d == "4":
        index2 += 1

    s = s[:index0] + s[index2] + s[index0 + 1:]
    s = s[:index2] + BLANK + s[index2 + 1:]
    return s


def gen_start():
    s = "012345678"
    for x in range(random.randint(100, 150)):
        index = s.index("0")
        d = possible_moves[index]
        s = make_move(s, d[random.randint(0, len(d)-1)], str(index))
    return s


def swap(s, n1, n2):
    if n1 == n2:
        return s
    if n1 > n2:
        n1, n2 = n2, n1
    return s[:n1] + s[n2] + s[n1 + 1: n2] + s[n1] + s[n2 + 1:]


def rand_puzzle():
    s = "012345678"
    for x in range(random.randint(10, 20)):
        s = swap(s, random.randint(0, len(s)-1), random.randint(0, len(s)-1))
    return s


def solve_rand_permutations(num):
    total_path = 0
    longest_path = 0
    longest_puzzle = ""
    unsolvable = 0
    for x in range(num):
        s = rand_puzzle()
        n, steps = bfs(Node(s, None))
        if n is None:
            unsolvable += 1
        else:
            total_path += steps
        if steps > longest_path:
            longest_path = steps
            longest_puzzle = s

    print("Fraction of solvable puzzles: " + str((num-unsolvable)/num))
    print("Average path length: " + str(total_path/num))
    print("Longest path length: " + str(longest_path))
    print("Longest puzzle: " + longest_puzzle)


def solve_input(string):
    start = time()
    n, path = bfs(Node(string.strip(), None))
    end = time()
    print("Path length: " + str(path))
    print("Execution time: %5.2f seconds" % (end - start))


def solve_file(filename):
    file = open(filename, "r")
    for line in file:
        start = time()
        line = line.strip()
        n, path = bfs(Node(line, None, ""))
        end = time()
        print("Puzzle: " + line)
        print("Path length: " + str(path))
        print("Execution time: %5.2f seconds" % (end - start)+"\n")


def main():
    start = time()
    solve_file("puzzles.txt")
    end = time()
    print("Total execution time: %5.2f seconds" % (end - start))

if __name__ == "__main__":
    main()
