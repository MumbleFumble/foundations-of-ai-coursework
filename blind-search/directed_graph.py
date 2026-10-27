# A matrix representation of a directed graph.
# This is for your testing.
# Read the assignment handout for details.

from typing import List, Optional, Set

from search_problem import SearchProblem


class DirectedGraph(SearchProblem[int]):
    """
    DGraph holds an adjacency matrix, which represents a directed graph. See the handout for more
    information on adjacency matrices.

    DGraph implements the SearchProblem Abstract Base Class. A state in DGraph is just an integer
    representing a node in the graph.
    """

    def __init__(
        self,
        matrix: List[List[Optional[float]]],
        goal_indices: Set[int],
        start_state: int = 0,
    ):
        """
        matrix - the matrix representation of the directed graph

        goal_indices - a Python set of the indices of the states
                       that are goal states.

        start_state - the index of the start state. 0 by default.
        """
        self.matrix = matrix
        self.goal_indices = goal_indices
        self.start_state = start_state

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        return state in self.goal_indices

    def get_successors(self, state):
        row = self.matrix[state]
        successors = {}
        index = 0
        for cost in row:
            if not (cost == None):
                successors[index] = cost
            index += 1
        return successors