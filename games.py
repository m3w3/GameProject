"""This is the file containing all code relevant to games to be implemented."""
from typing import Any, List, Union
import copy


class GameCurrentState:
    """
    An extension to support game class.
    Used to keep track of the current of the game being played.
    This is the basic interface for a general game's current state, and the
    more complex current states specific to our games will be based on this.
    """
    is_p1_turn: bool

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize the current game state, and set whether p1 is moving.

        Note: This initializer is meant for internal use only;
        this is an abstract class and should not be instantiated directly.

        >>> GameCurrentState(False).is_p1_turn
        False
        >>> GameCurrentState(True).is_p1_turn
        True
        """

        self.is_p1_turn = is_p1_turn

    def __eq__(self, other: Any) -> bool:
        """
        Return whether GameCurrentState self is equivalent to other.
        >>> gcs1 = GameCurrentState(True)
        >>> gcs2 = GameCurrentState(True)
        >>> gcs3 = "GameCurrentState(True)"
        >>> gcs1 == gcs2
        True
        >>> gcs1.__eq__(gcs3)
        False
        """

        return (type(self) == type(other) and
                self.is_p1_turn == other.is_p1_turn)

    def __str__(self) -> str:
        """
        Return a user-friendly string representation of GameCurrentState.
        >>> print(GameCurrentState(False))
        p2's turn to move.
        >>> print(GameCurrentState(True))
        p1's turn to move.
        """

        return "{}'s turn to move.".format(
            self.get_current_player_name())

    def get_possible_moves(self) -> Union[List[str], List[int]]:
        """
        Return a list of possible moves, given the current game state.
        """

        raise NotImplementedError

    def is_valid_move(self, move_to_make: Union[int, str]) -> bool:
        """
        Return whether move_to_make is legal given the current game state.
        """

        raise NotImplementedError

    def get_current_player_name(self) -> str:
        """
        Return the name of the current player making a move.
        Either 'p1' or 'p2'.
        >>> GameCurrentState(True).get_current_player_name()
        'p1'
        >>> GameCurrentState(False).get_current_player_name()
        'p2'
        """

        if self.is_p1_turn:
            p = 'p1'
        else:
            p = 'p2'

        return p

    def make_move(self, move_to_make: Union[int, str]) -> Any:
        """
        The current value is changed according to move_to_make.
        """
        # change player turn (since the game is sequential)

        raise NotImplementedError


class SSGameCurrentState(GameCurrentState):
    """
    Keeps track of the game subtract square being played.
    """
    is_p1_turn: bool
    current_val: int
    possible_moves_list: List[int]

    def __init__(self, is_p1_turn: bool, current_val: Union[str, int]) -> None:
        """
        Initialize the current game state, and set whether p1 is moving, and
        the current value of the game.
        >>> SSGameCurrentState(True, 0).current_val
        0
        >>> SSGameCurrentState(True, 0).possible_moves_list
        []
        >>> SSGameCurrentState(False, 2).is_p1_turn
        False
        """
        GameCurrentState.__init__(self, is_p1_turn)
        self.is_p1_turn = is_p1_turn
        self.current_val = int(current_val)

        # Make a list to keep track of the possible moves
        self.possible_moves_list = self.get_possible_moves()

    def __eq__(self, other: Any) -> bool:
        """
        Return whether SSGameCurrentState self is equivalent to other.
        >>> gcs1 = SSGameCurrentState(True, 10)
        >>> gcs2 = SSGameCurrentState(True, 10)
        >>> gcs3 = "SSGameCurrentState(True, 10)"
        >>> gcs1 == gcs2
        True
        >>> gcs1.__eq__(gcs3)
        False
        >>> gcs2.possible_moves_list = []
        >>> gcs1 == gcs2
        False
        """

        return (type(self) == type(other) and
                self.is_p1_turn == other.is_p1_turn and
                self.current_val == other.current_val and
                self.possible_moves_list == other.possible_moves_list)

    def __str__(self) -> str:
        """
        Return a user-friendly string representation of SSGameCurrentState.
        >>> print(SSGameCurrentState(False, 1))
        p2's turn to move; the current value is 1.
        >>> print(SSGameCurrentState(True, 0))
        p1's turn to move; the current value is 0.
        """

        return ("{}'s turn to move; the current value is {}.".
                format(self.get_current_player_name(), str(self.current_val)))

    def get_possible_moves(self) -> List[int]:
        """
        Return a list of possible moves, given the current game state.
        >>> SSGameCurrentState(False, 0).get_possible_moves()
        []
        >>> SSGameCurrentState(False, 1).get_possible_moves()
        [1]
        >>> SSGameCurrentState(False, 103).get_possible_moves()
        [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        """

        i = 1
        possible_moves = []
        while i*i <= self.current_val:
            possible_moves.append(i*i)
            i += 1

        # no need to sort this list since it's appended increasingly
        return possible_moves

    def is_valid_move(self, move_to_make: int) -> bool:
        """
        Return whether move_to_make is legal given the current game state.
        >>> SSGameCurrentState(False, 1).is_valid_move(1)
        True
        >>> SSGameCurrentState(True, 0).is_valid_move(0)
        False
        >>> SSGameCurrentState(True, 10000).is_valid_move(100)
        True
        """

        return move_to_make in self.possible_moves_list

    def make_move(self, move_to_make: int) -> Any:
        """
        The current value is changed according to move_to_make.
        >>> won = SSGameCurrentState(False, 1).make_move(1)
        >>> won.get_possible_moves()
        []
        >>> state = SSGameCurrentState(True, 100).make_move(64)
        >>> state.get_possible_moves()
        [1, 4, 9, 16, 25, 36]
        """

        copied = copy.deepcopy(self)

        # change player turn (since the game is sequential)
        copied.is_p1_turn = not copied.is_p1_turn

        # change the current value of the subtract square
        copied.current_val -= move_to_make

        # "refresh" the possible moves list for the other player
        copied.possible_moves_list = copied.get_possible_moves()

        return copied


class CSGameCurrentState(GameCurrentState):
    """
    Keeps track of the game chopsticks being played.
    """
    is_p1_turn: bool
    current_val: List[int]
    possible_moves_list: List[str]

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize the current game state, and set whether p1 is moving.
        Both players start with 1-1.
        >>> CSGameCurrentState(True).current_value
        [1, 1, 1, 1]
        >>> CSGameCurrentState(True).possible_moves_p1
        ['ll', 'lr', 'rl', 'rr']
        >>> CSGameCurrentState(False).is_p1_turn
        False
        """
        self.is_p1_turn = is_p1_turn

        # both players start with 1 on both hands
        self.current_value = [1, 1, 1, 1]

        # Make lists to keep track of the possible moves
        self.possible_moves_p1 = ["ll", "lr", "rl", "rr"]
        self.possible_moves_p2 = ["ll", "lr", "rl", "rr"]

    def __eq__(self, other: Any) -> bool:
        """
        Return whether CSGameCurrentState self is equivalent to other.
        >>> gcs1 = CSGameCurrentState(True)
        >>> gcs2 = CSGameCurrentState(True)
        >>> gcs3 = SSGameCurrentState(True, 20)
        >>> gcs1 == gcs2
        True
        >>> gcs1.__eq__(gcs3)
        False
        """

        return (type(self) == type(other) and
                self.is_p1_turn == other.is_p1_turn and
                self.current_value == other.current_value and
                sorted(self.possible_moves_p1)
                == sorted(other.possible_moves_p1) and
                sorted(self.possible_moves_p2)
                == sorted(other.possible_moves_p2))

    def __str__(self) -> str:
        """
        Return a user-friendly string representation of CSGameCurrentState.
        >>> print(CSGameCurrentState(False))
        Player 1: 1-1; Player 2 [Current]: 1-1
        """

        # values of each hand
        p1_l = self.current_value[0]
        p1_r = self.current_value[1]
        p2_l = self.current_value[2]
        p2_r = self.current_value[3]

        if self.is_p1_turn:
            return ("Player 1 [Current]: {}-{}; Player 2: {}-{}"
                    .format(p1_l, p1_r, p2_l, p2_r))
        return ("Player 1: {}-{}; Player 2 [Current]: {}-{}"
                    .format(p1_l, p1_r, p2_l, p2_r))

    def get_possible_moves(self) -> List[str]:
        """
        Return a list of possible moves, given the current game state.
        >>> CSGameCurrentState(False).get_possible_moves()
        ['ll', 'lr', 'rl', 'rr']
        """

        # value of each hand
        p1_l = self.current_value[0]
        p1_r = self.current_value[1]
        p2_l = self.current_value[2]
        p2_r = self.current_value[3]

        if self.get_current_player_name() == 'p1':
            if p1_l != 0 and p1_r != 0:
                if p2_l != 0 and p2_r != 0:
                    moves = ["ll", "lr", "rl", "rr"]
                elif p2_l == 0 and p2_r != 0:
                    moves = ["lr", "rr"]
                else:
                    moves = ["ll", "rl"]
            elif p1_l == 0 and p1_r != 0:
                if p2_l != 0 and p2_r != 0:
                    moves = ["rl", "rr"]
                elif p2_l == 0 and p2_r != 0:
                    moves = ["rr"]
                else:
                    moves = ["rl"]
            elif p1_l != 0 and p1_r == 0:
                if p2_l != 0 and p2_r != 0:
                    moves = ["ll", "lr"]
                elif p2_l == 0 and p2_r != 0:
                    moves = ["lr"]
                else:
                    moves = ["ll"]
            else:
                moves = []
        else:
            if p2_l != 0 and p2_r != 0:
                if p1_l != 0 and p1_r != 0:
                    moves = ["ll", "lr", "rl", "rr"]
                elif p1_l == 0 and p1_r != 0:
                    moves = ["lr", "rr"]
                else:
                    moves = ["ll", "rl"]
            elif p2_l == 0 and p2_r != 0:
                if p1_l != 0 and p1_r != 0:
                    moves = ["rl", "rr"]
                elif p1_l == 0 and p1_r != 0:
                    moves = ["rr"]
                else:
                    moves = ["rl"]
            elif p2_l != 0 and p2_r == 0:
                if p1_l != 0 and p1_r != 0:
                    moves = ["ll", "lr"]
                elif p1_l == 0 and p1_r != 0:
                    moves = ["lr"]
                else:
                    moves = ["ll"]
            else:
                moves = []

        return moves

    def is_valid_move(self, move_to_make: str) -> bool:
        """
        Return whether move_to_make is legal given the current game state.
        >>> CSGameCurrentState(False).is_valid_move("rl")
        True
        >>> CSGameCurrentState(True).is_valid_move("derp")
        False
        """

        return move_to_make in self.get_possible_moves()

    def make_move(self, move_to_make: str) -> Any:
        """
        The current value is changed according to move_to_make.
        >>> won = CSGameCurrentState(True).make_move("ll")
        >>> print(won)
        Player 1: 1-1; Player 2 [Current]: 2-1
        """

        copied = copy.deepcopy(self)
        # values of each hand
        p1_l = copied.current_value[0]
        p1_r = copied.current_value[1]
        p2_l = copied.current_value[2]
        p2_r = copied.current_value[3]

        # change the current positions of opposing player
        if copied.get_current_player_name() == 'p1':
            if move_to_make == "ll":
                # assign p2_1
                copied.current_value = [p1_l, p1_r, (p1_l + p2_l) % 5, p2_r]
            elif move_to_make == "lr":
                # assign p2_r
                copied.current_value = [p1_l, p1_r, p2_l, (p1_l + p2_r) % 5]
            elif move_to_make == "rl":
                # assign p2_1
                copied.current_value = [p1_l, p1_r, (p1_r + p2_l) % 5, p2_r]
            else:
                # assign p2_r
                copied.current_value = [p1_l, p1_r, p2_l, (p1_r + p2_r) % 5]
        else:
            if move_to_make == "ll":
                # assign p1_1
                copied.current_value = [(p2_l + p1_l) % 5, p1_r, p2_l, p2_r]
            elif move_to_make == "lr":
                # assign p1_r
                copied.current_value = [p1_l, (p2_l + p1_r) % 5, p2_l, p2_r]
            elif move_to_make == "rl":
                # assign p1_1
                copied.current_value = [(p2_r + p1_l) % 5, p1_r, p2_l, p2_r]
            else:
                # assign p1_r
                copied.current_value = [p1_l, (p2_r + p1_r) % 5, p2_l, p2_r]

        # change player's turn (since the game is sequential)
        copied.is_p1_turn = not copied.is_p1_turn

        # "refresh" the possible moves list
        if copied.get_current_player_name() == 'p1':
            copied.possible_moves_p1 = copied.get_possible_moves()
        else:
            copied.possible_moves_p2 = copied.get_possible_moves()

        return copied


class Game:
    """
     A general 2-player game with the following characteristics:
        1) Sequential-move
        2) Zero-sum
        3) Perfect-information
     """
    is_pl_turn: bool

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize the game; set which player (1 or 2) should move first.

        Note: This initializer is meant for internal use only;
        this is an abstract class and should not be instantiated directly.

        >>> ABC = Game(True)
        >>> ABC.is_p1_turn
        True
        """

        self.is_p1_turn = is_p1_turn

    def __eq__(self, other: Any) -> bool:
        """
        Return whether Game self is equivalent to other.
        >>> game1 = Game(True)
        >>> game2 = Game(True)
        >>> game3 = "Game(True)"
        >>> game1 == game2
        True
        >>> game2.__eq__(game3)
        False
        """

        return (type(self) == type(other) and
                self.is_p1_turn == other.is_p1_turn)

    def __str__(self) -> str:
        """
        Return a user-friendly string representation of Game.
        >>> print(Game(False))
        This is a general game, and it's p2's turn to move.
        >>> print(Game(True))
        This is a general game, and it's p1's turn to move.
        """

        if self.is_p1_turn:
            player = 'p1'
        else:
            player = 'p2'

        return "This is a general game, and it's {}'s turn to move.".format(
            player)

    def get_instructions(self) -> str:
        """
        Provides instructions for the current game being played.
        """

        raise NotImplementedError

    def is_over(self, current_s: Union[SSGameCurrentState,
                                       CSGameCurrentState]) -> bool:
        """
        Check if the game is over given the current_s.
        >>> ChopsticksGame(True).is_over(CSGameCurrentState(False))
        False
        >>> ChopsticksGame(True).is_over(CSGameCurrentState(False))
        False
        """

        return current_s.get_possible_moves() == []

    def is_winner(self, current_player: str) -> bool:
        """
        Return whether current_player has won.
        """

        raise NotImplementedError

    def str_to_move(self, move: str) -> Union[int, str]:
        """
        Converts the string value and returns a move for the game.
        """

        raise NotImplementedError


class SubtractSquareGame(Game):
    """
    A 2-player sequential game known as subtract square.
    The last player to choose 1 loses; use .get_instructions() for more info.
    """
    is_p1_turn: bool
    current_state: SSGameCurrentState
    Game_Description_SS: str

    # SubtractSquareGame's description is a constant, so place it here
    Game_Description_SS = (
        "A non-negative whole number is chosen as the starting value. "
        "The player whose turn it is, chooses some the of any postive "
        "natural number to subtract from the value. Note that the "
        "number chosen cannot be larger than the value. After "
        "subtracting, there's a new value, which the next player will "
        "choose a square and subtract from. The play continues to "
        "alternate between the two players until no movees are "
        "possible. Whoever is about to play at that point loses!")

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize the subtract square game;
        set which player (1 or 2) should move first.
        """

        self.is_p1_turn = is_p1_turn
        starting_num = self.initial_input()
        self.current_state = SSGameCurrentState(self.is_p1_turn, starting_num)

    def __eq__(self, other: Any) -> bool:
        """
        Return whether SubtractSquareGame self is equivalent to other.
        """

        return (type(self) == type(other) and
                self.is_p1_turn == other.is_p1_turn and
                self.current_state == other.current_state)

    def __str__(self) -> str:
        """
        Return a user-friendly string representation of SubtractSquareGame.
        """

        if self.is_p1_turn:
            player = 'p1'
        else:
            player = 'p2'

        return ("This is a subtract square game, "
                "and it's {}'s turn to move.".format(player))

    def get_instructions(self) -> str:
        """
        Provides the instruction for subtract square.
        """

        return self.Game_Description_SS

    def is_winner(self, current_player: str) -> bool:
        """
        Return whether current_player has won.
        Expects either "p1" or "p2" as input.
        """

        # check which player's turn it is
        if self.current_state.is_p1_turn:
            current_player_playing = "p1"
        else:
            current_player_playing = "p2"

        # check if there are any available moves
        if self.current_state.possible_moves_list == []:
            # check if the player with no moves isn't current player
            if current_player != current_player_playing:
                return True

        return False

    def str_to_move(self, move: str) -> Union[int, str]:
        """
        Converts the string value and returns a move for the game.
        """
        # convert the move to int typing if game is subtract square
        return int(move)

    def initial_input(self) -> str:
        """
        Request the player for a starting input to initialize the game.
        ***Note: if the player selects 0, they automatically lose, with
        the reason being that the player whose turn it is
        when the state has a value of 0 is the loser.***
        """

        # warn the player if they start with 0, this is auto-lose!
        starting_num = input("Choose the starting value "
                             "(if you choose 0, you lose!): ")

        return starting_num


class ChopsticksGame(Game):
    """
    A 2-player sequential game known as chopsticks.
    The player with 2 "dead" hands loses;
    use .get_instructions() for more info.
    """
    is_p1_turn: bool
    current_state: CSGameCurrentState
    Game_Description_CS: str

    # Chopsticks' description is a constant, so place it here
    Game_Description_CS = (
        "Each of 2 players begins with one finger pointed up "
        "on each of their hands. Player 1 touches one hand of "
        "player 2's hands, increasing the number of fingers "
        "pointing up on player 2's hands by the number on "
        "player 1's hand. Note that the number pointing up on "
        "player 1's hand remains the same. If player 2 now has 5 "
        "fingers up, that hand is unplayable. If the number of "
        "fingers should exceed five, subtract 5 from the sum. "
        "Keep playing until a player has two unplayable hands, "
        "thus losing.")

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize the chopsticks game;
        set which player (1 or 2) should move first.
        >>> ChopsticksGame(True).is_p1_turn
        True
        >>> print(ChopsticksGame(False).current_state)
        Player 1: 1-1; Player 2 [Current]: 1-1
        """

        self.is_p1_turn = is_p1_turn
        self.current_state = CSGameCurrentState(self.is_p1_turn)

    def __eq__(self, other: Any) -> bool:
        """
        Return whether ChopsticksGame self is equivalent to other.
        >>> ChopsticksGame(True) == ChopsticksGame(True)
        True
        """

        return (type(self) == type(other) and
                self.is_p1_turn == other.is_p1_turn and
                self.current_state == other.current_state)

    def __str__(self) -> str:
        """
        Return a user-friendly string representation of ChopsticksGame.
        >>> print(ChopsticksGame(True))
        This is a chopsticks game, and it's p1's turn to move.
        >>> print(ChopsticksGame(False))
        This is a chopsticks game, and it's p2's turn to move.
        """

        if self.is_p1_turn:
            player = 'p1'
        else:
            player = 'p2'

        return ("This is a chopsticks game, "
                "and it's {}'s turn to move.".format(player))

    def get_instructions(self) -> str:
        """
        Provides the instruction for subtract square.
        """
        return self.Game_Description_CS

    def is_winner(self, current_player: str) -> bool:
        """
        Return whether current_player has won.
        Expects either "p1" or "p2" as input.
        >>> ChopsticksGame(True).is_winner('p1')
        False
        """

        # check which player's turn it is
        if self.current_state.is_p1_turn:
            current_player_playing = "p1"
        else:
            current_player_playing = "p2"

        # check if there are any available moves
        if self.current_state.get_possible_moves() == []:
            # check if the player with no moves isn't current player
            if current_player != current_player_playing:
                return True

        return False

    def str_to_move(self, move: str) -> str:
        """
        Ensures the move entered is "ll", "lr", "rl", or "rr".
        Remove any possible illegal characters.
        >>> ChopsticksGame(True).str_to_move("l -r")
        'lr'
        >>> ChopsticksGame(False).str_to_move("rr")
        'rr'
        """

        unwanted = [" ", "-", "_", "+", "/"]
        new_move = ""

        for char in move:
            if char in unwanted:
                pass
            else:
                new_move += char

        return new_move


if __name__ == '__main__':
    import doctest
    doctest.testmod()
