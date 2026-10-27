import unittest
from typing import Optional, Callable, Any, Tuple, List
from maze import Maze
from search import PathNotFoundError, bfs, dfs
from directed_graph import DirectedGraph


class IOTest(unittest.TestCase):
    """
    Tests IO for bfs and dfs implementations. Contains basic/trivial test cases.

    Each test instatiates a Maze object and tests the bfs and dfs algorithms on it.
    Note: The tests currently are only testing if the algorithms start and end at the
    correct locations and if the path returned is the correct length (optional).

    You may wish to add path validity checks. How do you know if a path is valid nor not?
    Your path should not teleport you, move through a wall, or go through a cell more than once.
    Maybe you should test for this... We certainly will during grading!

    These tests are not exhaustive and do not check if your implementation follows the
    algorithm correctly. We encourage you to create your own tests as necessary.
    """

    def _check_maze(self, algorithm: Callable[[Maze], Tuple[Optional[List[Any]], dict]], maze: Maze, length: Optional[int] = None) -> None:
        """
        Test algorithm on a Maze
        algorithm: algorithm to test
        maze: Maze to test algorithm on
        length: length that the path returned from algorithm should be.
                Think about why this argument is optional, and when you should provide it.
        """
        path = algorithm(maze)[0]
        self.assertIsNotNone(path, "Algorithm should return a valid path")
        
        if path is not None:
            self.assertEqual(path[0], maze.get_start_state(),
                             "Path should start with the start state")
            self.assertTrue(maze.is_goal_state(path[-1]),
                            "Path should end with the goal state")
            if length:
                self.assertEqual(len(path), length,
                                 f"Path length should be {length}")

    def test_bfs(self) -> None:
        # Catches: BFS correctness on trivial mazes (1x1, 2x2, 10x10).
        single_cell_maze = Maze(1, 1)
        self._check_maze(bfs, single_cell_maze, 1)

        two_by_two_maze = Maze(2, 2)
        self._check_maze(bfs, two_by_two_maze, 3)

        large_maze = Maze(10, 10)
        self._check_maze(bfs, large_maze)
    
    def test_bfs_single_cell_stats(self):
        # Catches: incorrect stats reporting when maze is solved immediately.
        maze = Maze(1, 1)
        path, stats = bfs(maze)
        self.assertEqual(stats["path_length"], 1)
        self.assertEqual(stats["states_expanded"], 1)
        self.assertEqual(stats["max_frontier_size"], 1)

    def test_bfs_two_by_two_stats(self):
        # Catches: BFS miscounting path length, states expanded, or frontier size.
        maze = Maze(2, 2)
        path, stats = bfs(maze)
        self.assertEqual(stats["path_length"], 3)
        self.assertGreaterEqual(stats["states_expanded"], 2)
        self.assertGreaterEqual(stats["max_frontier_size"], 1)

    def test_bfs_path_shortest(self):
        # Catches: BFS not returning the shortest path compared to DFS.
        maze = Maze(4, 4)
        bfs_path, _ = bfs(maze)
        dfs_path, _ = dfs(maze)
        self.assertLessEqual(len(bfs_path), len(dfs_path),
                             "should be the shortest path")

    def test_bfs_frontier_growth(self):
        # Catches: BFS frontier never grows (would suggest algorithm bug).
        maze = Maze(5, 5)
        _, stats = bfs(maze)
        self.assertGreater(stats["max_frontier_size"], 1,
                           "Frontier should grow")

    def test_bfs_states_expanded_increases(self):
        # Catches: BFS not scaling correctly with maze size.
        maze_small = Maze(2, 2)
        _, stats_small = bfs(maze_small)
        maze_large = Maze(6, 6)
        _, stats_large = bfs(maze_large)
        self.assertGreater(stats_large["states_expanded"], stats_small["states_expanded"],
                           "should expand more states")

    def test_no_solution(self):
        # Catches: algorithms failing to raise PathNotFoundError when no path exists.
        maze = Maze(1, 2)
        maze.board[0][0].south = 1
        maze.board[1][0].north = 1
        with self.assertRaises(PathNotFoundError):
            bfs(maze)
        with self.assertRaises(PathNotFoundError):
            dfs(maze)

    def test_multiple_shortest_paths(self):
        # Catches: BFS or DFS returning invalid or too-long paths in open mazes.
        maze = Maze(2, 2)
        for row in maze.board:
            for room in row:
                room.north = room.south = room.east = room.west = 0
        path_bfs, _ = bfs(maze)
        path_dfs, _ = dfs(maze)
        self.assertEqual(path_bfs[0], maze.get_start_state())
        self.assertEqual(path_dfs[0], maze.get_start_state())
        self.assertTrue(maze.is_goal_state(path_bfs[-1]))
        self.assertTrue(maze.is_goal_state(path_dfs[-1]))
        self.assertLessEqual(len(path_bfs), 3, "BFS should find one of the shortest paths")
        self.assertLessEqual(len(path_dfs), 3, "DFS should find one of the shortest paths")

    def test_path_validity_bfs(self):
        # Catches: BFS returning paths with repeated states (looping).
        maze = Maze(4, 4)
        path, _ = bfs(maze)
        self.assertEqual(len(path), len(set(path)),
                         "BFS path issue")

    # --- DFS TESTS ---
    def test_dfs(self) -> None:
        # Catches: DFS correctness on trivial mazes (1x1, 2x2, 10x10).
        single_cell_maze = Maze(1, 1)
        self._check_maze(dfs, single_cell_maze, 1)

        two_by_two_maze = Maze(2, 2)
        self._check_maze(dfs, two_by_two_maze, 3)

        large_maze = Maze(10, 10)
        self._check_maze(dfs, large_maze)
    
    def test_bfs_vs_dfs_path_length(self):
        # Catches: BFS not shorter or equal length compared to DFS.
        maze = Maze(5, 5)
        bfs_path, _ = bfs(maze)
        dfs_path, _ = dfs(maze)
        self.assertLessEqual(len(bfs_path), len(dfs_path),
                             "BFS path should be no longer than DFS path")

    def test_dfs_single_cell_stats(self):
        # Catches: DFS stats incorrect for trivial case.
        maze = Maze(1, 1)
        _, stats = dfs(maze)
        self.assertEqual(stats["path_length"], 1)
        self.assertEqual(stats["states_expanded"], 1)
        self.assertEqual(stats["max_frontier_size"], 1)

    def test_dfs_two_by_two_stats(self):
        # Catches: DFS miscounting stats in small maze.
        maze = Maze(2, 2)
        _, stats = dfs(maze)
        self.assertEqual(stats["path_length"], 3)
        self.assertGreaterEqual(stats["states_expanded"], 2)
        self.assertGreaterEqual(stats["max_frontier_size"], 1)

    def test_dfs_frontier_growth(self):
        # Catches: DFS frontier never grows (algorithmic bug).
        maze = Maze(5, 5)
        _, stats = dfs(maze)
        self.assertGreater(stats["max_frontier_size"], 1,
                           "Frontier should grow")

    def test_dfs_states_expanded_increases(self):
        # Catches: DFS not expanding more states on larger maze.
        maze_small = Maze(2, 2)
        _, stats_small = dfs(maze_small)
        maze_large = Maze(6, 6)
        _, stats_large = dfs(maze_large)
        self.assertGreater(stats_large["states_expanded"], stats_small["states_expanded"],
                           "Larger maze should expand more states")

    def test_path_validity_dfs(self):
        # Catches: DFS returning invalid paths with repeated states.
        maze = Maze(4, 4)
        path, _ = dfs(maze)
        self.assertEqual(len(path), len(set(path)),
                         "DFS path issue")
    
    def test_dfs_branching_path(self):
        # Catches: DFS failing to return valid path in open maze with multiple branches.
        maze = Maze(2, 2)
        for row in maze.board:
            for room in row:
                room.north = room.south = room.east = room.west = 0
        path, _ = dfs(maze)
        self.assertEqual(path[0], maze.get_start_state())
        self.assertTrue(maze.is_goal_state(path[-1]))
        self.assertEqual(len(path), len(set(path)), "DFS path revisits states")

    def test_dfs_long_skinny_maze(self):
        # Catches: DFS breaking on deep/linear mazes (stack issues or wrong expansion).
        maze = Maze(1, 10)
        for j in range(9):
            maze.board[0][j].east = 0
            maze.board[0][j+1].west = 0
        path, _ = dfs(maze)
        self.assertEqual(path[0], maze.get_start_state())
        self.assertTrue(maze.is_goal_state(path[-1]))

    # --- GENERAL TESTS ---
    def test_single_row_maze(self):
        # Catches: Algorithms mishandling single-row mazes.
        maze = Maze(1, 5)
        for j in range(4):
            maze.board[0][j].east = 0
            maze.board[0][j+1].west = 0
        path_bfs, _ = bfs(maze)
        path_dfs, _ = dfs(maze)
        self.assertTrue(maze.is_goal_state(path_bfs[-1]))
        self.assertTrue(maze.is_goal_state(path_dfs[-1]))

    def test_single_column_maze(self):
        # Catches: Algorithms mishandling single-column mazes.
        maze = Maze(5, 1)
        for i in range(4):
            maze.board[i][0].south = 0
            maze.board[i+1][0].north = 0
        path_bfs, _ = bfs(maze)
        path_dfs, _ = dfs(maze)
        self.assertTrue(maze.is_goal_state(path_bfs[-1]))
        self.assertTrue(maze.is_goal_state(path_dfs[-1]))

    def test_stats_consistency_trivial(self):
        # Catches: stats not consistent on trivial maze.
        maze = Maze(1, 1)
        _, stats_bfs = bfs(maze)
        _, stats_dfs = dfs(maze)
        for stats in (stats_bfs, stats_dfs):
            self.assertEqual(stats["path_length"], 1)
            self.assertEqual(stats["states_expanded"], 1)
            self.assertEqual(stats["max_frontier_size"], 1)

    def test_frontier_never_exceeds_total_states(self):
        # Catches: frontier size blowing up beyond possible number of states.
        maze = Maze(4, 4)
        for algo in (bfs, dfs):
            _, stats = algo(maze)
            self.assertLessEqual(stats["max_frontier_size"], maze.width * maze.height)

    def test_path_valid_moves_only(self):
        # Catches: BFS/DFS paths teleporting across the maze (invalid moves).
        maze = Maze(3, 3)
        for algo in (bfs, dfs):
            path, _ = algo(maze)
            for a, b in zip(path, path[1:]):
                r1, c1 = a.location
                r2, c2 = b.location
                self.assertTrue(abs(r1 - r2) + abs(c1 - c2) == 1,
                                "Invalid move found in path")

    def test_directed_graph(self):
        # Catches: BFS/DFS correctness on non-maze graph problems.
        # Graph: 0 -> 1, 0 -> 2, goal = 2
        matrix = [
            [None, 1, 1],
            [None, None, None],
            [None, None, None],
        ]
        graph = DirectedGraph(matrix, goal_indices={2}, start_state=0)
        path_bfs, _ = bfs(graph)
        path_dfs, _ = dfs(graph)
        self.assertEqual(path_bfs[0], 0)
        self.assertEqual(path_bfs[-1], 2)
        self.assertEqual(path_dfs[0], 0)
        self.assertEqual(path_dfs[-1], 2)

if __name__ == "__main__":
    unittest.main()