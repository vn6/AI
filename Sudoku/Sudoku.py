import random
from time import time

ROWS = "ABCDEFGHI"
COLS = "123456789"
SQUARES = [r + c for r in ROWS for c in COLS]
UNITS = [{ROWS[n] + c for c in COLS} for n in range(len(ROWS))] + \
        [{r + COLS[n]  for r in ROWS} for n in range(len(COLS))] + \
         [{ROWS[r] + COLS[c] for r in range(ir, ir + 3) for c in range(ic, ic + 3)} # subsquares
          for ir in range(0, len(ROWS), 3) for ic in range(0, len(COLS), 3)]
PEERS = {s: ([p for p in UNITS if s in p][0] |
            [p for p in UNITS if s in p][1] |
            [p for p in UNITS if s in p][2]) - {s} for s in SQUARES}
NODES = 0


def csp(state):
    global NODES
    if goal_test(state): return state
    var = pick_var(state)
    for val in free_vals(state, var):
        new_state = state.copy()
        new_state = assign_val(new_state, var, val)
        if new_state is False: continue
        result = csp(new_state)
        NODES += 1
        if result: return result
    return False


def init_state(start):
    global NODES
    NODES = 0
    state = {x: COLS for x in SQUARES}
    for x in range(len(start)):
        if start[x] != ".":
            state = assign_val(state, SQUARES[x], start[x])
    return state


def goal_test(state):
    for var in state:
        if len(state[var]) > 1:
            return False
    return True


def pick_var(state): # mrv on units: pick unit that has 1 num w/ 1 posssible square then assign
    return min([v for v in state.keys() if len(state[v]) > 1], key=lambda k: len(state[k]) + random.random())


def free_vals(state, var):
    return state[var]


def assign_val(state, var, val):
    state[var] = val
    for s in PEERS[var]:
        i = len(state[s])
        state[s] = "".join([c for c in list(state[s]) if c != val])
        if len(state[s]) == 0: return False
        if i - len(state[s]) > 0 and len(state[s]) == 1:
            new_state = assign_val(state.copy(), s, state[s])
            if new_state is not False: state = new_state
            else: return False
    return state


def print_board(state):
    s = ""
    for x in range(len(SQUARES)):
        if len(state[SQUARES[x]]) == 1:
            s += state[SQUARES[x]] + " "
        else: s += "  "
        if x < len(SQUARES) -1 and (x + 1) % 27 == 0:
            s += "\n------------------\n"
        elif (x + 1) % 9 == 0:
            s += "\n"
        elif (x + 1) % 3 == 0:
            s += "|"
    print(s + "\n")


def solve():
    global NODES
    NODES = 0
    start = time()
    sol = csp(init_state(input("Enter a puzzle: ")))
    end = time()
    print_board(sol)
    print("Execution time: %5.2f seconds" % (end - start))
    print("Nodes: %i" % NODES)


def solve_file(filename):
    global NODES
    file = open(filename, "r")
    for line in file:
        puzz = line.strip().split(",")[-1]
        sol = csp(init_state(puzz))
        print(line.strip() + "Nodes: " + str(NODES))
        print_board(sol)


def main():
    solve_file(input("Enter filename: "))

if __name__ == "__main__":
    main()