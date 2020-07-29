import random
import time
from multiprocessing import Value, Process
import os, signal

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
N, S, E, W = -10, 10, 1, -1
NE, SE, NW, SW = N+E, S+E, N+W, S+W
DIRECTIONS = (N, NE, E, SE, S, SW, W, NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}

STARTING_BOARD = '???????????........??........??........??...o@...??...@o...??........??........??........???????????'
START = 11
END = 89
INDEXES = [x for x in range(START, END) if STARTING_BOARD[x] != OUTER]
CORNERS = [11, 18, 81, 88]
CBORDERS = {
    12: 11,
    17: 18,
    21: 11,
    28: 18,
    71: 81,
    78: 88,
    82: 81,
    87: 88,
}
WEIGHTS = [
 0, 0,    0,  0,  0,  0,  0,  0,   0,   0,
 0, 500, -50, 20, 5,  5,  20, -50, 500, 0,
 0, -50, -80, -5, -5, -5, -5, -80, -50, 0,
 0, 20,  -5,  15, 3,  3,  15, -5,  20,  0,
 0, 5,   -5,  3,  3,  3,  3,  -5,  5,   0,
 0, 5,   -5,  3,  3,  3,  3,  -5,  5,   0,
 0, 20,  -5,  15, 3,  3,  15, -5,  20,  0,
 0, -50, -80, -5, -5, -5, -5, -80, -50, 0,
 0, 500, -50, 20, 5,  5,  20, -50, 500, 0,
 0, 0,    0,  0,  0,  0,  0,  0,   0,   0
]


############################################################
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################


class Node:
    def __init__(self, board, move=-1, score=0):
        self.board = board
        self.move = move
        self.score = score
        self.children = []

    def __lt__(self, other):
        return self.score < other.score
# end class


