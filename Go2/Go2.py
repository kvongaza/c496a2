#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
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
        self.max_depth = 1

    def get_move(self,board, color):
        return GoBoardUtil.generate_random_move(board,color,True)

    def solve(self, board, connection):
        win, move = self.negamax(board, 1, 0)
        return

    def negamax(self, board, color, depth):
        if depth == self.max_depth:
            winner, val = board.score(0) #komi goes here, idk where it is right now
            if winner == color:
                return True, None
            return False, None
        if GoBoardUtil.generate_random_move(board, color, True) is None:
            winner, val = board.score()
            if winner == color:
                return True, None
            return False, None
        moves = GoBoardUtil.generate_legal_moves(board, color).split(' ')
        for _m in moves:
            m = GoBoardUtil.move_to_coord(_m, board.size)
            m = m[0] * board.size + m[1] + 3
            old_board = SimpleGoBoard(board.size); # this is the busted part
            old_board = GoBoardUtil.copyb2b(board, old_board)
            board.move(m, color)
            success = not self.negamax(board, color, depth + 1)
            # board.undo_move()
            board = GoBoardUtil.copyb2b(old_board, board)
            if success:
                return True, m
        return False, None


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnectionGo2(Go2(), board)
    con.start_connection()

if __name__=='__main__':
    run()
