"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    moves = 0
    # loop through board and see how many spaces are not empty
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                moves += 1
    # if an even number of moves have been made, it's X's turn, otherwise it's O
    return X if moves % 2 == 0 else O
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # empty set we will add all possible moves to
    actions = set()

    # go through the board, if there's an empty space, add that space to actions
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if move is invalid
    if action not in actions(board):
        raise Exception("Invalid move")
    
    # make a new board that is the same as the old board
    newboard = copy.deepcopy(board)
    # see whose turn it is and place their mark at the spot of the action
    if player(board) == X:
        newboard[action[0]][action[1]] = X
    else:
        newboard[action[0]][action[1]] = O 

    # return the new board without modifying old board
    return newboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # look if there are 3 in a row anywhere (hardcoding it because I'm lazy)
    if (board[0][0] == board[0][1] == board[0][2] != EMPTY) or \
    (board[1][0] == board[1][1] == board[1][2] != EMPTY) or \
    (board[2][0] == board[2][1] == board[2][2] != EMPTY) or \
    (board[0][0] == board[1][0] == board[2][0] != EMPTY) or \
    (board[0][1] == board[1][1] == board[2][1] != EMPTY) or \
    (board[0][2] == board[1][2] == board[2][2] != EMPTY) or \
    (board[0][0] == board[1][1] == board[2][2] != EMPTY) or \
    (board[2][0] == board[1][1] == board[0][2] != EMPTY):
        
        # this means there's a winner, check who it is
        # if it's player X's turn, that means O just went so he won, and vice versa
        if player(board) == X:
            return O
        else:
            return X
        
    # no winner
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is over if there's a winner or all 9 moves have been made
    if winner(board) == X or winner(board) == O or len(actions(board)) == 0:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the game's over, no move
    if terminal(board):
        return None
    
    # if there is a move to make, use minimax functions to return it
    _, move = maxvalue(board) if player(board) == X else minvalue(board)
    return move

def maxvalue(board):
    """
    Returns the max value of all the moves on the board (used for X)
    """
    if terminal(board):
        return utility(board), None
    v = -math.inf
    move = None
    for action in actions(board):
        max_v, _ = minvalue(result(board, action))
        if max_v > v:
            v = max_v
            move = action
    return v, move

def minvalue(board):
    """
    Returns the min value of all the moves on the board (used for O)
    """
    if terminal(board):
        return utility(board), None
    v = math.inf
    move = None
    for action in actions(board):
        min_v, _ = maxvalue(result(board, action))
        if min_v < v:
            v = min_v
            move = action
    return v, move