class Strategy:
    def __init__(self):
        pass

    def get_starting_board(self):
        """Create a new board with the initial black and white positions filled."""
        return STARTING_BOARD
        pass

    def get_pretty_board(self, board):
        """Get a string representation of the board."""
        board = board[START:END].replace("??", "\n")
        return board
        pass

    def opponent(self, player):
        """Get player's opponent."""
        if player == BLACK:
            return WHITE
        return BLACK
        pass

    def find_match(self, board, player, square, direction):
        """
        Find a square that forms a match with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        """
        square += direction
        while board[square] == self.opponent(player):
            square += direction
            if board[square] == player:
                return square
        return None
        pass

    def is_move_valid(self, board, player, move):
        """Is this a legal move for the player?"""
        for direction in DIRECTIONS:
            if self.find_match(board, player, move, direction) is not None:
                return True
        return False
        pass

    def make_move(self, board, player, move):
        """Update the board to reflect the move by the specified player."""
        # returns a new board/string
        square_pairs = {d: self.find_match(board, player, move, d) for d in DIRECTIONS}
        board = list(board)
        for d in square_pairs:
            if square_pairs[d] is not None:
                for s in range(move, square_pairs[d], d):
                    board[s] = player
        return ''.join(board)
        pass

    def get_valid_moves(self, board, player):
        """Get a list of all legal moves for player."""
        return [x for x in range(len(board)) if board[x] == EMPTY and self.is_move_valid(board, player, x)]
        pass

    def has_valid_moves(self, board, player):
        """Can player make any moves?"""
        return len(self.get_valid_moves(board, player)) != 0
        pass

    def next_player(self, board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if self.has_valid_moves(board, self.opponent(prev_player)):
            return self.opponent(prev_player)
        if self.has_valid_moves(board, prev_player):
            return prev_player
        return None
        pass

    def score(self, board, player=BLACK):
        """Compute player's score (number of player's pieces minus opponent's)."""
        score = 0
        for x in INDEXES:
            if board[x] == BLACK:
                score += 1
            elif board[x] == WHITE:
                score -= 1
        return score
        pass

    def frontier(self, board, player=BLACK):
        f = 0
        for x in INDEXES:
            if board[x] == player:
                for d in DIRECTIONS:
                    if board[x+d]==EMPTY:
                        f += 1
                        break
        return f

    def weighted_score(self, board, player=BLACK):
        n = 1 if player == BLACK else -1
        score = random.random()
        for x in INDEXES:
            if board[x] == BLACK:
                score += WEIGHTS[x]
            elif board[x] == WHITE:
                score -= WEIGHTS[x]
        score += len(self.get_valid_moves(board, player))*50*n
        return score

    def weighted_score2(self, board, player=BLACK):
        n = 1 if player == BLACK else -1
        score = random.random()
        for x in INDEXES:
            if board[x] == BLACK:
                score += self.get_weight(board, player, x)
            elif board[x] == WHITE:
                score -= self.get_weight(board, player, x)
        score += len(self.get_valid_moves(board, player))*50*n
        score -= self.frontier(board, player)*15*n
        return score

    def get_weight(self, board, player, x):
        if x in CBORDERS and board[CBORDERS[x]] != EMPTY:
            return abs(WEIGHTS[x])
        return WEIGHTS[x]

    def game_over(self, board, player):
        """Return true if player and opponent have no valid moves"""
        return self.next_player(board, player) is None
        pass

    # Monitoring players
    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    # --------------- strategies ----------------------------- #
    def minmax_search(self, node, player, depth):
        # determine best move for player recursively
        # it may return a move, or a search node, depending on your design
        # feel free to adjust the parameters
        best = {BLACK: max, WHITE: min}
        node.score = self.score(node.board, player)
        if depth == 0:
            return node
        for move in self.get_valid_moves(node.board, player):
            next_board = self.make_move(node.board, player, move)
            next_player = self.next_player(next_board, player)
            if next_player is None:
                node.children.append(Node(next_board, move=move, score=1000*self.score(next_board)))
            else:
                c = Node(next_board, move=move)
                c.score = self.minmax_search(c, next_player, depth=depth-1).score
                node.children.append(c)
        winner = best[player](node.children)
        node.score = winner.score
        return winner
        pass

    def minmax_strategy(self, board, player, depth=4):
        # calls minmax_search
        # feel free to adjust the parameters
        # returns an integer move
        node = Node(board)
        node = self.minmax_search(node, player, depth)
        return node.move
        pass

    def alphabeta_search(self, node, player, depth, a, b):
        best = {BLACK: max, WHITE: min}
        node.score = self.weighted_score(node.board, player)
        if depth == 0:
            return node

        children = []
        for move in self.get_valid_moves(node.board, player):
            next_board = self.make_move(node.board, player, move)
            next_player = self.next_player(next_board, player)
            if next_player is None:
                children.append(Node(next_board, move=move, score=1000*self.score(next_board)))
            else:
                c = Node(next_board, move=move)
                c.score = self.alphabeta_search(c, next_player, depth=depth-1, a=a, b=b).score
                children.append(c)
                if player == BLACK:
                    a = max(a, c.score)
                elif player == WHITE:
                    b = min(b, c.score)
                if a >= b:
                    break
        winner = best[player](children)
        node.score = winner.score
        return winner
        pass

    def alphabeta_strategy(self, board, player, depth=5):
        #for x in CORNERS:
        #    if board[x] == EMPTY and \
        #       self.is_move_valid(board, player, x) and self.is_move_valid(board, self.opponent(player), x):
        #        return x
        node = Node(board)
        node = self.alphabeta_search(node, player, depth, -1000000, 1000000)
        return node.move
        pass

    def alphabeta_search2(self, node, player, depth, a, b):
        best = {BLACK: max, WHITE: min}
        node.score = self.weighted_score2(node.board, player)
        if depth == 0:
            return node

        children = []
        for move in self.get_valid_moves(node.board, player):
            next_board = self.make_move(node.board, player, move)
            next_player = self.next_player(next_board, player)
            if next_player is None:
                children.append(Node(next_board, move=move, score=1000*self.score(next_board)))
            else:
                c = Node(next_board, move=move)
                c.score = self.alphabeta_search2(c, next_player, depth=depth-1, a=a, b=b).score
                children.append(c)
                if player == BLACK:
                    a = max(a, c.score)
                elif player == WHITE:
                    b = min(b, c.score)
                if a >= b:
                    break
        winner = best[player](children)
        node.score = winner.score
        return winner
        pass

    def alphabeta_strategy2(self, board, player, depth=5):
        for x in CORNERS:
            if board[x] == EMPTY and \
               self.is_move_valid(board, player, x) and self.is_move_valid(board, self.opponent(player), x):
                return x
        node = Node(board)
        node = self.alphabeta_search2(node, player, depth, -1000000, 1000000)
        return node.move
        pass


    def random_strategy(self, board, player):
        return random.choice(self.get_valid_moves(board, player))

    def best_strategy(self, board, player, best_move, still_running):
        # THIS IS the public function you must implement
        # Run your best search in a loop and update best_move.value
        depth = 1
        while True:
            best_move.value = self.alphabeta_strategy2(board, player, depth)
            depth += 1

    def test_strategy(self, board, player, best_move, still_running):
        # THIS IS the public function you must implement
        # Run your best search in a loop and update best_move.value
        depth = 1
        while True:
            best_move.value = self.alphabeta_strategy(board, player, depth)
            depth += 1
    standard_strategy = minmax_strategy

silent = False

#################################################
# StandardPlayer runs a single game
# it calls Strategy.standard_strategy(board, player)
#################################################


class StandardPlayer:
    def __init__(self):
        pass

    def play(self):
        # create 2 opponent objects and one referee to play the game
        # these could all be from separate files
        ref = Strategy()
        black = Strategy()
        white = Strategy()

        print("Playing Standard Game")
        board = ref.get_starting_board()
        player = BLACK
        strategy = {BLACK: black.minmax_strategy, WHITE: white.random_strategy}
        print(ref.get_pretty_board(board))

        while player is not None:
            move = strategy[player](board, player)
            print("Player %s chooses %i" % (player, move))
            board = ref.make_move(board, player, move)
            print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))


