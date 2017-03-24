"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
from typing import Tuple, List, Callable
from itertools import chain
from isolation import Board

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game: Board, player) -> float:
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    def get_moves_1_ahead(game, player):
        moves = game.get_legal_moves(player)
        more_moves = chain(*map(lambda m: game.__get_moves__(m), moves))
        #more_moves = chain(*map(lambda m: game.__get_moves__(m), more_moves))
        more_moves = set(more_moves)
        return more_moves

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)
    my_moves = get_moves_1_ahead(game, player)
    opponent_moves = get_moves_1_ahead(game, opponent)

    div = float(len(opponent_moves)) #if my_moves & opponent_moves else 1.0
    return float("inf") if div == 0 else (len(my_moves)) / div


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.method_fn = self.alphabeta if method == "alphabeta" else self.minimax
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        best_score, best_move = float("-inf"), (-1, -1)
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            depth = 1 if self.iterative else self.search_depth
            duration = 0
            while legal_moves and time_left() > self.TIMER_THRESHOLD:
                if duration < time_left() and time_left() > self.TIMER_THRESHOLD:
                    duration = time_left()
                    score, move = self.method_fn(game, depth, time_left)
                    duration -= time_left()
                    # if (score, move) != (best_score, best_move):
                    #     print("Move changed: ", depth, score, move)
                    best_score, best_move = score, move

                if not self.iterative or depth == self.search_depth:
                    break

                depth += 1

        except Timeout:
            # Handle any actions required at timeout, if necessary
            # print("Timeout!! ", time_left())
            pass

        # print("Move chosen: ", depth, best_score, best_move, time_left())
        return best_move

    def minimax(self, game: Board, depth: int,
                time_left: Callable) -> Tuple[float, Tuple[int, int]]:
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        def max_play(g: Board, d: int) -> Tuple[float, Tuple[int, int]]:
            moves = g.get_legal_moves()
            best_score, best_move = float("-inf"), (-1, -1)
            for move in moves:
                if time_left() < self.TIMER_THRESHOLD:
                    raise Timeout()
                new_game = g.forecast_move(move)
                if d == 1:
                    score = self.score(new_game, self)
                else:
                    score, _ = min_play(new_game, d - 1)
                best_score, best_move = max([(best_score, best_move), (score, move)])
            return best_score, best_move

        def min_play(g: Board, d: int) -> Tuple[float, Tuple[int, int]]:
            moves = g.get_legal_moves()
            best_score, best_move = float("inf"), (-1, -1)
            for move in moves:
                if time_left() < self.TIMER_THRESHOLD:
                    raise Timeout()
                new_game = g.forecast_move(move)
                if d == 1:
                    score = self.score(new_game, self)
                else:
                    score, _ = max_play(new_game, d - 1)
                best_score, best_move = min([(best_score, best_move), (score, move)])
            return best_score, best_move

        return max_play(game, depth)

    def alphabeta(self, game, depth, time_left: Callable,
                  alpha=float("-inf"), beta=float("inf")) -> Tuple[float, Tuple[int, int]]:
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        def moves_by_rank(g: Board, reverse=False) -> List[Tuple[float, Tuple[int, int]]]:
            moves = g.get_legal_moves()
            moves_w_r = sorted(map(lambda m: (0.0 + len(g.__get_moves__(m)), m), moves), reverse=reverse)
            return moves_w_r

        def max_play(g: Board, d: int, a: float, b: float) -> Tuple[float, Tuple[int, int]]:
            moves = moves_by_rank(g, reverse=True)
            best_score, best_move = float("-inf"), (-1, -1)
            for _, move in moves:
                if time_left() < self.TIMER_THRESHOLD:
                    raise Timeout()
                if best_score >= b:
                    break
                else:
                    new_game = g.forecast_move(move)
                    if d == 1:
                        score = self.score(new_game, self)
                    else:
                        score, _ = min_play(new_game, d - 1, max(best_score, a), b)
                best_score, best_move = max([(best_score, best_move), (score, move)])
            return best_score, best_move

        def min_play(g: Board, d: int, a: float, b: float) -> Tuple[float, Tuple[int, int]]:
            moves = moves_by_rank(g, reverse=False)
            best_score, best_move = float("inf"), (-1, -1)
            for _, move in moves:
                if time_left() < self.TIMER_THRESHOLD:
                    raise Timeout()
                if best_score <= a:
                    break
                else:
                    new_game = g.forecast_move(move)
                    if d == 1:
                        score = self.score(new_game, self)
                    else:
                        score, _ = max_play(new_game, d - 1, a, min(best_score, b))
                best_score, best_move = min([(best_score, best_move), (score, move)])
            return best_score, best_move

        return max_play(game, depth, alpha, beta)
