# author Vincent Kubala; GameUI implementation by Eli Zucker

###############################################################################
# State and Action Representations:
#
# - A (game) state is a TTTState that contains game board and the index of the
#   player to move
#
# - An action is a pair that represents the location at which a player
#   would like to draw an X or an O: (<index of row>, <index of column>),
#   where the indices start at 0.
#
# - See the main function at the bottom of this file for an example.
#
###############################################################################


from typing import Tuple, List, Set, Union, Optional
from adversarial_search_problem import AdversarialSearchProblem, GameState, GameUI
import time

SPACE = " "
X = "X"  # Player 0 is X
O = "O"  # Player 1 is O
PLAYER_SYMBOLS = [X, O]


class TTTState(GameState):
    def __init__(self, board: List[List[str]], ptm: int) -> None:
        """
        Initialize a tic-tac-toe game state.
        
        Args:
            board: 2D list of character strings representing the game board.
                  Each character is X, O, or SPACE, where SPACE indicates
                  an empty cell on the tic-tac-toe board.
            ptm: Index of the player to move (0 for X player, 1 for O player)
        """
        self.board = board
        self.ptm = ptm

    def player_to_move(self) -> int:
        """
        Returns the index of the player who will move next.
        
        Returns:
            0 for X player, 1 for O player
        """
        return self.ptm


# In TTT, an action consists of placing a piece on a 2D grid. Thus, our actions need two pieces of
# data: both row and column. So the type of our action is tuple with two ints.
Action = Tuple[int, int]


class TTTProblem(AdversarialSearchProblem[TTTState, Action]):
    def __init__(self, dim: int = 3, board: Optional[List[List[str]]] = None, player_to_move: int = 0) -> None:
        """
        Initialize a tic-tac-toe problem instance.
        
        Args:
            dim: The number of cells in one row or column
            board: Optional 2D list of character strings (as in TTTState)
            player_to_move: Index of player to move (0 for X, 1 for O)
        
        The board and player_to_move together constitute the start state of the game.
        """
        if board:
            assert (len(board) == len(board[0]) == dim)
        self._dim = dim
        if board == None:
            board = [[SPACE for _ in range(dim)] for _ in range(dim)]
        self._start_state = TTTState(board, player_to_move)

    def get_available_actions(self, state: TTTState) -> Set[Action]:
        """
        Get all available actions (empty spaces) for the current state.
        
        Args:
            state: The current game state
            
        Returns:
            Set of available actions as (row, column) tuples
        """
        actions = set()
        for r in range(self._dim):
            for c in range(self._dim):
                if state.board[r][c] == " ":
                    actions.add((r, c))
        return actions

    def transition(self, state: TTTState, action: Action) -> TTTState:
        """
        Apply an action to the current state and return the resulting state.
        
        Args:
            state: The current game state
            action: The action to take as (row, column) tuple
            
        Returns:
            New TTTState after applying the action
        """
        assert not (self.is_terminal_state(state))
        assert action in self.get_available_actions(state)

        # make deep copy of board
        board = [[elt for elt in row] for row in state.board]

        board[action[0]][action[1]] = PLAYER_SYMBOLS[state.ptm]
        return TTTState(board, 1 - state.ptm)

    def is_terminal_state(self, state: TTTState) -> bool:
        """
        Check if the given state is a terminal state.
        
        Args:
            state: The game state to check
            
        Returns:
            True if the state is terminal, False otherwise
        """
        return not (self._internal_evaluate_terminal(state) == "non-terminal")

    def get_result(self, state: TTTState) -> Union[int, float]:
        """
        Get the result value for a terminal state.
        
        Args:
            state: The terminal state to evaluate
            
        Returns:
            Positive infinity if X wins, negative infinity if O wins, 0 for draw
            
        Raises:
            ValueError: If the state is not terminal
        """
        internal_val = self._internal_evaluate_terminal(state)
        if internal_val == "non-terminal":
            raise ValueError("attempting to evaluate a non-terminal state")
        else:
            return internal_val

    def _internal_evaluate_terminal(self, state: TTTState) -> Union[int, float]:
        """
        If state is terminal, returns its evaluation;
        otherwise, returns 'non-terminal'.
        """
        board = state.board

        diagonal1 = [board[i][i] for i in range(self._dim)]
        # bind the output of _all_same for diagonal1 for its two uses
        asd1 = TTTProblem._all_same(diagonal1)
        if asd1:  # #onlyinpython / #imissoptions
            return asd1

        diagonal2 = [board[i][self._dim - 1 - i] for i in range(self._dim)]
        asd2 = TTTProblem._all_same(diagonal2)
        if asd2:
            return asd2

        for row in board:
            asr = TTTProblem._all_same(row)
            if asr:
                return asr

        for c in range(self._dim):
            # why oh why didn't I just use numpy arrays?
            col = [board[r][c] for r in range(self._dim)]
            asc = TTTProblem._all_same(col)
            if asc:
                return asc

        if self.get_available_actions(state) == set():
            # all spaces are filled up
            return 0
        else:
            return "non-terminal"

    @staticmethod
    def _all_same(cell_list: List[str]) -> Union[bool, float]:
        """
        Given a list of cell contents, e.g. ['x', ' ', 'X'],
        returns [1.0, 0.0] if they're all X, [0.0, 1.0] if they're all O,
        and False otherwise.
        """
        xlist = [cell == X for cell in cell_list]
        if all(xlist):
            return float('inf')

        olist = [cell == O for cell in cell_list]
        if all(olist):
            return float('-inf')

        return False

    @staticmethod
    def board_to_pretty_string(board: List[List[str]]) -> str:
        """
        Takes in a tile game board and outputs a pretty string representation
        of it for printing.
        """
        hbar = "-"
        vbar = "|"
        corner = "+"
        dim = len(board)

        s = corner
        for _ in range(2 * dim - 1):
            s += hbar
        s += corner + "\n"

        for r in range(dim):
            s += vbar
            for c in range(dim):
                s += str(board[r][c]) + " "
            s = s[:-1]
            s += vbar
            s += "\n"

        s += corner
        for _ in range(2 * dim - 1):
            s += hbar
        s += corner
        return s


