import math

import numpy as np
from scipy.signal import convolve2d

horizontal_kernel = np.array([[1, 1, 1, 1]])
vertical_kernel = horizontal_kernel.T
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


def convolve(mat, kernel):
    """
    Convolve a matrix (with no wrapping boundary) with a kernel

    Args:
        mat (ndarray): Matrix to be convolved
        kernel (ndarray): Kernel to be used for convolution

    Returns:
        ndarray: Convolved matrix
    """

    return convolve2d(mat, kernel, mode="valid")


def evaluation(state):
    """
    Evaluates "strength" of configuration

    Args:
        state (Board): board state

    Returns:
        int: evaluation of configuration
    """

    value = 0
    rewards = [np.array([0, 1, 10, 200, 10**5]), np.array([0, 1, 15, 300, 10**5])]

    for idx_mat, mat in enumerate(state.matrix_rep()):

        for idx_ker, kernel in enumerate(detection_kernels):

            line_sum = convolve(mat, kernel)

            # idx_ker<2 corresponds to the horizontal and vertical kernels
            # For which we use the rewards[0]
            if idx_ker < 2:
                reward = rewards[0]
            else:
                reward = rewards[1]

            line_sum = reward[line_sum].sum()

            if idx_mat == 0:
                value += line_sum
            else:
                value -= line_sum

    return value


def minimax(
    state,
    depth,
    alpha,
    beta,
    maximizing_player,
    hashmap={},
):
    """
    Finds optimal move for AI by running minimax with alpha beta pruning and memoization

    Args:
        state (Board): board state
        depth (int): Keeps track of recursion depth in minimax
        alpha (float): Paramater required for alpha-beta pruning
        beta (float): Paramater required for alpha-beta pruning
        maximizing_player (bool): Keep track of which player's turn it is when in the search tree
        hashmap (dict, optional): Stores configs and correspondng evaluations. Defaults to {}.

    Returns:
        int: column position of best move
    """

    if depth == 0 or state.checkwin() or not state.legalmoves():

        if state.config not in hashmap:

            hashmap[state.config] = state.evaluation()

        return None, hashmap[state.config]

    best_move = 3

    if maximizing_player:

        max_eval = -math.inf

        for child in state.legalmoves():

            current_eval = minimax(
                state + child, depth - 1, alpha, beta, False, hashmap
            )[1]

            if current_eval > max_eval:

                max_eval = current_eval
                best_move = child

            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break

        return best_move, max_eval

    else:
        min_eval = math.inf

        for child in state.legalmoves():

            current_eval = minimax(
                state + child, depth - 1, alpha, beta, True, hashmap
            )[1]

            if current_eval < min_eval:

                min_eval = current_eval
                best_move = child

            beta = min(beta, current_eval)
            if beta <= alpha:
                break

        return best_move, min_eval
