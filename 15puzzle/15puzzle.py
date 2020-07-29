import heapq
from collections import deque
import time
import random


possible_moves = ["DR", "DLR", "DLR", "DL",
                  "UDR", "UDLR", "UDLR", "UDL",
                  "UDR", "UDLR", "UDLR", "UDL",
                  "UR", "ULR", "ULR", "UL"]
SIZE = 4
BLANK = "."
GOAL = "ABCDEFGHIJKLMNO."
GOAL_INDEXES = {}
for i in range(SIZE**2):
    GOAL_INDEXES[GOAL[i]] = i
UP, DOWN, LEFT, RIGHT = "U", "D", "L", "R"
REVERSE_MOVES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT, "":""}
NODE_COUNTER = 0


class Node:
    def __init__(self, state, parent, move=""):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = 0
        self.ancestors = set()
        self.ancestors.add(self.state)
        if parent is not None:
            self.depth = parent.depth + 1
            self.ancestors = self.ancestors.union(parent.ancestors)
        self.move = move
# end class


def greedy(root):
    global NODE_COUNTER
    NODE_COUNTER = 0
    fringe = []
    heapq.heappush(fringe, (h(root.state) + root.depth + random.random(), root))
    visited = set([])
    visited.add(root.state)
    while fringe:
        (score, p) = heapq.heappop(fringe)
        if p.state == GOAL:
            return p
        index = p.state.find(BLANK)
        for d in possible_moves[index]:
            s = make_move(p.state, d, index)
            if s not in visited:
                visited.add(s)
                NODE_COUNTER += 1
                n = Node(s, p, d)
                p.children += [n]
                heapq.heappush(fringe, (h(s) + n.depth + random.random(), n))
    return None


def h(s):
    total = 0
    for x in range(len(s)):
        if s[x] != BLANK:
            total += manhattan(s, x)
    return total


def manhattan(s, n):
    i1, j1 = n_ij(n)
    i2, j2 = n_ij(GOAL_INDEXES[s[n]])
    return abs(i1 - i2) + abs(j1 - j2)


def bfs(root):
    global NODE_COUNTER
    NODE_COUNTER = 0
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
                NODE_COUNTER += 1
                n = Node(s, p, d)
                p.children += [n]
                fringe.append(n)
    return None


def id_dfs(root, k):
    for x in range(1, k):
        node = k_dfs(root, x)
        if node is not None:
            return node


def k_dfs(root, k):
    global NODE_COUNTER
    NODE_COUNTER = 0
    fringe = [root]
    while fringe:
        p = fringe.pop()
        if p.state == GOAL:
            return p
        if p.depth + 1 < k:
            index = p.state.find(BLANK)
            for d in possible_moves[index]:
                s = make_move(p.state, d, index)
                if s not in p.ancestors:
                    NODE_COUNTER += 1
                    n = Node(s, p, d)
                    p.children += [n]
                    fringe.append(n)
    return None


def bi_bfs(root):
    global NODE_COUNTER
    NODE_COUNTER = 0
    fringe1 = deque([root])
    fringe2 = deque([Node(GOAL, None)])
    visited1 = set()
    visited1.add(root.state)
    visited2 = set()
    visited2.add(GOAL)
    dict1 = {root.state: root}
    dict2 = {GOAL: fringe2[0]}
    intersect = visited1 & visited2

    while not intersect:
        p1 = fringe1.popleft()
        p2 = fringe2.popleft()
        index1 = p1.state.find(BLANK)
        index2 = p2.state.find(BLANK)
        for d in possible_moves[index1]:
            s = make_move(p1.state, d, index1)
            if s not in visited1:
                visited1.add(s)
                NODE_COUNTER += 1
                n = Node(s, p1, d)
                dict1[s] = n
                p1.children += [n]
                fringe1.append(n)
        for d in possible_moves[index2]:
            s = make_move(p2.state, d, index2)
            if s not in visited2:
                visited2.add(s)
                NODE_COUNTER += 1
                n = Node(s, p2, d)
                dict2[s] = n
                p2.children += [n]
                fringe2.append(n)
        intersect = visited1 & visited2

    state = intersect.pop()
    n1 = dict1[state]
    n2 = dict2[state].parent
    while n2 is not None:
        n1.children += [Node(n2.state, n1, REVERSE_MOVES[n2.move])]
        n2 = n2.parent
        n1 = n1.children[-1]
    return n1


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

    return swap(s, index, index2)


def swap(s, n1, n2):
    t = list(s)
    t[n1], t[n2] = t[n2], t[n1]
    return "".join(t)


def n_ij(n):
    return n//SIZE, n % SIZE


def gen_start():
    s = GOAL
    for x in range(random.randint(150, 200)):
        index = s.index(BLANK)
        d = possible_moves[index]
        s = make_move(s, d[random.randint(0, len(d)-1)], index)
    print("Puzzle: " + s)
    return s


def solve_input(string):
    start = time.time()
    n = bi_bfs(Node(string.strip(), None))
    end = time.time()
    print("Path length: " + str(n.depth))
    print("Execution time: %5.2f seconds" % (end - start))
    print("Node count: " + str(n.node_count))
    # print_steps(n)


def test_method(f, args, verbose=1):
    global NODE_COUNTER
    NODE_COUNTER = 0

    tic = time.clock()
    sol = f(*args)
    toc = time.clock()

    t = toc - tic
    if verbose == 1:
        print("\n------Testing %s ------- \n" % f.__name__)

        if sol is not None:
            print("Solution Found")
            print("Node count: %i" % NODE_COUNTER)
            print("Length: %i steps, Time: %5.4f" % (sol.depth, t))
            print_steps(sol)
        else:
            print("Unsolvable")

    elif verbose == 0:
        if sol is not None:
            print("Solved. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % (f.__name__, NODE_COUNTER, sol.depth,
                                                                                   t, NODE_COUNTER / t))
        else:
            print("Unsolv. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % (f.__name__, NODE_COUNTER, 0, t,
                                                                                   NODE_COUNTER / t))


def multi_solver(start_state=None):
    if start_state is None:
        state = gen_start()
    else:
        state = start_state
    print("\n---->Solving ", state)

    test_method(bfs, (Node(state, None),), 0)
    test_method(bi_bfs, (Node(state, None),), 0)
    # test_method(k_dfs, (Node(state, None), 22), 0)
    test_method(id_dfs, (Node(state, None), 22), 0)
    test_method(greedy, (Node(state, None),), 0)


def solve_file(filename):
    file = open(filename, "r")
    for line in file:
        multi_solver(line.strip())


def main():
    puzzles = ["ABCDEFGHIJKLMN.O", "ABCDEFKGI.JHMNOL", "A.CDEBFHIJGLMNKO", "AFBD.ECHIKGLMJNO", "ABCDEF.GMIJHNKOL",
               "ABCD.IFGMEJHNOKL", "ABCDEJ.GILFOMNHK", "JACDEFHKIBG.MNOL", "ABCDEFGHIJ.OMNLK", "ABCDEFGHIKLOM.JN",
               "ABCDEFGHINOJMKL.", "ABCDEFGHINOJMKL.", "ABGCENF.ILHDMKJO", "BCDHEAG.IKFLMJNO", ".BCDAJGHEIKLFMNO",
               "ACGDIEBH.FOKMJNL"]
    # for puzz in puzzles:
        # multi_solver(puzz)
    solve_file("puzzles.txt")

if __name__ == "__main__":
    main()
