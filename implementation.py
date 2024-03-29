"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, INFINITY, NEG_INFINITY
import random

# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

STUDENT_ID = 20526389
AGENT_NAME = "Sharkbird"
COMPETE = True

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """

    score = basic_evaluate(board)

    if board.is_game_over():
      score = -1042 + board.num_tokens_on_board()

    return score

    #raise NotImplementedError


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

def alpha_beta_search_value(board, depth, eval_fn, 
                      alpha, beta,
                      get_next_moves_fn,
                      is_terminal_fn,
                      verbose=True):

    if is_terminal_fn(depth, board):
        return eval_fn(board)
    val = NEG_INFINITY
    for move, new_board in get_next_moves_fn(board):
      temp_val = -1 * alpha_beta_search_value(new_board, depth - 1, eval_fn, beta, alpha, get_next_moves_fn, is_terminal_fn)
      if temp_val > val:
        val = temp_val
      if val > alpha:
        alpha = val
      if alpha >= -beta:
        break
    return val

    #return minimax(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, verbose=True)

# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.

# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    """
     board is the current tree node.

     depth is the search depth.  If you specify depth as a very large number then your search will end at the leaves of trees.
     
     def eval_fn(board):
       a function that returns a score for a given board from the
       perspective of the state's current player.
    
     def get_next_moves(board):
       a function that takes a current node (board) and generates
       all next (move, newboard) tuples.
    
     def is_terminal_fn(depth, board):
       is a function that checks whether to statically evaluate
       a board/node (hence terminating a search branch).
    """

    return_tuple = None
    alpha = NEG_INFINITY
    beta = NEG_INFINITY
    for move, new_board in get_next_moves_fn(board):
      val = -1 * alpha_beta_search_value(new_board, depth -1, eval_fn, beta, alpha, get_next_moves_fn, is_terminal_fn)
      if alpha < val:
        alpha = val
        return_tuple = (val, move, new_board)

    print("ALPHA_BETA: Decided on column {} with rating {}".format(return_tuple[1], return_tuple[0]))

    return return_tuple[1]

    #raise NotImplementedError


# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=5, eval_fn=focused_evaluate)
    #return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)


# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

def better_evaluate(board):
    score = focused_evaluate(board);
    if board.is_game_over() == False:
      if random.random() <= 0.50:
        score += random.randrange(-1000, 1000)

    return score

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
def my_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=5)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
