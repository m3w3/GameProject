""" This is the strategy file."""
from typing import Any, Union
import random
from games import SubtractSquareGame, ChopsticksGame

def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def current_strategy(game: Union[ChopsticksGame, SubtractSquareGame]) \
        -> Union[str, int]:
    """
    Returns a randomly selected move.
    """

    # get all legal moves, then randomly pick 1
    legal_moves = game.current_state.get_possible_moves()
    total_moves = len(legal_moves)

    return legal_moves[random.randint(0, total_moves - 1)]
