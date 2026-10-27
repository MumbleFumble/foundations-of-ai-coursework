from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Union
from heuristic_adversarial_search_problem import HeuristicAdversarialSearchProblem
from asps.heuristic_connect_four import HeuristicConnectFourProblem
from asps.heuristic_ttt_problem import HeuristicTTTProblem
from adversarial_search import minimax, alpha_beta
from adversarial_search_problem import GameState, Action


class GameAgent(ABC):
    """
    Interface for GameAgents
    An agent is an object that takes actions given some state information.
    For the purposes of this assignment, it is a combination of search algorithm and heuristic.
    Agents with different search algorithms or heuristics can be compared by playing games.
    """
    @abstractmethod
    def get_move(self, state: GameState) -> Tuple[Action, Dict[str, int]]:
        """
        Returns an action and search statistics given a game state.
        
        Args:
            state: The current game state to analyze
            
        Returns:
            Tuple containing the best action and a dictionary of search statistics
        """
        pass


class MinimaxAgent(GameAgent):
    """
    A GameAgent that uses minimax search to find the best move.
    
    Uses the minimax algorithm with optional depth cutoff for adversarial search.
    When cutoff is reached, uses heuristic evaluation instead of exhaustive search.
    """

    def __init__(self, searchproblem: HeuristicAdversarialSearchProblem, cutoff_depth: float = 3) -> None:
        """
        Initialize the MinimaxAgent with a search problem and cutoff depth.
        
        Args:
            searchproblem: The adversarial search problem to solve
            cutoff_depth: Maximum search depth before using heuristic evaluation
        """
        self.searchproblem = searchproblem
        self.cutoff_depth = cutoff_depth

    def get_move(self, state: GameState) -> Tuple[Action, Dict[str, int]]:
        """
        Get the best move using minimax search.
        
        Args:
            state: The current game state
            
        Returns:
            Tuple containing the best action and search statistics
        """
        self.searchproblem.set_start_state(state)
        return minimax(self.searchproblem, cutoff_depth=self.cutoff_depth)


class AlphaBetaAgent(GameAgent):
    """
    A GameAgent that uses alpha-beta search to find the best move.
    
    Uses alpha-beta pruning optimization of minimax to eliminate branches
    that cannot influence the final decision, improving search efficiency.
    """

    def __init__(self, searchproblem: HeuristicAdversarialSearchProblem, cutoff_depth: float = 3) -> None:
        """
        Initialize the AlphaBetaAgent with a search problem and cutoff depth.
        
        Args:
            searchproblem: The adversarial search problem to solve
            cutoff_depth: Maximum search depth before using heuristic evaluation
        """
        self.searchproblem = searchproblem
        self.cutoff_depth = cutoff_depth

    def get_move(self, state: GameState) -> Tuple[Action, Dict[str, int]]:
        """
        Get the best move using alpha-beta pruning search.
        
        Args:
            state: The current game state
            
        Returns:
            Tuple containing the best action and search statistics
        """
        self.searchproblem.set_start_state(state)
        return alpha_beta(self.searchproblem, cutoff_depth=self.cutoff_depth)