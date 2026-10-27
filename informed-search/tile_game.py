from typing import Tuple, Optional, Dict, List, Set
from search_problem import SearchProblem
from heuristic_search_problem import HeuristicSearchProblem

import itertools
import random

# The tile game search problem, implemented as a SearchProblem
# States are board configurations.
# Read the assignment handout for details.


class TileGameState:
    """
    Represents a specific position within the tile game and implements hashable behavior.

    Attributes:
        board (Tuple[Tuple[int]]): The board of numbers that make up the tile game.
    """

    def __init__(self, board: Tuple[Tuple[int]]) -> None:
        self.board = board

    def __eq__(self, other) -> bool:
        if not isinstance(other, TileGameState):
            return False
        return self.board == other.board

    def __hash__(self) -> int:
        return hash(self.board)

    def __lt__(self, other) -> bool:
        if not isinstance(other, TileGameState):
            return NotImplemented
        return self.board < other.board

    def __le__(self, other) -> bool:
        if not isinstance(other, TileGameState):
            return NotImplemented
        return self.board <= other.board

    def __gt__(self, other) -> bool:
        if not isinstance(other, TileGameState):
            return NotImplemented
        return self.board > other.board

    def __ge__(self, other) -> bool:
        if not isinstance(other, TileGameState):
            return NotImplemented
        return self.board >= other.board

    def __repr__(self) -> str:
        return f"State({self.board})"


class TileGame(SearchProblem[TileGameState]):
    """
    TileGame represents the sliding tile puzzle game as a search problem. 
    It defines the board's dimensions, start state, and goal state.
    """

    def __init__(
        self,
        dim: int,
        start: Optional[TileGameState] = None,
        goal: Optional[TileGameState] = None,
    ) -> None:
        """
        Initializes the TileGame with a specified dimension, start state, and goal state.

        Args:
            dim (int): The dimension of the game board (dim x dim).
            start (Optional[TileGameState]): The initial state of the game, if provided.
            goal (Optional[TileGameState]): The goal state of the game, if provided.
        """
        self.dim = dim

        if start:
            self.start_state = start
        else:
            self.start_state = self.random_start(dim)

        if goal:
            self.goal_state = goal
        else:
            self.goal_state = self.construct_goal()

    ###### SEARCH PROBLEM IMPLEMENTATION ######
    ###### DO NOT CHANGE THESE FUNCTIONS ######

    def get_start_state(self) -> TileGameState:
        """
        Returns the start state of the game.

        Returns:
            TileGameState: The initial state of the game board.
        """
        return self.start_state

    def is_goal_state(self, state: TileGameState) -> bool:
        """
        Checks if a given state is the goal state.

        Args:
            state (TileGameState): The state to be checked.

        Returns:
            bool: True if the state is the goal state, False otherwise.
        """
        return state == self.goal_state

    def get_successors(self, state: TileGameState) -> Set[TileGameState]:
        """
        Generates all successor states from the current state.

        Args:
            state (TileGameState): The current state of the board.

        Returns:
            Set[TileGameState]: A set of successor states.
        """
        successors = []
        for r in range(self.dim):
            for c in range(self.dim):
                if r < self.dim - 1:
                    successors.append(self.swap_tiles(state, r, c, r + 1, c))
                if c < self.dim - 1:
                    successors.append(self.swap_tiles(state, r, c, r, c + 1))
                    
        return set(successors)

    ###### INTERNAL HELPER FUNCTIONS ######
    ###### DO NOT CHANGE THESE FUNCTIONS ######

    def construct_goal(self) -> TileGameState:
        """
        Constructs the goal state based on the board's dimension.

        Returns:
            TileGameState: The goal state of the game.
        """
        dim = self.dim
        goal_board = tuple(tuple(j+1 for j in range(dim * i, dim * (i+1)))
                           for i in range(0, dim))
        return TileGameState(goal_board)

    def swap_tiles(self, state: TileGameState, r1: int, c1: int, r2: int, c2: int) -> TileGameState:
        """
        Swaps two tiles on the board and returns the new state.

        Args:
            state (TileGameState): The current state of the board.
            r1, c1, r2, c2 (int): The row and column indices of the tiles to be swapped.

        Returns:
            TileGameState: The new state after swapping the tiles.
        """
        board = list(list(row) for row in state.board)
        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
        return TileGameState(tuple(tuple(row) for row in board))

    @staticmethod
    def random_start(dim: int) -> TileGameState:
        """
        Generates a random start state for the game.

        Args:
            dim (int): The dimension of the game board.

        Returns:
            TileGameState: A randomly shuffled initial state.
        """
        tiles = list(range(1, dim * dim + 1))

        # Shuffle the list randomly
        random.shuffle(tiles)

        # Convert the shuffled list into a 2D list (board)
        board = tuple([tuple(tiles[i * dim:(i + 1) * dim])
                      for i in range(dim)])
        return TileGameState(board)

    ###### USE TO VISUALIZE BOARD IF YOU WISH ######
    @staticmethod
    def board_to_pretty_string(board: TileGameState) -> str:
        """
        Converts a board state to a string for easy visualization.

        Args:
            board (TileGameState): The board state to be converted.

        Returns:
            str: A formatted string representing the board.
        """
        hbar = "-"
        vbar = "|"
        corner = "+"
        dim = len(board.board)

        s = corner
        for i in range(2 * dim - 1):
            s += hbar
        s += corner + "\n"

        for r in range(dim):
            s += vbar
            for c in range(dim):
                s += str(board.board[r][c]) + " "
            s = s[:-1]
            s += vbar
            s += "\n"

        s += corner
        for i in range(2 * dim - 1):
            s += hbar
        s += corner
        return s

    @staticmethod
    def print_pretty_path(board_path: List[TileGameState]) -> None:
        """
        Prints a sequence of board states for easy visualization.

        Args:
            board_path (List[TileGameState]): A list of board states to print.
        """
        for b in board_path:
            print(TileGame.board_to_pretty_string(b))


class HeuristicTileGame(TileGame, HeuristicSearchProblem):
    """
    HeuristicTileGame extends the TileGame class and implements the HeuristicSearchProblem interface, 
    allowing the use of heuristics to guide the search towards the goal state more efficiently.

    This class uses the same board configuration and methods as TileGame, but with the addition of a 
    heuristic function to estimate the cost to reach the goal state from a given state.
    """

    def heuristic(self, state: TileGameState) -> float:
        return super().heuristic(state)

    def __init__(self, dim: int, heuristic, start_state: Optional[TileGameState] = None, goal_state: Optional[TileGameState] = None) -> None:
        super().__init__(dim, start_state, goal_state)
        self.heuristic = heuristic