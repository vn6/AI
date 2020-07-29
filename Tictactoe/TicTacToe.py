START_BOARD = "........."
SIZE = 3
X_WIN = 1
O_WIN = -1
TIE = 0
MAX = "X"
MIN = "O"


class Node:
    def __init__(self, state, parent, player="O", score=None, move=-1):
        self.state = state
        self.parent = parent
        self.player = player
        self.move = move
        self.score = score
        self.children = []
# end class


def get_children(node):
    for m in valid_moves(node.state):
        node.children.append(make_move(node, m))
    return node.children

def dfs(root):
    fringe = [root]
    final_boards = set([])
    games = 0
    while fringe:
        node = fringe.pop()
        if goal_test(node) is not None:
            final_boards.add(node.state)
            games += 1
        else:
            for m in valid_moves(node.state):
                fringe.append(make_move(node, m))
    return final_boards, games


def valid_moves(board):
    return [x for x in range(len(board)) if board[x] == "."]


def make_move(node, move):
    return Node(node.state[:move] + next_player(node.player) + node.state[move+1:], node,
                player=next_player(node.player), move=move)


def goal_test(node):
    win = X_WIN if node.player == "X" else O_WIN
    rcd = [{x for x in range(i, i+SIZE) if node.state[x] == node.player} for i in range(0, 7, SIZE)] + \
          [{x for x in range(i, i+(SIZE*2)+1, SIZE) if node.state[x] == node.player} for i in range(0, SIZE)] + \
          [{x for x in range(0, 9, 4) if node.state[x] == node.player},
           {x for x in range(2, 7, 2) if node.state[x] == node.player}]
    if len([x for x in rcd if len(x)==SIZE]) > 0:
        return win
    if len(valid_moves(node.state)) == 0:
        return TIE
    return None  # cont game


def next_player(player):
    if player == "X":
        return "O"
    else:
        return "X"


def minmax(node, player):
    node.score = goal_test(node)
    if node.score is not None:
        return node
    if player == MAX:
        node.score = min(get_children(node), key=lambda x:minmax(x, MIN).score).score
    else:
        node.score = max(get_children(node), key=lambda x:minmax(x, MAX).score).score
    return node


def best_move(node, player):
    node = minmax(node, player)
    for n in node.children:
        if n.score == node.score:
            return n.state


def print_board(node):
    print(node.state[:SIZE] + "\n" + node.state[SIZE:SIZE*2] + "\n" + node.state[SIZE*2:] + "\n")


def main():
    boards, games = dfs(Node(START_BOARD, None))
    # for b in boards:
    #     print_board(b)
    print("final boards: " + str(len(boards)))
    print("games: " + str(games))


def play():
    node = Node(START_BOARD, None, player="O")
    goal = None
    while goal is None:
        print_board(node)
        if node.player == "O":
            move = int(input("What Move? (Enter a number from 0 to 9)"))
            node = make_move(node, move)
        else:
            node.state = best_move(node, node.player)
            node.player = next_player(node.player)
        goal = goal_test(node)
    print_board(node)
    if goal == X_WIN:
        print("WIN")
    elif goal == O_WIN:
        print("LOSE")
    elif goal == TIE:
        print("TIE")


if __name__ == "__main__":
    play()