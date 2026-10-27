from typing import Dict, List, Set, Tuple

from heuristic_adversarial_search_problem import HeuristicAdversarialSearchProblem, GameState


class DAGState(GameState):
    """
    State class for DAG HASP
    """

    def __init__(self, index, player_to_move):
        self._index = index
        self._ptm = player_to_move

    def player_to_move(self):
        return self._ptm


Action = int


class GameDAG(HeuristicAdversarialSearchProblem[DAGState, Action]):
    """
    A HASP class to help with testing purposes.
    """

    def __init__(
        self,
        matrix: List[List[bool]],
        start_state: DAGState,
        terminal_evaluations: Dict[int, float],
    ):
        """
        An implementation of AdversarialSearchProblem for testing purposes
        Inputs:
            matrix - an n-by-n 2D array storing booleans, where n is
            the number of states in the game, and each state is represented
            by a unique natural number between 0 and n-1 inclusive.
            
            matrix[i][j] stores the proposition that it is possible to
            transition from the state whose index is i to the state
            whose index is j.

            start_state - a DAGState representing a starting state

            terminal_evaluations - a dictionary where the key is the index of
            a terminal state and the value is the value at that terminal state.
        """
        # Prevent cycles
        if any(
            matrix[i][j]
            for i in range(len(matrix))
            for j in range(len(matrix[0]))
            if i >= j
        ):
            raise ValueError(
                "GameDAG edges must go from lower index states to higher index states (to prevent cycles)"
            )

        if not terminal_evaluations:
            raise ValueError("terminal_evaluations must not be empty")

        self._matrix = matrix
        self._start_state = start_state
        self._terminal_evaluations = terminal_evaluations

    def heuristic(self, state: DAGState) -> float:
        """
        Constant heuristic function for a given state (always 0)
        """
        
        return 0

    def get_available_actions(self, state: DAGState) -> Set[Action]:
        """
        Inputs:
            state - a DAGState
        Outputs:
            A set containing the actions available to the player-to-move
            from the given state
            Returns an empty set if the state is a terminal state.

            For a GameDAG an action is a natural number whose value corresponds
            to the index of the next state
        """
        if self.is_terminal_state(state):
            return set()
        available_actions = set()
        actions_to_check = self._matrix[state._index]
        for i in range(0, len(actions_to_check)):
            if actions_to_check[i]:
                available_actions.add(i)
        return available_actions

    def transition(self, state: DAGState, action: Action) -> DAGState:
        """
        Inputs:
            state- a DAGState
            action- a natural number whose value corresponds
            to the index of the next state
        Output:
            Returns the state that results from taking the given action
            from the given state. (Assume deterministic transitions.)
        """
        assert not (self.is_terminal_state(state))
        assert action in self.get_available_actions(state)

        return DAGState(action, 1 - state._ptm)

    def is_terminal_state(self, state: DAGState) -> bool:
        """
        Input:
            state- a DAGState
        Ouput:
            A boolean indicating whether or not the given state is terminal.
        """
        return state._index in self._terminal_evaluations

    def get_result(self, state: DAGState) -> float:
        """
        Input:
            state- a terminal DAGState
        Output:
            returns the value of the state to the player.
        """
        assert self.is_terminal_state(state)

        return self._terminal_evaluations[state._index]