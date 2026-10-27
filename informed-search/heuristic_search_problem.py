from abc import abstractmethod
from search_problem import SearchProblem, State

class HeuristicSearchProblem(SearchProblem[State]):
    """
    Abstract base class for heuristic search problems.

    This class extends the SearchProblem class and introduces a heuristic function 
    that estimates the cost to reach the goal state from a given state.

    Methods:
        heuristic(state: State) -> float:
            Abstract method that must be implemented by subclasses to provide 
            a heuristic estimate for a given state.
    """
    @abstractmethod
    def heuristic(self, state: State) -> float:
        """
        Returns a heuristic estimate of the cost to reach the goal from the given state.

        Args:
            state (State): The current state of the problem.

        Returns:
            float: The estimated cost to reach the goal from the given state.
        """
        pass