#################################################
# ParallelPlayer simulated tournament play
# With parallel processes and time limits
# this may not work on Windows, because, Windows is lame
# This calls Strategy.best_strategy(board, player, best_shared, running)
##################################################
class ParallelPlayer:
    def __init__(self, time_limit=5):
        self.black = Strategy()
        self.white = Strategy()
        self.time_limit = time_limit

    def play(self):
        ref = Strategy()
        print("play")
        board = ref.get_starting_board()
        player = BLACK

        print("Playing Parallel Game")
        strategy = lambda who: self.black.best_strategy if who == BLACK else self.white.test_strategy
        while player is not None:
            best_shared = Value("i", -99)
            best_shared.value = -99
            running = Value("i", 1)

            p = Process(target=strategy(player), args=(board, player, best_shared, running))
            # start the subprocess
            t1 = time.time()
            p.start()
            # run the subprocess for time_limit
            p.join(self.time_limit)
            # warn that we're about to stop and wait
            running.value = 0
            time.sleep(0.01)
            # kill the process
            p.terminate()
            time.sleep(0.01)
            # really REALLY kill the process
            if p.is_alive():
                os.kill(p.pid, signal.SIGKILL)
            # see the best move it found
            move = best_shared.value
            if not silent:
                print("move = %i , time = %4.2f" % (move, time.time() - t1))
            if not silent:
                print(board, ref.get_valid_moves(board, player))
            # make the move
            board = ref.make_move(board, player, move)
            if not silent:
                print(ref.get_pretty_board(board))
            player = ref.next_player(board, player)

        print("Final Score %i." % ref.score(board), end=" ")
        print("%s wins" % ("Black" if ref.score(board) > 0 else "White"))

if __name__ == "__main__":
    start = time.time()
    game =  ParallelPlayer(5)
    # game = StandardPlayer()
    game.play()
    # player = Strategy()
    # player.test_score(
    # "???????????o@@@@@@@??oo@@@@@@??ooo@o@@@??ooo@oo@@??@oo@@o@@??o@o@@@oo??oo@@@ooo??.oo@@@@o???????????", "@")
    end = time.time()
    print(end-start)

