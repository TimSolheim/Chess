from copy import deepcopy
from matplotlib.animation import FuncAnimation
from matplotlib.colors import BoundaryNorm
from matplotlib.pyplot import imshow
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import show
from matplotlib.pyplot import subplots
from numpy.random import randint
from time import time


class Move:
    def __init__(self, piece, origin, dest, promotion=None, en_pessant=False, castle=None):
        self.piece = piece
        self.origin = origin
        self.dest = dest
        self.promotion = promotion
        self.en_pessant = en_pessant
        self.castle = castle


class ChessBoard:
    num_to_col = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
    col_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    count_check_game_result = 0
    count_check_for_check = 0
    count_get_valid_moves = 0
    count_perform_move = 0
    count_check_for_checkmate = 0
    count_move_validation_check = 0
    count_ChessBoard_initiation = 0
    count_evaluate_position = 0
    count_identify_one_valid_move = 0
    eval_gen = {'W':
        {
            'P': {(1, 2): 50, (1, 3): 58, (1, 4): 66, (1, 5): 74, (1, 6): 82, (1, 7): 90,
                  (2, 2): 50, (2, 3): 62, (2, 4): 74, (2, 5): 86, (2, 6): 98, (2, 7): 110,
                  (3, 2): 50, (3, 3): 66, (3, 4): 82, (3, 5): 98, (3, 6): 114, (3, 7): 130,
                  (4, 2): 50, (4, 3): 70, (4, 4): 90, (4, 5): 110, (4, 6): 130, (4, 7): 150,
                  (5, 2): 50, (5, 3): 70, (5, 4): 90, (5, 5): 110, (5, 6): 130, (5, 7): 150,
                  (6, 2): 50, (6, 3): 66, (6, 4): 82, (6, 5): 98, (6, 6): 114, (6, 7): 130,
                  (7, 2): 50, (7, 3): 62, (7, 4): 74, (7, 5): 86, (7, 6): 98, (7, 7): 110,
                  (8, 2): 50, (8, 3): 58, (8, 4): 66, (8, 5): 74, (8, 6): 82, (8, 7): 90},
            'N': {(1, 1): 300, (1, 2): 303, (1, 3): 307, (1, 4): 310, (1, 5): 310, (1, 6): 307, (1, 7): 303,
                  (1, 8): 300,
                  (2, 1): 300, (2, 2): 312, (2, 3): 328, (2, 4): 340, (2, 5): 340, (2, 6): 328, (2, 7): 312,
                  (2, 8): 300,
                  (3, 1): 300, (3, 2): 324, (3, 3): 356, (3, 4): 380, (3, 5): 380, (3, 6): 356, (3, 7): 324,
                  (3, 8): 300,
                  (4, 1): 300, (4, 2): 330, (4, 3): 370, (4, 4): 400, (4, 5): 400, (4, 6): 370, (4, 7): 330,
                  (4, 8): 300,
                  (5, 1): 300, (5, 2): 330, (5, 3): 370, (5, 4): 400, (5, 5): 400, (5, 6): 370, (5, 7): 330,
                  (5, 8): 300,
                  (6, 1): 300, (6, 2): 324, (6, 3): 356, (6, 4): 380, (6, 5): 380, (6, 6): 356, (6, 7): 324,
                  (6, 8): 300,
                  (7, 1): 300, (7, 2): 312, (7, 3): 328, (7, 4): 340, (7, 5): 340, (7, 6): 328, (7, 7): 312,
                  (7, 8): 300,
                  (8, 1): 300, (8, 2): 303, (8, 3): 307, (8, 4): 310, (8, 5): 310, (8, 6): 307, (8, 7): 303,
                  (8, 8): 300},
            'B': {(1, 1): 325, (1, 2): 325, (1, 3): 325, (1, 4): 325, (1, 5): 325, (1, 6): 325, (1, 7): 325,
                  (1, 8): 325,
                  (2, 1): 325, (2, 2): 329, (2, 3): 333, (2, 4): 337, (2, 5): 337, (2, 6): 333, (2, 7): 329,
                  (2, 8): 325,
                  (3, 1): 325, (3, 2): 333, (3, 3): 341, (3, 4): 349, (3, 5): 349, (3, 6): 341, (3, 7): 333,
                  (3, 8): 325,
                  (4, 1): 325, (4, 2): 337, (4, 3): 349, (4, 4): 361, (4, 5): 361, (4, 6): 349, (4, 7): 337,
                  (4, 8): 325,
                  (5, 1): 325, (5, 2): 337, (5, 3): 349, (5, 4): 361, (5, 5): 361, (5, 6): 349, (5, 7): 337,
                  (5, 8): 325,
                  (6, 1): 325, (6, 2): 333, (6, 3): 341, (6, 4): 349, (6, 5): 349, (6, 6): 341, (6, 7): 333,
                  (6, 8): 325,
                  (7, 1): 325, (7, 2): 329, (7, 3): 333, (7, 4): 337, (7, 5): 337, (7, 6): 333, (7, 7): 329,
                  (7, 8): 325,
                  (8, 1): 325, (8, 2): 325, (8, 3): 325, (8, 4): 325, (8, 5): 325, (8, 6): 325, (8, 7): 325,
                  (8, 8): 325},
            'R': {(1, 1): 516, (1, 2): 512, (1, 3): 508, (1, 4): 504, (1, 5): 504, (1, 6): 508, (1, 7): 512,
                  (1, 8): 516,
                  (2, 1): 532, (2, 2): 524, (2, 3): 516, (2, 4): 508, (2, 5): 508, (2, 6): 516, (2, 7): 524,
                  (2, 8): 532,
                  (3, 1): 548, (3, 2): 536, (3, 3): 524, (3, 4): 512, (3, 5): 512, (3, 6): 524, (3, 7): 536,
                  (3, 8): 548,
                  (4, 1): 564, (4, 2): 548, (4, 3): 532, (4, 4): 516, (4, 5): 516, (4, 6): 532, (4, 7): 548,
                  (4, 8): 564,
                  (5, 1): 564, (5, 2): 548, (5, 3): 532, (5, 4): 516, (5, 5): 516, (5, 6): 532, (5, 7): 548,
                  (5, 8): 564,
                  (6, 1): 548, (6, 2): 536, (6, 3): 524, (6, 4): 512, (6, 5): 512, (6, 6): 524, (6, 7): 536,
                  (6, 8): 548,
                  (7, 1): 532, (7, 2): 524, (7, 3): 516, (7, 4): 508, (7, 5): 508, (7, 6): 516, (7, 7): 524,
                  (7, 8): 532,
                  (8, 1): 516, (8, 2): 512, (8, 3): 508, (8, 4): 504, (8, 5): 504, (8, 6): 508, (8, 7): 512,
                  (8, 8): 516},
            'Q': {(1, 1): 900, (1, 2): 900, (1, 3): 900, (1, 4): 900, (1, 5): 900, (1, 6): 900, (1, 7): 900,
                  (1, 8): 900,
                  (2, 1): 900, (2, 2): 900, (2, 3): 900, (2, 4): 900, (2, 5): 900, (2, 6): 900, (2, 7): 900,
                  (2, 8): 900,
                  (3, 1): 900, (3, 2): 900, (3, 3): 900, (3, 4): 900, (3, 5): 900, (3, 6): 900, (3, 7): 900,
                  (3, 8): 900,
                  (4, 1): 900, (4, 2): 900, (4, 3): 900, (4, 4): 900, (4, 5): 900, (4, 6): 900, (4, 7): 900,
                  (4, 8): 900,
                  (5, 1): 900, (5, 2): 900, (5, 3): 900, (5, 4): 900, (5, 5): 900, (5, 6): 900, (5, 7): 900,
                  (5, 8): 900,
                  (6, 1): 900, (6, 2): 900, (6, 3): 900, (6, 4): 900, (6, 5): 900, (6, 6): 900, (6, 7): 900,
                  (6, 8): 900,
                  (7, 1): 900, (7, 2): 900, (7, 3): 900, (7, 4): 900, (7, 5): 900, (7, 6): 900, (7, 7): 900,
                  (7, 8): 900,
                  (8, 1): 900, (8, 2): 900, (8, 3): 900, (8, 4): 900, (8, 5): 900, (8, 6): 900, (8, 7): 900,
                  (8, 8): 900},
            'K': {(1, 1): 90, (1, 2): 63, (1, 3): 36, (1, 4): 0, (1, 5): 0, (1, 6): 36, (1, 7): 63, (1, 8): 90,
                  (2, 1): 100, (2, 2): 70, (2, 3): 40, (2, 4): 0, (2, 5): 0, (2, 6): 40, (2, 7): 70, (2, 8): 100,
                  (3, 1): 80, (3, 2): 56, (3, 3): 32, (3, 4): 0, (3, 5): 0, (3, 6): 32, (3, 7): 56, (3, 8): 80,
                  (4, 1): 50, (4, 2): 35, (4, 3): 20, (4, 4): 0, (4, 5): 0, (4, 6): 20, (4, 7): 35, (4, 8): 50,
                  (5, 1): 50, (5, 2): 35, (5, 3): 20, (5, 4): 0, (5, 5): 0, (5, 6): 20, (5, 7): 35, (5, 8): 50,
                  (6, 1): 80, (6, 2): 56, (6, 3): 32, (6, 4): 0, (6, 5): 0, (6, 6): 32, (6, 7): 56, (6, 8): 80,
                  (7, 1): 100, (7, 2): 70, (7, 3): 40, (7, 4): 0, (7, 5): 0, (7, 6): 40, (7, 7): 70, (7, 8): 100,
                  (8, 1): 90, (8, 2): 63, (8, 3): 36, (8, 4): 0, (8, 5): 0, (8, 6): 36, (8, 7): 63, (8, 8): 90}
        },
        'B':
            {
                'P': {(1, 2): -90, (1, 3): -82, (1, 4): -74, (1, 5): -66, (1, 6): -58, (1, 7): -50,
                      (2, 2): -110, (2, 3): -98, (2, 4): -86, (2, 5): -74, (2, 6): -62, (2, 7): -50,
                      (3, 2): -130, (3, 3): -114, (3, 4): -98, (3, 5): -82, (3, 6): -66, (3, 7): -50,
                      (4, 2): -150, (4, 3): -130, (4, 4): -110, (4, 5): -90, (4, 6): -70, (4, 7): -50,
                      (5, 2): -150, (5, 3): -130, (5, 4): -110, (5, 5): -90, (5, 6): -70, (5, 7): -50,
                      (6, 2): -130, (6, 3): -114, (6, 4): -98, (6, 5): -82, (6, 6): -66, (6, 7): -50,
                      (7, 2): -110, (7, 3): -98, (7, 4): -86, (7, 5): -74, (7, 6): -62, (7, 7): -50,
                      (8, 2): -90, (8, 3): -82, (8, 4): -74, (8, 5): -66, (8, 6): -58, (8, 7): -50},
                'N': {(1, 1): -300, (1, 2): -303, (1, 3): -307, (1, 4): -310, (1, 5): -310, (1, 6): -307, (1, 7): -303,
                      (1, 8): -300,
                      (2, 1): -300, (2, 2): -312, (2, 3): -328, (2, 4): -340, (2, 5): -340, (2, 6): -328, (2, 7): -312,
                      (2, 8): -300,
                      (3, 1): -300, (3, 2): -324, (3, 3): -356, (3, 4): -380, (3, 5): -380, (3, 6): -356, (3, 7): -324,
                      (3, 8): -300,
                      (4, 1): -300, (4, 2): -330, (4, 3): -370, (4, 4): -400, (4, 5): -400, (4, 6): -370, (4, 7): -330,
                      (4, 8): -300,
                      (5, 1): -300, (5, 2): -330, (5, 3): -370, (5, 4): -400, (5, 5): -400, (5, 6): -370, (5, 7): -330,
                      (5, 8): -300,
                      (6, 1): -300, (6, 2): -324, (6, 3): -356, (6, 4): -380, (6, 5): -380, (6, 6): -356, (6, 7): -324,
                      (6, 8): -300,
                      (7, 1): -300, (7, 2): -312, (7, 3): -328, (7, 4): -340, (7, 5): -340, (7, 6): -328, (7, 7): -312,
                      (7, 8): -300,
                      (8, 1): -300, (8, 2): -303, (8, 3): -307, (8, 4): -310, (8, 5): -310, (8, 6): -307, (8, 7): -303,
                      (8, 8): -300},
                'B': {(1, 1): -325, (1, 2): -325, (1, 3): -325, (1, 4): -325, (1, 5): -325, (1, 6): -325, (1, 7): -325,
                      (1, 8): -325,
                      (2, 1): -325, (2, 2): -329, (2, 3): -333, (2, 4): -337, (2, 5): -337, (2, 6): -333, (2, 7): -329,
                      (2, 8): -325,
                      (3, 1): -325, (3, 2): -333, (3, 3): -341, (3, 4): -349, (3, 5): -349, (3, 6): -341, (3, 7): -333,
                      (3, 8): -325,
                      (4, 1): -325, (4, 2): -337, (4, 3): -349, (4, 4): -361, (4, 5): -361, (4, 6): -349, (4, 7): -337,
                      (4, 8): -325,
                      (5, 1): -325, (5, 2): -337, (5, 3): -349, (5, 4): -361, (5, 5): -361, (5, 6): -349, (5, 7): -337,
                      (5, 8): -325,
                      (6, 1): -325, (6, 2): -333, (6, 3): -341, (6, 4): -349, (6, 5): -349, (6, 6): -341, (6, 7): -333,
                      (6, 8): -325,
                      (7, 1): -325, (7, 2): -329, (7, 3): -333, (7, 4): -337, (7, 5): -337, (7, 6): -333, (7, 7): -329,
                      (7, 8): -325,
                      (8, 1): -325, (8, 2): -325, (8, 3): -325, (8, 4): -325, (8, 5): -325, (8, 6): -325, (8, 7): -325,
                      (8, 8): -325},
                'R': {(1, 1): -516, (1, 2): -512, (1, 3): -508, (1, 4): -504, (1, 5): -504, (1, 6): -508, (1, 7): -512,
                      (1, 8): -516,
                      (2, 1): -532, (2, 2): -524, (2, 3): -516, (2, 4): -508, (2, 5): -508, (2, 6): -516, (2, 7): -524,
                      (2, 8): -532,
                      (3, 1): -548, (3, 2): -536, (3, 3): -524, (3, 4): -512, (3, 5): -512, (3, 6): -524, (3, 7): -536,
                      (3, 8): -548,
                      (4, 1): -564, (4, 2): -548, (4, 3): -532, (4, 4): -516, (4, 5): -516, (4, 6): -532, (4, 7): -548,
                      (4, 8): -564,
                      (5, 1): -564, (5, 2): -548, (5, 3): -532, (5, 4): -516, (5, 5): -516, (5, 6): -532, (5, 7): -548,
                      (5, 8): -564,
                      (6, 1): -548, (6, 2): -536, (6, 3): -524, (6, 4): -512, (6, 5): -512, (6, 6): -524, (6, 7): -536,
                      (6, 8): -548,
                      (7, 1): -532, (7, 2): -524, (7, 3): -516, (7, 4): -508, (7, 5): -508, (7, 6): -516, (7, 7): -524,
                      (7, 8): -532,
                      (8, 1): -516, (8, 2): -512, (8, 3): -508, (8, 4): -504, (8, 5): -504, (8, 6): -508, (8, 7): -512,
                      (8, 8): -516},
                'Q': {(1, 1): -900, (1, 2): -900, (1, 3): -900, (1, 4): -900, (1, 5): -900, (1, 6): -900, (1, 7): -900,
                      (1, 8): -900,
                      (2, 1): -900, (2, 2): -900, (2, 3): -900, (2, 4): -900, (2, 5): -900, (2, 6): -900, (2, 7): -900,
                      (2, 8): -900,
                      (3, 1): -900, (3, 2): -900, (3, 3): -900, (3, 4): -900, (3, 5): -900, (3, 6): -900, (3, 7): -900,
                      (3, 8): -900,
                      (4, 1): -900, (4, 2): -900, (4, 3): -900, (4, 4): -900, (4, 5): -900, (4, 6): -900, (4, 7): -900,
                      (4, 8): -900,
                      (5, 1): -900, (5, 2): -900, (5, 3): -900, (5, 4): -900, (5, 5): -900, (5, 6): -900, (5, 7): -900,
                      (5, 8): -900,
                      (6, 1): -900, (6, 2): -900, (6, 3): -900, (6, 4): -900, (6, 5): -900, (6, 6): -900, (6, 7): -900,
                      (6, 8): -900,
                      (7, 1): -900, (7, 2): -900, (7, 3): -900, (7, 4): -900, (7, 5): -900, (7, 6): -900, (7, 7): -900,
                      (7, 8): -900,
                      (8, 1): -900, (8, 2): -900, (8, 3): -900, (8, 4): -900, (8, 5): -900, (8, 6): -900, (8, 7): -900,
                      (8, 8): -900},
                'K': {(1, 1): -90, (1, 2): -63, (1, 3): -36, (1, 4): 0, (1, 5): 0, (1, 6): -36, (1, 7): -63,
                      (1, 8): -90,
                      (2, 1): -100, (2, 2): -70, (2, 3): -40, (2, 4): 0, (2, 5): 0, (2, 6): -40, (2, 7): -70,
                      (2, 8): -100,
                      (3, 1): -80, (3, 2): -56, (3, 3): -32, (3, 4): 0, (3, 5): 0, (3, 6): -32, (3, 7): -56,
                      (3, 8): -80,
                      (4, 1): -50, (4, 2): -35, (4, 3): -20, (4, 4): 0, (4, 5): 0, (4, 6): -20, (4, 7): -35,
                      (4, 8): -50,
                      (5, 1): -50, (5, 2): -35, (5, 3): -20, (5, 4): 0, (5, 5): 0, (5, 6): -20, (5, 7): -35,
                      (5, 8): -50,
                      (6, 1): -80, (6, 2): -56, (6, 3): -32, (6, 4): 0, (6, 5): 0, (6, 6): -32, (6, 7): -56,
                      (6, 8): -80,
                      (7, 1): -100, (7, 2): -70, (7, 3): -40, (7, 4): 0, (7, 5): 0, (7, 6): -40, (7, 7): -70,
                      (7, 8): -100,
                      (8, 1): -90, (8, 2): -63, (8, 3): -36, (8, 4): 0, (8, 5): 0, (8, 6): -36, (8, 7): -63,
                      (8, 8): -90}
            }}

    @staticmethod
    def read_moves_from_file():
        file = open('C:\\Users\\jtims\\PycharmProjects\\Chess 2\\Game_moves.txt')
        words = file.read().split('\n')
        file.close()
        movelist = []
        for x in words:
            y = x.split(' ')
            if len(y) == 3:
                movelist += [y[1]]
                movelist += [y[2]]
        return movelist

    def __init__(self, board=None, cwl=None, cws=None, cbl=None, cbs=None, ep=None, pl=None):
        # ChessBoard.count_ChessBoard_initiation += 1
        # Row then column
        if board is None:
            self.board = {
                (1, 1): ('W', 'R'), (2, 1): ('W', 'N'), (3, 1): ('W', 'B'), (4, 1): ('W', 'Q'),
                (5, 1): ('W', 'K'), (6, 1): ('W', 'B'), (7, 1): ('W', 'N'), (8, 1): ('W', 'R'),
                (1, 2): ('W', 'P'), (2, 2): ('W', 'P'), (3, 2): ('W', 'P'), (4, 2): ('W', 'P'),
                (5, 2): ('W', 'P'), (6, 2): ('W', 'P'), (7, 2): ('W', 'P'), (8, 2): ('W', 'P'),
                (1, 7): ('B', 'P'), (2, 7): ('B', 'P'), (3, 7): ('B', 'P'), (4, 7): ('B', 'P'),
                (5, 7): ('B', 'P'), (6, 7): ('B', 'P'), (7, 7): ('B', 'P'), (8, 7): ('B', 'P'),
                (1, 8): ('B', 'R'), (2, 8): ('B', 'N'), (3, 8): ('B', 'B'), (4, 8): ('B', 'Q'),
                (5, 8): ('B', 'K'), (6, 8): ('B', 'B'), (7, 8): ('B', 'N'), (8, 8): ('B', 'R')}
        else:
            self.board = board
        if pl is None:
            self.player = 'W'
        else:
            self.player = pl
        self.turn_number = 1
        self.fifty_move_count = 0
        if cws is None:
            self.castle_w_short = True
        else:
            self.castle_w_short = cws
        if cwl is None:
            self.castle_w_long = True
        else:
            self.castle_w_long = cwl
        if cbs is None:
            self.castle_b_short = True
        else:
            self.castle_b_short = cbs
        if cbl is None:
            self.castle_b_long = True
        else:
            self.castle_b_long = cbl
        # Here, en_pessant is the column for en pessant. A value of 0 indicates that there is currently no valid
        # en pessant
        if ep is None:
            self.en_pessant = 0
        else:
            self.en_pessant = ep
        self.valid_move_list = []
        self.player_type_1 = 'H'
        self.player_type_2 = 'AIS'
        self.previous_move = ''

    def show_board(self):
        cmap = ListedColormap(['gainsboro', 'darkgrey', 'darkgrey'])
        map = [[1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1]]
        bounds = [0, 1, 3]
        norm = BoundaryNorm(bounds, cmap.N)
        fig, ax = subplots()
        ax.imshow(map, cmap=cmap, norm=norm, origin='lower')
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0)
        ax.set_xticklabels(['_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        ax.set_yticklabels(['_', '1', '2', '3', '4', '5', '6', '7', '8'])
        for square in self.board:
            if self.board[square][0] == 'W':
                ax.text(square[0] - 1.25, square[1] - 1.25, self.board[square][1], color='white', fontsize=20)
            elif self.board[square][0] == 'B':
                ax.text(square[0] - 1.25, square[1] - 1.25, self.board[square][1], color='black', fontsize=20)
        show()

    def animation_init(self):
        self.im.set_data(self.map)
        return [self.im]

    def animate(self, i):
        self.get_valid_moves()
        if self.player == 'W':
            move = self.convert_notation_to_move(self.moveset[int(i / 2)][0])
        else:
            move = self.convert_notation_to_move(self.moveset[int(i / 2)][1])
        self.perform_move(move)
        # self.to_play = 'B' if self.to_play == 'W' else 'W'
        self.ax.texts = []
        for square in self.board:
            if self.board[square][0] == 'W':
                self.ax.text(square[0] - 1.25, square[1] - 0.75, self.board[square][1], color='white', fontsize=20)
            elif self.board[square][0] == 'B':
                self.ax.text(square[0] - 1.25, square[1] - 0.75, self.board[square][1], color='black', fontsize=20)
        return [self.im, self.ax]

    def animate_move_set(self, moveset):
        fig, self.ax = subplots()
        cmap = ListedColormap(['gainsboro', 'darkgrey', 'darkgrey'])
        self.map = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]]
        self.ax.set_xticklabels(['_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        self.ax.set_yticklabels(['_', '8', '7', '6', '5', '4', '3', '2', '1'])
        for square in self.board:
            if self.board[square][0] == 'W':
                self.ax.text(square[0] - 1.25, square[1] - 0.75, self.board[square][1], color='white', fontsize=20)
            elif self.board[square][0] == 'B':
                self.ax.text(square[0] - 1.25, square[1] - 0.75, self.board[square][1], color='black', fontsize=20)
        self.im = imshow(self.map, cmap=cmap)
        self.moveset = moveset
        an = FuncAnimation(fig, self.animate, init_func=self.animation_init, frames=len(moveset) * 2, interval=500,
                           blit=True, repeat=False)
        show()

    def check_for_check(self, player=None):
        # ChessBoard.count_check_for_check += 1
        if player is None:
            player = self.player
        # Return codes: 0 = No check, 1 = Check, 2 = Error
        opponent = 'B' if player == 'W' else 'W'
        searching = True
        c = 0
        r = 0
        for x in self.board:
            if self.board[x] == (player, 'K'):
                c = x[0]
                r = x[1]
                searching = False
                break
        if searching:
            return 2
        d = 1 if player == 'W' else -1
        if self.board.get((c - 2, r - 1), False) == (opponent, 'N'):
            return 1
        if self.board.get((c - 2, r + 1), False) == (opponent, 'N'):
            return 1
        if self.board.get((c + 2, r - 1), False) == (opponent, 'N'):
            return 1
        if self.board.get((c + 2, r + 1), False) == (opponent, 'N'):
            return 1
        if self.board.get((c - 1, r - 2), False) == (opponent, 'N'):
            return 1
        if self.board.get((c - 1, r + 2), False) == (opponent, 'N'):
            return 1
        if self.board.get((c + 1, r - 2), False) == (opponent, 'N'):
            return 1
        if self.board.get((c + 1, r + 2), False) == (opponent, 'N'):
            return 1
        if self.board.get((c + d, r - 1), False) == (opponent, 'P'):
            return 1
        if self.board.get((c + d, r + 1), False) == (opponent, 'P'):
            return 1
        if self.board.get((c + 1, r + 1), False) == (opponent, 'K'):
            return 1
        if self.board.get((c + 1, r), False) == (opponent, 'K'):
            return 1
        if self.board.get((c + 1, r - 1), False) == (opponent, 'K'):
            return 1
        if self.board.get((c, r + 1), False) == (opponent, 'K'):
            return 1
        if self.board.get((c, r - 1), False) == (opponent, 'K'):
            return 1
        if self.board.get((c - 1, r + 1), False) == (opponent, 'K'):
            return 1
        if self.board.get((c - 1, r), False) == (opponent, 'K'):
            return 1
        if self.board.get((c - 1, r - 1), False) == (opponent, 'K'):
            return 1
        tc = c + 1
        tr = r + 1
        while tc < 9 and tr < 9:
            if self.board.get((tc, tr), False) in ((opponent, 'B'), (opponent, 'Q')):
                return 1
            if self.board.get((tc, tr), False) is not False:
                break
            tc += 1
            tr += 1
        tc = c + 1
        tr = r - 1
        while tc < 9 and 0 < tr:
            if self.board.get((tc, tr), False) in ((opponent, 'B'), (opponent, 'Q')):
                return 1
            if self.board.get((tc, tr), False) is not False:
                break
            tc += 1
            tr -= 1
        tc = c - 1
        tr = r + 1
        while 0 < tc and tr < 9:
            if self.board.get((tc, tr), False) in ((opponent, 'B'), (opponent, 'Q')):
                return 1
            if self.board.get((tc, tr), False) is not False:
                break
            tc -= 1
            tr += 1
        tc = c - 1
        tr = r - 1
        while 0 < tc and 0 < tr:
            if self.board.get((tc, tr), False) in ((opponent, 'B'), (opponent, 'Q')):
                return 1
            if self.board.get((tc, tr), False) is not False:
                break
            tc -= 1
            tr -= 1
        tc = c + 1
        while tc < 9:
            if self.board.get((tc, r), False) in ((opponent, 'R'), (opponent, 'Q')):
                return 1
            if self.board.get((tc, r), False) is not False:
                break
            tc += 1
        tc = c - 1
        while 0 < tc:
            if self.board.get((tc, r), False) in ((opponent, 'R'), (opponent, 'Q')):
                return 1
            if self.board.get((tc, r), False) is not False:
                break
            tc -= 1
        tr = r + 1
        while tr < 9:
            if self.board.get((c, tr), False) in ((opponent, 'R'), (opponent, 'Q')):
                return 1
            if self.board.get((c, tr), False) is not False:
                break
            tr += 1
        tr = r - 1
        while 0 < tr:
            if self.board.get((c, tr), False) in ((opponent, 'R'), (opponent, 'Q')):
                return 1
            if self.board.get((c, tr), False) is not False:
                break
            tr -= 1
        return 0

    def get_valid_moves(self, player=None):
        # t1 = time()
        # ChessBoard.count_get_valid_moves += 1
        if player is None:
            player = self.player
        move_list = []
        opponent = 'W' if player == 'B' else 'B'
        for s in self.board:
            if self.board[s][0] == player:
                if self.board[s][1] == 'P':
                    if player == 'W':
                        if s[1] == 2:
                            if (s[0], 3) not in self.board:
                                move = Move(self.board[s], s, (s[0], 3))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                if (s[0], 4) not in self.board:
                                    move = Move(self.board[s], s, (s[0], 4))
                                    if self.move_validation_check(move) == 0:
                                        move_list += [move]
                            if self.board.get((s[0] - 1, 3), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] - 1, 3))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] + 1, 3), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] + 1, 3))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                        elif 2 < s[1] < 7:
                            if (s[0], s[1] + 1) not in self.board:
                                move = Move(self.board[s], s, (s[0], s[1] + 1))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] - 1, s[1] + 1), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] - 1, s[1] + 1))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] + 1, s[1] + 1), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] + 1, s[1] + 1))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if s[1] == 5 and self.en_pessant != 0:
                                if self.en_pessant in (s[0] - 1, s[0] + 1):
                                    move = Move(self.board[s], s, (self.en_pessant, 6), en_pessant=True)
                                    if self.move_validation_check(move) == 0:
                                        move_list += [move]
                        elif s[1] == 7:
                            if (s[0], 8) not in self.board:
                                move = Move(self.board[s], s, (s[0], 8), promotion='N')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0], 8), promotion='B')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0], 8), promotion='R')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0], 8), promotion='Q')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] + 1, 8), False) == opponent:
                                move = Move(self.board[s], s, (s[0] + 1, 8), promotion='N')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] + 1, 8), promotion='B')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] + 1, 8), promotion='R')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] + 1, 8), promotion='Q')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] - 1, 8), False) == opponent:
                                move = Move(self.board[s], s, (s[0] - 1, 8), promotion='N')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] - 1, 8), promotion='B')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] - 1, 8), promotion='R')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] - 1, 8), promotion='Q')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                    elif player == 'B':
                        if s[1] == 7:
                            if (s[0], 6) not in self.board:
                                move = Move(self.board[s], s, (s[0], 6))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                if (s[0], 5) not in self.board:
                                    move = Move(self.board[s], s, (s[0], 5))
                                    if self.move_validation_check(move) == 0:
                                        move_list += [move]
                            if self.board.get((s[0] - 1, 6), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] - 1, 6))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] + 1, 6), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] + 1, 6))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                        elif 2 < s[1] < 7:
                            if (s[0], s[1] - 1) not in self.board:
                                move = Move(self.board[s], s, (s[0], s[1] - 1))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] - 1, s[1] - 1), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] - 1, s[1] - 1))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] + 1, s[1] - 1), ['_'])[0] == opponent:
                                move = Move(self.board[s], s, (s[0] + 1, s[1] - 1))
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if s[1] == 4 and self.en_pessant != 0:
                                if self.en_pessant in (s[0] - 1, s[0] + 1):
                                    move = Move(self.board[s], s, (self.en_pessant, 3), en_pessant=True)
                                    if self.move_validation_check(move) == 0:
                                        move_list += [move]
                        elif s[1] == 2:
                            if (s[0], 1) not in self.board:
                                move = Move(self.board[s], s, (s[0], 1), promotion='N')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0], 1), promotion='B')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0], 1), promotion='R')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0], 1), promotion='Q')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] + 1, 1), False) == opponent:
                                move = Move(self.board[s], s, (s[0] + 1, 1), promotion='N')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] + 1, 1), promotion='B')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] + 1, 1), promotion='R')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] + 1, 1), promotion='Q')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                            if self.board.get((s[0] - 1, 1), False) == opponent:
                                move = Move(self.board[s], s, (s[0] - 1, 1), promotion='N')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] - 1, 1), promotion='B')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] - 1, 1), promotion='R')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                                move = Move(self.board[s], s, (s[0] - 1, 1), promotion='Q')
                                if self.move_validation_check(move) == 0:
                                    move_list += [move]
                elif self.board[s][1] == 'N':
                    if s[0] > 2 and s[1] > 1 and self.board.get((s[0] - 2, s[1] - 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] - 2, s[1] - 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] < 7 and s[1] > 1 and self.board.get((s[0] + 2, s[1] - 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] + 2, s[1] - 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] > 1 and s[1] > 2 and self.board.get((s[0] - 1, s[1] - 2), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] - 1, s[1] - 2))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] < 8 and s[1] > 2 and self.board.get((s[0] + 1, s[1] - 2), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] + 1, s[1] - 2))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] > 1 and s[1] < 7 and self.board.get((s[0] - 1, s[1] + 2), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] - 1, s[1] + 2))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] < 8 and s[1] < 7 and self.board.get((s[0] + 1, s[1] + 2), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] + 1, s[1] + 2))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] > 2 and s[1] < 8 and self.board.get((s[0] - 2, s[1] + 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] - 2, s[1] + 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] < 7 and s[1] < 8 and self.board.get((s[0] + 2, s[1] + 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] + 2, s[1] + 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                elif self.board[s][1] == 'K':
                    if s[0] > 1 and self.board.get((s[0] - 1, s[1]), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] - 1, s[1]))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] > 1 and s[1] > 1 and self.board.get((s[0] - 1, s[1] - 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] - 1, s[1] - 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] > 1 and s[1] < 8 and self.board.get((s[0] - 1, s[1] + 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] - 1, s[1] + 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[1] > 1 and self.board.get((s[0], s[1] - 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0], s[1] - 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[1] < 8 and self.board.get((s[0], s[1] + 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0], s[1] + 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] < 8 and self.board.get((s[0] + 1, s[1]), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] + 1, s[1]))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] < 8 and s[1] > 1 and self.board.get((s[0] + 1, s[1] - 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] + 1, s[1] - 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if s[0] < 8 and s[1] < 8 and self.board.get((s[0] + 1, s[1] + 1), ['_'])[0] != player:
                        move = Move(self.board[s], s, (s[0] + 1, s[1] + 1))
                        if self.move_validation_check(move) == 0:
                            move_list += [move]
                    if player == 'W':
                        if self.castle_w_long and (2, 1) not in self.board and (3, 1) not in self.board and (
                           4, 1) not in self.board:
                            move = Move(('W', 'K'), (5, 1), (3, 1), castle='long')
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                        if self.castle_w_short and (6, 1) not in self.board and (7, 1) not in self.board:
                            move = Move(('W', 'K'), (5, 1), (7, 1), castle='short')
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                    if player == 'B':
                        if self.castle_b_long and (2, 8) not in self.board and (3, 8) not in self.board and (
                           4, 8) not in self.board:
                            move = Move(('B', 'K'), (5, 8), (3, 8), castle='long')
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                        if self.castle_b_short and (6, 8) not in self.board and (7, 8) not in self.board:
                            move = Move(('B', 'K'), (5, 8), (7, 8), castle='short')
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                elif self.board[s][1] in ('B', 'Q'):
                    tc = s[0] - 1
                    tr = s[1] - 1
                    while tc > 0 and tr > 0:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tc -= 1
                            tr -= 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
                    tc = s[0] + 1
                    tr = s[1] - 1
                    while tc < 9 and tr > 0:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tc += 1
                            tr -= 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
                    tc = s[0] - 1
                    tr = s[1] + 1
                    while tc > 0 and tr < 9:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tc -= 1
                            tr += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
                    tc = s[0] + 1
                    tr = s[1] + 1
                    while tc < 9 and tr < 9:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tc += 1
                            tr += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
                if self.board[s][1] in ('R', 'Q'):
                    tc = s[0] - 1
                    tr = s[1]
                    while tc > 0:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tc -= 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
                    tc = s[0] + 1
                    tr = s[1]
                    while tc < 9:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tc += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
                    tc = s[0]
                    tr = s[1] + 1
                    while tr < 9:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tr += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
                    tc = s[0]
                    tr = s[1] - 1
                    while tr > 0:
                        if (tc, tr) not in self.board:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            tr -= 1
                        elif self.board[(tc, tr)][0] == opponent:
                            move = Move(self.board[s], s, (tc, tr))
                            if self.move_validation_check(move) == 0:
                                move_list += [move]
                            break
                        else:
                            break
        self.valid_move_list = move_list
        # t2 = time()
        # print(f'Get valid moves  {t2-t1}')

    def identify_one_valid_move(self, player=None):
        # ChessBoard.count_identify_one_valid_move += 1
        if player is None:
            player = self.player
        self.valid_move_list = []
        opponent = 'W' if player == 'B' else 'B'
        for s in self.board:
            if self.board[s][0] == player:
                if self.board[s][1] == 'P':
                    if player == 'W':
                        if s[1] == 2:
                            if (s[0], 3) not in self.board:
                                if self.move_validation_check(Move(self.board[s], s, (s[0], 3))) == 0:
                                    return True
                                if (s[0], 4) not in self.board:
                                    if self.move_validation_check(Move(self.board[s], s, (s[0], 4))) == 0:
                                        return True
                            if self.board.get((s[0] - 1, 3), ['_'][0]) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, 3))) == 0:
                                    return True
                            if self.board.get((s[0] + 1, 3), ['_'][0]) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, 3))) == 0:
                                    return True
                        elif 2 < s[1] < 7:
                            if (s[0], s[1] + 1) not in self.board:
                                if self.move_validation_check(Move(self.board[s], s, (s[0], s[1] + 1))) == 0:
                                    return True
                            if self.board.get((s[0] - 1, s[1] + 1), ['_'][0]) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, s[1] + 1))) == 0:
                                    return True
                            if self.board.get((s[0] + 1, s[1] + 1), ['_'][0]) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, s[1] + 1))) == 0:
                                    return True
                            if s[1] == 5 and self.en_pessant != 0:
                                if self.en_pessant in (s[0] - 1, s[0] + 1):
                                    if self.move_validation_check(
                                            Move(self.board[s], s, (self.en_pessant, 6), en_pessant=True)) == 0:
                                        return True
                        elif s[1] == 7:
                            if (s[0], 8) not in self.board:
                                if self.move_validation_check(Move(self.board[s], s, (s[0], 8), promotion='N')) == 0:
                                    return True
                            if self.board.get((s[0] + 1, 8), False) == opponent:
                                if self.move_validation_check(
                                        Move(self.board[s], s, (s[0] + 1, 8), promotion='N')) == 0:
                                    return True
                            if self.board.get((s[0] - 1, 8), False) == opponent:
                                if self.move_validation_check(
                                        Move(self.board[s], s, (s[0] - 1, 8), promotion='N')) == 0:
                                    return True
                    elif player == 'B':
                        if s[1] == 7:
                            if (s[0], 6) not in self.board:
                                if self.move_validation_check(Move(self.board[s], s, (s[0], 6))) == 0:
                                    return True
                                if (s[0], 5) not in self.board:
                                    if self.move_validation_check(Move(self.board[s], s, (s[0], 5))) == 0:
                                        return True
                            if self.board.get((s[0] - 1, 6), False) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, 6))) == 0:
                                    return True
                            if self.board.get((s[0] + 1, 6), False) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, 6))) == 0:
                                    return True
                        elif 2 < s[1] < 7:
                            if (s[0], s[1] - 1) not in self.board:
                                if self.move_validation_check(Move(self.board[s], s, (s[0], s[1] - 1))) == 0:
                                    return True
                            if self.board.get((s[0] - 1, s[1] - 1), False) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, s[1] - 1))) == 0:
                                    return True
                            if self.board.get((s[0] + 1, s[1] - 1), False) == opponent:
                                if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, s[1] - 1))) == 0:
                                    return True
                            if s[1] == 4 and self.en_pessant != 0:
                                if self.en_pessant in (s[0] - 1, s[0] + 1):
                                    if self.move_validation_check(
                                            Move(self.board[s], s, (self.en_pessant, 3), en_pessant=True)) == 0:
                                        return True
                        elif s[1] == 2:
                            if (s[0], 1) not in self.board:
                                if self.move_validation_check(Move(self.board[s], s, (s[0], 1), promotion='N')) == 0:
                                    return True
                            if self.board.get((s[0] + 1, 1), False) == opponent:
                                if self.move_validation_check(
                                        Move(self.board[s], s, (s[0] + 1, 1), promotion='N')) == 0:
                                    return True
                            if self.board.get((s[0] - 1, 1), False) == opponent:
                                if self.move_validation_check(
                                        Move(self.board[s], s, (s[0] - 1, 1), promotion='N')) == 0:
                                    return True
                elif self.board[s][1] == 'N':
                    if s[0] > 2 and s[1] > 1 and self.board.get((s[0] - 2, s[1] - 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] - 2, s[1] - 1))) == 0:
                            return True
                    if s[0] < 7 and s[1] > 1 and self.board.get((s[0] + 2, s[1] - 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] + 2, s[1] - 1))) == 0:
                            return True
                    if s[0] > 1 and s[1] > 2 and self.board.get((s[0] - 1, s[1] - 2), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, s[1] - 2))) == 0:
                            return True
                    if s[0] < 8 and s[1] > 2 and self.board.get((s[0] + 1, s[1] - 2), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, s[1] - 2))) == 0:
                            return True
                    if s[0] > 1 and s[1] < 7 and self.board.get((s[0] - 1, s[1] + 2), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, s[1] + 2))) == 0:
                            return True
                    if s[0] < 8 and s[1] < 7 and self.board.get((s[0] + 1, s[1] + 2), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, s[1] + 2))) == 0:
                            return True
                    if s[0] > 2 and s[1] < 8 and self.board.get((s[0] - 2, s[1] + 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] - 2, s[1] + 1))) == 0:
                            return True
                    if s[0] < 7 and s[1] < 8 and self.board.get((s[0] + 2, s[1] + 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] + 2, s[1] + 1))) == 0:
                            return True
                elif self.board[s][1] == 'K':
                    if s[0] > 1 and self.board.get((s[0] - 1, s[1]), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, s[1]))) == 0:
                            return True
                    if s[0] > 1 and s[1] > 1 and self.board.get((s[0] - 1, s[1] - 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, s[1] - 1))) == 0:
                            return True
                    if s[0] > 1 and s[1] < 8 and self.board.get((s[0] - 1, s[1] + 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] - 1, s[1] + 1))) == 0:
                            return True
                    if s[1] > 1 and self.board.get((s[0], s[1] - 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0], s[1] - 1))) == 0:
                            return True
                    if s[1] < 8 and self.board.get((s[0], s[1] + 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0], s[1] + 1))) == 0:
                            return True
                    if s[0] < 8 and self.board.get((s[0] + 1, s[1]), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, s[1]))) == 0:
                            return True
                    if s[0] < 8 and s[1] > 1 and self.board.get((s[0] + 1, s[1] - 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, s[1] - 1))) == 0:
                            return True
                    if s[0] < 8 and s[1] < 8 and self.board.get((s[0] + 1, s[1] + 1), ['_'])[0] != player:
                        if self.move_validation_check(Move(self.board[s], s, (s[0] + 1, s[1] + 1))) == 0:
                            return True
                if self.board[s][1] in ('B', 'Q'):
                    tc = s[0] - 1
                    tr = s[1] - 1
                    while tc > 0 and tr > 0:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tc -= 1
                            tr -= 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
                    tc = s[0] + 1
                    tr = s[1] - 1
                    while tc < 9 and tr > 0:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tc += 1
                            tr -= 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
                    tc = s[0] - 1
                    tr = s[1] + 1
                    while tc > 0 and tr < 9:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tc -= 1
                            tr += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
                    tc = s[0] + 1
                    tr = s[1] + 1
                    while tc < 9 and tr < 9:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tc += 1
                            tr += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
                if self.board[s][1] in ('R', 'Q'):
                    tc = s[0] - 1
                    tr = s[1]
                    while tc > 0:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tc -= 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
                    tc = s[0] + 1
                    tr = s[1]
                    while tc < 9:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tc += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
                    tc = s[0]
                    tr = s[1] + 1
                    while tr < 9:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tr += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
                    tc = s[0]
                    tr = s[1] - 1
                    while tr > 0:
                        if (tc, tr) not in self.board:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            tr += 1
                        elif self.board[(tc, tr)][0] == opponent:
                            if self.move_validation_check(Move(self.board[s], s, (tc, tr))) == 0:
                                return True
                            break
                        else:
                            break
        return False

    def perform_move(self, move):
        # ChessBoard.count_perform_move += 1
        if move.piece[1] == 'P' or move.dest in self.board:
            self.fifty_move_count = 0
        else:
            self.fifty_move_count += 1
        if move.castle is None:
            self.board[move.dest] = move.piece
            del self.board[move.origin]
            if move.en_pessant is True:
                if self.player == 'W':
                    del self.board[(self.en_pessant, 5)]
                elif self.player == 'B':
                    del self.board[(self.en_pessant, 4)]
            elif move.promotion is not None:
                self.board[move.dest] = (self.player, move.promotion)
            elif move.piece[1] == 'K':
                if move.piece[0] == 'W':
                    self.castle_w_long = False
                    self.castle_w_short = False
                else:
                    self.castle_b_long = False
                    self.castle_b_short = False
            elif move.piece[1] == 'R':
                if move.piece[0] == 'W':
                    if move.origin == (1, 1):
                        self.castle_w_long = False
                    elif move.origin == (8, 1):
                        self.castle_w_short = False
                else:
                    if move.origin == (1, 8):
                        self.castle_b_long = False
                    elif move.origin == (8, 8):
                        self.castle_b_short = False
            if move.piece[1] == 'P' and (move.piece[0] == 'W' and move.origin[1] == 2 and move.dest[1] == 4) or \
                    (move.piece[0] == 'B' and move.origin[1] == 7 and move.dest[1] == 5):
                self.en_pessant = move.dest[0]
            else:
                self.en_pessant = 0
        else:
            if self.player == 'W':
                if move.castle == 'long':
                    self.board[(3, 1)] = ('W', 'K')
                    self.board[(4, 1)] = ('W', 'R')
                    del self.board[(1, 1)]
                    del self.board[(5, 1)]
                elif move.castle == 'short':
                    self.board[(6, 1)] = ('W', 'R')
                    self.board[(7, 1)] = ('W', 'K')
                    del self.board[(8, 1)]
                    del self.board[(5, 1)]
                self.castle_w_long = False
                self.castle_w_short = False
            elif self.player == 'B':
                if move.castle == 'long':
                    self.board[(3, 8)] = ('B', 'K')
                    self.board[(4, 8)] = ('B', 'R')
                    del self.board[(1, 8)]
                    del self.board[(5, 8)]
                elif move.castle == 'short':
                    self.board[(6, 8)] = ('B', 'R')
                    self.board[(7, 8)] = ('B', 'K')
                    del self.board[(8, 8)]
                    del self.board[(5, 8)]
                self.castle_b_long = False
                self.castle_b_short = False
            self.en_pessant = 0
        self.player = 'B' if self.player == 'W' else 'W'

    def move_validation_check(self, move):
        # ChessBoard.count_move_validation_check += 1
        temp_board = ChessBoard(self.board.copy(), self.castle_w_long, self.castle_w_short, self.castle_b_long,
                                self.castle_b_short, self.en_pessant, self.player)
        if move.castle is None:
            temp_board.perform_move(move)
            result = temp_board.check_for_check(self.player)
            return result
        else:
            result = temp_board.check_for_check(self.player)
            if result == 1:
                return 1
            temp_board.perform_move(move)
            result = temp_board.check_for_check(self.player)
            if result == 1:
                return 1
            if self.player == 'W':
                if move.castle == 'long':
                    if self.board.get((2, 2), False) == ('B', 'N'):
                        return 1
                    if self.board.get((6, 2), False) == ('B', 'N'):
                        return 1
                    if self.board.get((3, 3), False) == ('B', 'N'):
                        return 1
                    if self.board.get((5, 3), False) == ('B', 'N'):
                        return 1
                    if self.board.get((3, 2), False) == ('B', 'P'):
                        return 1
                    if self.board.get((5, 2), False) == ('B', 'P'):
                        return 1
                    for i in range(2, 9):
                        if self.board.get((4, i), False) in (('B', 'R'), ('B', 'Q')):
                            return 1
                        elif (4, i) in self.board:
                            break
                    for i in range(2, 5):
                        if self.board.get((5 - i, i), False) in (('B', 'B'), ('B', 'Q')):
                            return 1
                        elif (5 - i, i) in self.board:
                            break
                    for i in range(2, 6):
                        if self.board.get((3 + i, i), False) in (('B', 'B'), ('B', 'Q')):
                            return 1
                        elif (3 + i, i) in self.board:
                            break
                elif move.castle == 'short':
                    if self.board.get((4, 2), False) == ('B', 'N'):
                        return 1
                    if self.board.get((8, 2), False) == ('B', 'N'):
                        return 1
                    if self.board.get((5, 3), False) == ('B', 'N'):
                        return 1
                    if self.board.get((7, 3), False) == ('B', 'N'):
                        return 1
                    if self.board.get((5, 2), False) == ('B', 'P'):
                        return 1
                    if self.board.get((7, 2), False) == ('B', 'P'):
                        return 1
                    for i in range(2, 9):
                        if self.board.get((6, i), False) in (('B', 'R'), ('B', 'Q')):
                            return 1
                        elif (6, i) in self.board:
                            break
                    for i in range(2, 4):
                        if self.board.get((5 + i, i), False) in (('B', 'B'), ('B', 'Q')):
                            return 1
                        elif (5 + i, i) in self.board:
                            break
                    for i in range(2, 7):
                        if self.board.get((7 - i, i), False) in (('B', 'B'), ('B', 'Q')):
                            return 1
                        elif (7 - i, i) in self.board:
                            break
            elif self.player == 'B':
                if move.castle == 'long':
                    if self.board.get((2, 7), False) == ('W', 'N'):
                        return 1
                    if self.board.get((6, 7), False) == ('W', 'N'):
                        return 1
                    if self.board.get((3, 6), False) == ('W', 'N'):
                        return 1
                    if self.board.get((5, 6), False) == ('W', 'N'):
                        return 1
                    if self.board.get((3, 7), False) == ('W', 'P'):
                        return 1
                    if self.board.get((5, 7), False) == ('W', 'P'):
                        return 1
                    for i in range(1, 8):
                        if self.board.get((4, i), False) in (('W', 'R'), ('W', 'Q')):
                            return 1
                        elif (4, i) in self.board:
                            break
                    for i in range(5, 8):
                        if self.board.get((i - 4, i), False) in (('W', 'B'), ('W', 'Q')):
                            return 1
                        elif (i - 4, i) in self.board:
                            break
                    for i in range(4, 8):
                        if self.board.get((12 - i, i), False) in (('W', 'B'), ('W', 'Q')):
                            return 1
                        elif (12 - i, i) in self.board:
                            break
                elif move.castle == 'short':
                    if self.board.get((4, 7), False) == ('W', 'N'):
                        return 1
                    if self.board.get((8, 7), False) == ('W', 'N'):
                        return 1
                    if self.board.get((5, 6), False) == ('W', 'N'):
                        return 1
                    if self.board.get((7, 6), False) == ('W', 'N'):
                        return 1
                    if self.board.get((5, 7), False) == ('W', 'P'):
                        return 1
                    if self.board.get((7, 7), False) == ('W', 'P'):
                        return 1
                    for i in range(1, 8):
                        if self.board.get((6, i), False) in (('W', 'R'), ('W', 'Q')):
                            return 1
                        elif (6, i) in self.board:
                            break
                    for i in range(3, 8):
                        if self.board.get((i - 2, i), False) in (('W', 'B'), ('W', 'Q')):
                            return 1
                        elif (i - 2, i) in self.board:
                            break
                    for i in range(6, 8):
                        if self.board.get((14 - i, i), False) in (('W', 'B'), ('W', 'Q')):
                            return 1
                        elif (14 - i, i) in self.board:
                            break

    def check_for_checkmate(self):
        # ChessBoard.count_check_for_checkmate += 1
        in_check = self.check_for_check(self.player)
        if in_check == 1:
            self.get_valid_moves()
            if len(self.valid_move_list) == 0:
                return 1
        return 0

    def convert_move_to_notation(self, move):
        if move.castle == 'short':
            notation = 'O-O'
        elif move.castle == 'long':
            notation = 'O-O-O'
        else:
            if move.piece[1] == 'P':
                if move.origin[0] == move.dest[0]:
                    notation = ''
                else:
                    notation = ChessBoard.num_to_col[move.origin[0]] + 'x'
            else:
                notation = move.piece[1]
                if move.piece[1] not in ('P', 'K'):
                    c = False
                    r = False
                    for this_move in self.valid_move_list:
                        if this_move.piece == move.piece and this_move.dest == move.dest and \
                                this_move.origin != move.origin:
                            if this_move.origin[0] == move.origin[0]:
                                r = True
                            elif this_move.origin[1] == move.origin[1]:
                                c = True
                    if c:
                        notation += ChessBoard.num_to_col[this_move.origin[0]]
                    if r:
                        notation += str(this_move.origin[1])
                if move.dest in self.board:
                    notation += 'x'
            notation += ChessBoard.num_to_col[move.dest[0]] + str(move.dest[1])
        temp_board = ChessBoard(self.board.copy(), self.castle_w_long, self.castle_w_short, self.castle_b_long,
                                self.castle_b_short, self.en_pessant, self.player)
        temp_board.perform_move(move)
        opponent = 'W' if self.player == 'B' else 'B'
        if move.promotion is not None:
            notation += '=' + move.promotion
        r = temp_board.check_for_check()
        if r == 1:
            r = temp_board.check_for_checkmate()
            if r == 0:
                notation += '+'
            elif r == 1:
                notation += '#'
        return notation

    def convert_notation_to_move(self, notation):
        if len(notation) < 2:
            return False
        promote = ''
        if notation[-1] in ('+', '#'):
            notation = notation[:-1]
        if notation == '0-0':
            if self.player == 'W':
                return Move(('W', 'K'), (5, 1), (7, 1), castle='short')
            elif self.player == 'B':
                return Move(('B', 'K'), (5, 8), (7, 8), castle='short')
        elif notation == '0-0-0':
            if self.player == 'W':
                return Move(('W', 'K'), (5, 1), (3, 1), castle='long')
            elif self.player == 'B':
                return Move(('B', 'K'), (5, 8), (3, 8), castle='long')
        if notation[0] in ('N', 'B', 'R', 'Q', 'K'):
            piece = notation[0]
            if notation[1] == 'x':
                notation = notation[2:]
            else:
                notation = notation[1:]
            if len(notation) < 2:
                return False
            dest = notation[-2:]
            notation = notation[:-2]
            if notation == '':
                disamb_c = 0
                disamb_r = 0
            else:
                if notation[0] in ChessBoard.col_to_num:
                    disamb_c = ChessBoard.col_to_num[notation[0]]
                    if len(notation) > 1:
                        disamb_r = int(notation[1])
                    else:
                        disamb_r = 0
                elif notation[0] in ('1', '2', '3', '4', '5', '6', '7', '8'):
                    disamb_c = 0
                    disamb_r = int(notation[0])
                else:
                    disamb_c = 0
                    disamb_r = 0
        else:
            piece = 'P'
            if notation[1] == 'x':
                disamb_c = ChessBoard.col_to_num[notation[0]]
                disamb_r = 0
                notation = notation[2:]
                if len(notation) < 2:
                    return False
            else:
                disamb_c = 0
                disamb_r = 0
            dest = notation[:2]
            if len(notation) > 2:
                promote = notation[-1]
        if dest[0] not in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h') or \
                dest[1] not in ('1', '2', '3', '4', '5', '6', '7', '8'):
            return False
        dest = (ChessBoard.col_to_num[dest[0]], int(dest[1]))
        searching = True
        for test_move in self.valid_move_list:
            if test_move.piece[1] == piece and test_move.dest == dest and \
                    ((test_move.promotion is None and promote == '') or (
                            test_move.promotion is not None and test_move.promotion == promote)) and \
                    ((disamb_c == 0 or disamb_c == test_move.origin[0]) and (
                            disamb_r == 0 or disamb_r == test_move.origin[1])):
                found_move = deepcopy(test_move)
                searching = False
                break
        if searching:
            print('No valid move found!')
            return False
        else:
            return found_move

    def get_ai_recursive_minimax(self, current_depth, max_depth, input_chess_board, current_player, minimax_score):
        best_evaluation = 'I'
        current_player = 'B' if current_player == 'W' else 'W'
        input_chess_board.get_valid_moves()
        for this_move in input_chess_board.valid_move_list:
            temp_chess_board = ChessBoard(input_chess_board.board.copy(), input_chess_board.castle_w_long,
                                          input_chess_board.castle_w_short,
                                          input_chess_board.castle_b_long, input_chess_board.castle_b_short,
                                          input_chess_board.en_pessant, input_chess_board.player)
            temp_chess_board.perform_move(this_move)
            if current_depth < max_depth:
                evaluation = self.get_ai_recursive_minimax(current_depth + 1, max_depth, temp_chess_board,
                                                           current_player, best_evaluation)
            else:
                evaluation = temp_chess_board.evaluate_position(current_player)
                if evaluation == -1000000:
                    evaluation += current_depth * 2000
                elif evaluation == 1000000:
                    evaluation -= current_depth * 2000
            if current_player == 'W':
                if best_evaluation == 'I' or evaluation > best_evaluation:
                    best_evaluation = evaluation
                if minimax_score != 'I' and best_evaluation > minimax_score:
                    # Minimax: Because one of white's options for this move is better than their best option for a
                    # previously calculated move, black will not select this option, hence further calculation is
                    # unnecessary
                    return best_evaluation
            # Otherwise current_player = 'black'
            else:
                if best_evaluation == 'I' or evaluation < best_evaluation:
                    best_evaluation = evaluation
                if minimax_score != 'I' and best_evaluation < minimax_score:
                    # Minimax: Because one of black's options for this move is better than their best option for a
                    # previously calculated move, white will not select this option, hence further calculation is
                    # unnecessary.
                    return best_evaluation
        if len(input_chess_board.valid_move_list) == 0 or best_evaluation == 'I':
            if not input_chess_board.check_for_check():
                return 0
            if current_player == 'W':
                return -1000000 + current_depth * 2000
            # Otherwise current_player = 'black'
            else:
                return 1000000 - current_depth * 2000
        return best_evaluation

    def get_ai_move(self, depth):
        tolerance = 0
        # a = self.chess_board.evaluate_position('white')
        # e_time = perf_counter()
        # print(e_time - start_time)
        self.get_valid_moves()
        if len(self.valid_move_list) == 0:
            return False
        # for i in range(len(valid_move_list)):
        # print(i, self.convert_to_notation(valid_move_list[i], self.to_play))
        moves_considered = []
        best_evaluation = 'I'
        for this_move in self.valid_move_list:
            temp_chess_board = ChessBoard(self.board.copy(), self.castle_w_long, self.castle_w_short,
                                          self.castle_b_long, self.castle_b_short, self.en_pessant, self.player)
            temp_chess_board.perform_move(this_move)
            if not temp_chess_board.check_for_check():
                if best_evaluation == 'I':
                    minimax_score = 'I'
                elif self.player == 'W':
                    minimax_score = best_evaluation - tolerance
                else:
                    minimax_score = best_evaluation + tolerance
                evaluation = self.get_ai_recursive_minimax(2, depth, temp_chess_board, self.player, minimax_score)
                if self.player == 'W':
                    if best_evaluation == 'I' or evaluation > best_evaluation:
                        best_evaluation = evaluation
                    if evaluation >= best_evaluation - tolerance:
                        moves_considered += [[this_move, evaluation]]
                # Otherwise self.to_play = 'black'
                else:
                    if best_evaluation == 'I' or evaluation < best_evaluation:
                        best_evaluation = evaluation
                    if evaluation <= best_evaluation + tolerance:
                        moves_considered += [[this_move, evaluation]]
                # print(self.chess_board.convert_to_notation(this_move, self.to_play), evaluation)
        # This removes positions that were of appropriate evaluation when analysed, but are not at the end
        i = 0
        while i < len(moves_considered):
            if self.player == 'W':
                if moves_considered[i][1] < best_evaluation - tolerance:
                    moves_considered.pop(i)
                else:
                    i += 1
            # Otherwise self.to_play = 'black'
            elif moves_considered[i][1] > best_evaluation + tolerance:
                moves_considered.pop(i)
            else:
                i += 1
        move_id = randint(len(moves_considered))
        return moves_considered[move_id][0]

    def evaluate_position(self, player):
        # ChessBoard.count_evaluate_position += 1
        player = 'B' if player == 'W' else 'W'
        valid_moves = self.identify_one_valid_move()
        if not valid_moves:
            if self.check_for_check(player):
                if player == 'W':
                    return -1000000
                # Otherwise player = 'black'
                else:
                    return 1000000
            else:
                return 0
        else:
            evaluation = 0
            # temp_dict = {'K': 0, 'P': 100, 'N': 300, 'B': 325, 'R': 500, 'Q': 900}
            for x in self.board:
                # if self.board[x][0] == 'W':
                # evaluation += temp_dict[self.board[x][1]]
                # else:
                # evaluation -= temp_dict[self.board[x][1]]
                evaluation += ChessBoard.eval_gen[self.board[x][0]][self.board[x][1]][x]
            return evaluation

    def get_ai_smart_move(self):
        return self.get_ai_move(4)

    def get_ai_random_move(self):
        return self.valid_move_list[randint(len(self.valid_move_list))]

    def get_human_move(self):
        while True:
            inp = input('Please choose a move: ')
            if inp.upper() in ('S', 'SB', 'SHOW', 'SHOWBOARD', 'SHOW_BOARD', 'SHOW BOARD'):
                self.show_board()
            elif inp.upper() in ('R', 'RESIGN'):
                if self.player == 'W':
                    move_chosen = 'R1'
                else:
                    move_chosen = 'R2'
                break
            else:
                move_chosen = self.convert_notation_to_move(inp)
                if move_chosen is False:
                    print('That was not a valid move!')
                else:
                    break
        return move_chosen

    def check_game_result(self):
        # ChessBoard.count_check_game_result += 1
        if self.fifty_move_count == 100:
            return '50'
        if len(self.board) < 4:
            sufficient_material = False
            for x in self.board:
                if self.board[x][1] in ('P', 'R', 'Q'):
                    sufficient_material = True
            if not sufficient_material:
                return 'IM'
        self.get_valid_moves()
        if len(self.valid_move_list) == 0:
            r = self.check_for_check()
            if r == 0:
                result = 'S'
            elif self.player == 'B':
                result = '#1'
            else:
                result = '#2'
        else:
            result = 'U'
        return result

    def play_game(self, mode='AUTO'):
        self.write_file = open('C:\\Users\\jtims\\PycharmProjects\\Chess 2\\Game_moves.txt', 'a+')
        if mode == 'AUTO':
            recorded_moves = ChessBoard.read_moves_from_file()
            self.recorded_moves = []
            for i in range(int(len(recorded_moves) / 2)):
                self.recorded_moves += [[recorded_moves[2 * i], recorded_moves[2 * i + 1]]]
            if len(recorded_moves) % 2 == 1:
                self.recorded_moves += [[recorded_moves[-1], '']]
        self.get_valid_moves()
        result = 'U'
        while result == 'U':
            if self.player == 'W':
                if self.player_type_1 == 'H':
                    move = self.get_human_move()
                elif self.player_type_1 == 'AIR':
                    move = self.get_ai_random_move()
                elif self.player_type_1 == 'AIS':
                    move = self.get_ai_smart_move()
                elif self.player_type_1 == 'AUTO':
                    if self.turn_number <= len(self.recorded_moves):
                        move = self.convert_notation_to_move(self.recorded_moves[self.turn_number - 1][0])
                    else:
                        move = self.get_human_move()
                else:
                    print('No other player type is valid. Defaulting to human player')
                    move = self.get_human_move()
                if move == 'R1':
                    result = 'R1'
                else:
                    self.previous_move = self.convert_move_to_notation(move)
                    self.perform_move(move)
                    result = self.check_game_result()
            elif self.player == 'B':
                if self.player_type_2 == 'H':
                    move = self.get_human_move()
                elif self.player_type_2 == 'AIR':
                    move = self.get_ai_random_move()
                elif self.player_type_2 == 'AIS':
                    t1 = time()
                    move = self.get_ai_smart_move()
                    print(time() - t1)
                elif self.player_type_2 == 'AUTO':
                    if self.turn_number <= len(self.recorded_moves) and self.recorded_moves[self.turn_number - 1][
                       1] != '':
                        move = self.convert_notation_to_move(self.recorded_moves[self.turn_number - 1][1])
                    else:
                        move = self.get_human_move()
                else:
                    print('No other player type is valid. Defaulting to human player')
                    move = self.get_human_move()
                if move == 'R2':
                    result = 'R2'
                else:
                    self.write_file.write(
                        f'{self.turn_number}. {self.previous_move} {self.convert_move_to_notation(move)}\n')
                    print(f'{self.turn_number}. {self.previous_move} {self.convert_move_to_notation(move)}')
                    self.perform_move(move)
                    result = self.check_game_result()
                self.turn_number += 1
        if result == 'S':
            print('The result was stalemate due to no legal moves for the current player')
        if result == 'IM':
            print('The result was stalemate due to insufficient material to checkmate')
        elif result == '50':
            print('The result was stalemate due to the fifty move rule')
        elif result == 'R1':
            print('White resigned. Black wins! 0-1')
        elif result == 'R2':
            print('Black resigned. White wins! 1-0')
            self.write_file.write(f'{self.turn_number}. {self.previous_move}\n')
        elif result == '#1':
            print('Checkmate. White wins! 1-0')
            self.write_file.write(f'{self.turn_number}. {self.previous_move}\n')
        elif result == '#2':
            print('Checkmate. Black wins! 0-1')
        self.write_file.write(result)
        self.write_file.close()


test = ChessBoard()
test.play_game()
# recorded_moves = ChessBoard.read_moves_from_file()
# srecorded_moves = []
# for i in range(int(len(recorded_moves)/2)):
#     srecorded_moves += [[recorded_moves[2*i], recorded_moves[2*i+1]]]
# if len(recorded_moves) % 2 == 1:
#     srecorded_moves += [[recorded_moves[-1], '']]
# test.animate_move_set(srecorded_moves)
# print(f'count_check_game_result {ChessBoard.count_check_game_result}')
# print(f'count_check_for_check {ChessBoard.count_check_for_check}')
# print(f'count_get_valid_moves {ChessBoard.count_get_valid_moves}')
# print(f'count_perform_move {ChessBoard.count_perform_move}')
# print(f'count_check_for_checkmate {ChessBoard.count_check_for_checkmate}')
# print(f'count_move_validation_check {ChessBoard.count_move_validation_check}')
# print(f'count_ChessBoard_initiation {ChessBoard.count_ChessBoard_initiation}')
# print(f'count_evaluate_position {ChessBoard.count_evaluate_position}')
# print(f'count_identify_one_valid_move {ChessBoard.count_identify_one_valid_move}')
