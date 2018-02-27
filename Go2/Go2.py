#! /usr/bin/python3
# Set the path to your python3 above

# Modified by Kiefer von Gaza and Jonah Quist
# Modifications:
#   Implemented functions:
#       timelimit
#       solve
#   Modified functions:
#       genmove

# Set up relative path for util; sys.path[0] is directory of current program
import os, sys
utilpath = sys.path[0] + "/../util/"
sys.path.append(utilpath)

from gtp_connection_go2 import GtpConnectionGo2
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard

class Go2():
    def __init__(self):
        """
        Player that selects moves randomly from the set of legal moves.
        With the fill-eye filter.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "Go2"
        self.version = 0.1
        self.max_depth = 5
        self.nega_moves = []
        self.win = None
        self.searcher = None

    def get_move(self,board, color):
        return GoBoardUtil.generate_random_move(board,color,True)

    def solve(self, board, connection):
        self.nega_moves = [None] * self.max_depth
        self.win = None
        self.searcher = board.current_player
        best = self.negamax(board, board.current_player, 0)
        moves_repr = list(map(str, self.nega_moves))
        if self.win is not None:
            return GoBoardUtil.int_to_color(self.win)
        return '|'.join(moves_repr)

    def negamax(self, board, color, depth):
        if depth == self.max_depth:
            winner, score = board.score(self.komi)
            if winner == color:
                return score
            else:
                return -score 
        if GoBoardUtil.generate_random_move(board, color, True) is None:
            winner, score = board.score(self.komi)
            self.win = color
            if winner == color:
                return score
            else:
                return -score 
        moves = GoBoardUtil.generate_legal_moves(board, color).split(' ')
        best = -float('Inf')
        best_m = None
        for _m in moves:
            m = GoBoardUtil.move_to_coord(_m, board.size)
            m = (board.NS) * m[0] + m[1]
            moved = board.move(m, color)
            if moved:
                value = -self.negamax(board, GoBoardUtil.opponent(color), depth + 1)
                board.undo_move()
            if value > best:
                best = value
                best_m = _m
        if self.searcher == color:
            self.nega_moves[depth] = GoBoardUtil.int_to_color(color) + ' ' + best_m
        return best


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnectionGo2(Go2(), board)
    con.start_connection()

if __name__=='__main__':
    run()
