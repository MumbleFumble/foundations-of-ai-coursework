import unittest
from typing import Optional, Callable

from directed_graph import DirectedGraph
from search import bfs, dfs
from tile_game import TileGame, TileGameState, HeuristicTileGame
from informed_search import astar
from blind_search import iterative_deepening_search
from heuristics import admissible_heuristic, inadmissible_heuristic


class IOTest(unittest.TestCase):
    """
    Tests IO for search implementations. Contains basic/trivial test cases.

    Each test function instantiates a search problem (TileGame) and tests if the three test case
    contains the solution, the start state is in the solution, the end state is in the
    solution and, if applicable, if the length of the solutions are the same.

    These tests are not exhaustive and do not check if your implementation follows the
    algorithm correctly. We encourage you to create your own tests as necessary.
    """

    def _check_tilegame(self, start_state: TileGameState, goal_state: TileGameState, length: Optional[int] = None, heuristic: Optional[Callable[[TileGameState], float]] = None) -> None:
        """
        Test algorithm on a TileGame
        algorithm: algorithm to test
        start_state: start state of the TileGame
        goal_state: goal state of the TileGame
        length: length that the path returned from algorithm should be. 
                Think about why this argument is optional, and when you should provide it.
        heuristic: heuristic to use for the TileGame (admissible or inadmissible)
        """
        # Ensure start_state and goal_state dimensions are n x n
        self.assertEqual(len(start_state.board), len(start_state.board[0]), "Dimensions must be n x n")
        dim = len(start_state.board)
        
        # Initialize the TileGame with the provided start and goal states, and the given heuristic
        game = HeuristicTileGame(dim, start_state=start_state, goal_state=goal_state, heuristic=heuristic)
        
        # Run the algorithm (e.g., A* or any other search algorithm) on the game
        path, stats = astar(game)
        
        # Check that the path starts and ends with the correct states
        self.assertEqual(path[0], start_state, "Path should start with the start state")
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        # If a path length is provided, verify the length matches the expected value
        if length:
            self.assertEqual(len(path), length, f"Path length should be {length}")
        
    def test_astar(self) -> None:
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        self._check_tilegame(start_state, goal_state, length=7, heuristic=admissible_heuristic)

    def test_trivial_goal_state(self):
        # Edge case: start == goal should return a path of length 1.
        start_state = TileGameState(((1, 2), (3, 4)))
        goal_state = TileGameState(((1, 2), (3, 4)))
        self._check_tilegame(start_state, goal_state, length=1, heuristic=admissible_heuristic)

    def test_unsolvable_board(self):
        # Edge case: if board is unsolvable, astar should raise PathNotFoundError.
        start_state = TileGameState(((2, 1), (3, 5))) 
        goal_state = TileGameState(((1, 2), (3, 4)))
        from informed_search import astar, PathNotFoundError
        from heuristics import admissible_heuristic
        game = HeuristicTileGame(2, start_state=start_state, goal_state=goal_state, heuristic=admissible_heuristic)
        with self.assertRaises(PathNotFoundError):
            astar(game)

    def test_path_reconstruction_correctness(self):
        # Bug check: path returned should actually transform start -> goal.
        start_state = TileGameState(((1, 2), (4, 3)))
        goal_state = TileGameState(((1, 2), (3, 4)))
        path, stats = astar(HeuristicTileGame(2, start_state=start_state, goal_state=goal_state, heuristic=admissible_heuristic))
        self.assertEqual(path[0], start_state)
        self.assertEqual(path[-1], goal_state)
        self.assertTrue(all(isinstance(state, TileGameState) for state in path))

    def test_my_heuristic_nonnegative(self):
        # Bug check: my_heuristic should never return negative values.
        from heuristics import my_heuristic
        state = TileGameState(((2, 1), (3, 4)))
        self.assertGreaterEqual(my_heuristic(state), 0)

    def test_admissible_monotonicity(self):
        # Check heuristic consistency: heuristic(start) >= 0 and goal == 0.
        from heuristics import admissible_heuristic
        goal = TileGameState(((1, 2), (3, 4)))
        self.assertEqual(admissible_heuristic(goal), 0)
        start = TileGameState(((2, 1), (3, 4)))
        self.assertGreaterEqual(admissible_heuristic(start), 0)

    def test_inadmissible_may_overestimate(self):
        # Check inadmissible_heuristic can return a larger value than admissible.
        from heuristics import inadmissible_heuristic, admissible_heuristic
        state = TileGameState(((2, 1), (3, 4)))
        self.assertGreaterEqual(inadmissible_heuristic(state), admissible_heuristic(state))

    def test_large_board_runs(self):
        # Edge case: A* should handle larger boards without crashing.
        start_state = TileGameState(((4, 3), (2, 1)))
        goal_state = TileGameState(((1, 2), (3, 4)))
        path, stats = astar(HeuristicTileGame(2, start_state=start_state, goal_state=goal_state, heuristic=admissible_heuristic))
        self.assertIn("states_expanded", stats)

    def test_multiple_solutions_minimal_length(self):
        # Check that A* returns the shortest path when multiple solutions exist.
        start_state = TileGameState(((1, 3), (2, 4)))
        goal_state = TileGameState(((1, 2), (3, 4)))
        path, stats = astar(HeuristicTileGame(2, start_state=start_state, goal_state=goal_state, heuristic=admissible_heuristic))
        self.assertEqual(stats["path_length"], 3)  # Known minimal solution length

    def test_frontier_growth(self):
        #Bug check: max_frontier_size should be >= states_expanded.
        start_state = TileGameState(((1, 3), (4, 2)))
        goal_state = TileGameState(((1, 2), (3, 4)))
        path, stats = astar(HeuristicTileGame(2, start_state=start_state, goal_state=goal_state, heuristic=admissible_heuristic))
        self.assertGreaterEqual(stats["max_frontier_size"], stats["states_expanded"])



if __name__ == "__main__":
    unittest.main()