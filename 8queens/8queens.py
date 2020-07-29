import random
import time
import math
import matplotlib.pyplot as plt

NODES = 0


def csp(state):
    global NODES
    if NODES >= 5000:
        NODES = 0
        csp(start_state(len(state[0])))
    if goal_test(state): return state[0]
    var = pick_var(state) # col
    for val in free_vals(state, var):
        new_state = assign_val(state, var, val)
        if not new_state: continue
        result = csp(new_state)
        NODES += 1
        if result: return result
    return False


def start_state(n):
    return [-1]*n, {x: {y for y in range(n)} for x in range(n)}


def goal_test(state):
    return len(state[-1]) == 0


def pick_var(state):
    return min([x for x in state[-1].keys()], key=lambda x: len(state[-1][x]) + random.random())


def free_vals(state, var):
    vals = [x for x in state[-1][var]]
    vals.sort(key=lambda x: abs(x-(len(state[0])//2)) + random.random())
    return vals


def assign_val(state, var, val):
    new_state = ([state[0][x] if x != var else val for x in range(len(state[0]))],
             {x: {y for y in state[-1][x] if y != val and abs(x - var) != abs(y - val)} for x in state[-1] if x != var})
    for x in new_state[-1]:
        if not new_state[-1][x]:
            return False
    return new_state


def print_board(state):
    if state is None: return
    print(state)
    s = ""
    for x in range(len(state)):
        for i in range(len(state)):
            if state[x] == i: s += "Q "
            else: s += ". "
        s += "\n"
    print(s)


def graph():
    global NODES
    x = []
    n = []
    t = []
    for i in range(5, 201, 2):
        NODES = 0
        start = time.time()
        csp(start_state(i))
        end = time.time()
        x.append(i)
        n.append(math.log(NODES))
        t.append(end-start)
    plt.subplot(211)
    plt.plot(x, n)
    plt.ylabel("log(nodes)")
    plt.subplot(212)
    plt.plot(x, t)
    plt.ylabel("time")
    plt.xlabel("size")
    plt.show()


def run():
    n = int(input("Size: ").strip())
    start = time.time()
    sol = csp(start_state(n))
    end = time.time()
    print("Execution time: %5.2f seconds" % (end - start))
    print_board(sol)


def main():
    graph()


if __name__ == "__main__":
    main()