# Basic TTT GameUI implementation (prints board states to console)
class TTTUI(GameUI):
    def __init__(self, asp: TTTProblem, delay: float = 0.2) -> None:
        """
        Initialize the tic-tac-toe user interface.
        
        Args:
            asp: The TTTProblem instance to interface with
            delay: Delay in seconds between renders
        """
        self._asp = asp
        self._delay = delay
        self._state = TTTState(
            [[SPACE for _ in range(asp._dim)] for _ in range(asp._dim)], 0
        )  # empty state

    def render(self) -> None:
        """
        Render the current game state to the console.
        """
        print(TTTProblem.board_to_pretty_string(self._state.board))
        time.sleep(self._delay)

    def get_user_input_action(self) -> Action:
        """
        Get user input for the next action.
        
        Returns:
            Action tuple (row, column) obtained from user input
        """
        user_action = None
        available_actions = self._asp.get_available_actions(self._state)

        while not user_action in available_actions:
            row = int(input("Enter row index: "))
            col = int(input("Enter column index: "))
            user_action = (row, col)

        return user_action


def main() -> None:
    """
    Provides an example of the TTTProblem class being used.
    """
    t = TTTProblem()
    # A state in which an X is in the center cell, and O moves next.
    s0 = TTTState([[" ", " ", " "], [" ", "X", " "], [" ", " ", " "]], 1)
    # The O player puts down an O at the top-left corner, and now X moves next
    s1 = t.transition(s0, (0, 0))
    assert s1.board == [["O", " ", " "], [" ", "X", " "], [" ", " ", " "]]
    assert s1.ptm == 0


if __name__ == "__main__":
    main()