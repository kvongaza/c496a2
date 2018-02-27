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
import os, sys, time
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
        self.win = None
        self.startTime = 0.0
        self.timeElapsed = 0.0
        self.timedOut = False

    def get_move(self,board, color):
        return GoBoardUtil.generate_random_move(board,color,True)

    def withinTime(self, startTime, connection):
        self.timeUsed = time.process_time() - startTime
        if self.timeUsed <= connection.timelimit:
            return True
        else:
            return False

    def solve(self, board, connection):
        self.win = None
        self.startTime = time.process_time()
        self.timedOut = False
        _, best = self.negamax(board, board.current_player, 0, connection)
        best = board._point_to_coord(best)
        # Unsure of how to deal with this
        if self.timedOut:
            return(False, "Unknown")
        if self.win is not None:
            return GoBoardUtil.int_to_color(self.win)
        return GoBoardUtil.int_to_color(board.current_player) + ' '+  GoBoardUtil.format_point(best)

    def negamax(self, board, color, depth, connection):
        timeElapsed = time.process_time() -  self.startTime
        if timeElapsed > connection.timelimit:
            self.timedOut = True
            return False, None

        if depth == self.max_depth:
            winner, score = board.score(self.komi)
            if winner == color:
                return True, None
            else:
                return False, None
        if board.end_of_game():
            winner, score = board.score(self.komi)
            self.win = color
            if winner == color:
                return True, None
            else:
                return False, None
        moves = GoBoardUtil.generate_legal_moves(board, color).strip().split(' ')
        for _m in moves:
            m = GoBoardUtil.move_to_coord(_m, board.size)
            m = board._coord_to_point(m[0], m[1])
            if board.is_eye(m, color):
                continue
            board.move(m, color)
            value, _ = self.negamax(board, GoBoardUtil.opponent(color), depth + 1, connection)
            value = not value
            board.undo_move()
            if value:
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
