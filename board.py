import math
from itertools import product

import engine
import numpy as np
from engine import convolve, detection_kernels

dictionary = dict()


class Board:
    """Class storing connect4 board state"""

    def __init__(self, config=""):
        self.config = config

    def __iter__(self):
        return product(range(7), range(6))

    def __add__(self, move):
        return Board(self.config + str(move))

    def matrix_rep(self):
        """
        Returns matrix representation of current configuration.

        Returns:
            Board:  Matrices representation of Board
        """

        mat = np.zeros((6, 7), dtype=int)
        run = True

        for i in self.config:
            k = int(i)

            if run:
                mat[np.count_nonzero(mat[:, k]), k] = 1

            else:
                mat[np.count_nonzero(mat[:, k]), k] = 2

            run = not run

        return (mat == 1) * 1, (mat == 2) * 1

    def legalmoves(self):
        """
        Return the set of legal moves allowed

        Returns:
            list: list of moves that can be played
        """

        return [move for move in range(7) if (self.config).count(str(move)) < 6]

    def checkwin(self):
        """
        Check whether any player has won or lost.

        Returns:
            bool: True if gameover, else False
        """

        mat1, mat2 = self.matrix_rep()

        for kernel in detection_kernels:

            if (4 in convolve(mat1, kernel)) or (4 in convolve(mat2, kernel)):

                return True

        return False

    def checkwin_player(self):
        """
        Check which Player has won.

        Returns:
            string: "Player1" if human has won, else "Player2"
        """

        mat1, mat2 = self.matrix_rep()

        for kernel in detection_kernels:

            if 4 in convolve(mat1, kernel):
                return "Player1"

            if 4 in convolve(mat2, kernel):
                return "Player2"

    def checkwin_move(self):
        """
        Check which win has led to the win "ROW", "COLUMN", "LEFTDIAG", "RIGHTDIAG"

        Returns:
            str: winning move orientation
            int: column of winning move
        """

        position = ["ROW", "COLUMN", "LEFTDIAG", "RIGHTDIAG"]

        for mat in self.matrix_rep():

            for idx, kernel in enumerate(detection_kernels):

                line_sum = convolve(mat, kernel)

                if 4 in line_sum:

                    if idx != 3:

                        return position[idx], [i[0] for i in np.where(line_sum.T == 4)]

                    else:

                        indices = [i[0] for i in np.where(np.fliplr(sum.T) == 4)]
                        return position[idx], [indices[0], 6 - indices[1]]

        return None, None

    def test(self):
        """
        Prepare Board in a test state
        """
        self.config = "334543331204154554511636660400566100122"

    def evaluation(self):
        """
        Evaluates "strength" of configuration

        Returns:
            int: evaluation of configuration
        """
        return engine.evaluation(self)

    def engine_move(self):
        """
        Output the ideal next move

        Returns:
            int: column position of best move
        """
        player_bool = len(self.config) % 2 == 0

        for child in self.legalmoves():

            if (self + child).checkwin():

                return child

        return engine.minimax(self, 5, -math.inf, math.inf, player_bool, dictionary)[0]
