import argparse
from queue import LifoQueue, Queue
from typing import List, Dict, Optional, Tuple
from search_problem import SearchProblem, State
from tile_game import TileGame
from search import bfs, dfs
import tqdm


def iterative_deepening_search(problem: SearchProblem[State]) -> Tuple[Optional[List[State]], Dict[str, int]]:
    """
    Performs Iterative Deepening Search (IDS) on the given problem.

    Args:
        problem (SearchProblem[State]): The search problem to solve.

    Returns:
        Tuple[Optional[List[State]], Dict[str, int]]:
            - A list of states representing the solution path, or None if no solution was found.
            - A dictionary of search statistics, including:
                - 'path_length': The length of the final path.
                - 'states_expanded': The number of states expanded during the search.
                - 'total_cost': The total cost of the path (number of moves to reach the goal).
                - 'max_frontier_size': The maximum size of the frontier during the search.
    """

    stats = {"path_length": 0, "states_expanded": 0,
             "total_cost": 0, "max_frontier_size": 0}

    cutoff_depth = 1
    goal_found = False
    while not goal_found:
        # Run depth-limited search with the current cutoff depth
        result, stats = depth_limited_search(problem, cutoff_depth)

        # Update stats
        states_expanded = stats["states_expanded"]
        max_frontier_size = stats["max_frontier_size"]
        stats["states_expanded"] += states_expanded
        stats["max_frontier_size"] = max(
            stats["max_frontier_size"], max_frontier_size)
        if not result:
            # If no solution was found, increase the cutoff depth and continue
            cutoff_depth += 1
        else:
            # If a solution was found, return the path and stats
            goal_found = True
            stats["path_length"] = len(result)
            stats["total_cost"] = len(result) - 1
            return result, stats

    return None, stats


def depth_limited_search(problem: SearchProblem[State], depth: int) -> Tuple[Optional[List[State]], Dict[str, int]]:
    """
    Implement depth-limited search.

    Input:
        problem - the SearchProblem to solve
        depth - the maximum depth to which the search should explore

    Output:
        a list of states representing the path of the solution
        the number of states expanded during the search
    """
    frontier = LifoQueue()
    start_state = problem.get_start_state()
    frontier.put(start_state)
    parents_dict = {start_state: None}
    depth_of_state = {start_state: 0}
    num_states_expanded = 0
    max_frontier_size = 1

    while not frontier.empty():
        # update size of frontier stat
        max_frontier_size = max(max_frontier_size, frontier.qsize())

        # get state from open set
        state = frontier.get()

        if problem.is_goal_state(state):
            # Backtracking: use parents dictionary to construct path
            # Path will be in reverse order at first (state is currently the goal state)
            path = [state]

            # Loop until a node with no parents is reached (the start state)
            while state and parents_dict[state] is not None:
                parent = parents_dict[state]
                state = parent
                path.append(state)

            # Reverse path
            path.reverse()
            return path, {'states_expanded': num_states_expanded, 'max_frontier_size': max_frontier_size}
        else:
            # Expand state (get successors)
            successors = problem.get_successors(state)
            num_states_expanded += 1

            visited = parents_dict
            for child in successors:
                if child in visited:
                    # If we've visited a node before, it may have been at a different depth
                    # Check if we need to lower the depth
                    temp_depth = depth_of_state[state] + 1
                    if temp_depth < depth_of_state[child]:
                        # If a node was reached at a different depth,
                        # update parent dictionary (to guarantee we use the faster path)
                        depth_of_state[child] = temp_depth
                        parents_dict[child] = state
                        if depth_of_state[child] <= depth:
                            frontier.put(child)
                else:
                    # First time visiting a node
                    depth_of_state[child] = depth_of_state[state] + 1
                    parents_dict[child] = state
                    if depth_of_state[child] <= depth:
                        frontier.put(child)

    return None, {'states_expanded': num_states_expanded, 'max_frontier_size': max_frontier_size}


def compile_stats(size: int, n_trials: int, ids_only: bool) -> Dict[str, List[float]]:
    """
    Collect stats for BFS, DFS, and IDS on TileGame problems.
    This method is intended to be used for comparing the performance of blind-search algorithms

    Args:
        size (int): The size of the TileGame problem.
        n_trials (int): The number of trials to run for each algorithm.
        ids_only (bool): Whether to run only IDS or all algorithms.

    Returns:
        Dict[str, Tuple[int, int]]: A dictionary containing the average statistics for each algorithm.

    Note: 
        The statistics are: the number of states expanded, the maximum frontier size, and the average path length.
    """
    # 0 = states expanded, 1 = max frontier size
    stats = {'bfs': [0., 0., 0.], 'dfs': [0., 0., 0.], 'ids': [0., 0., 0.]}
    if n_trials <= 0:
        return stats

    for _ in tqdm.tqdm(range(n_trials)):
        tile_game = TileGame(size)

        if not ids_only:  # run all algos
            # BFS
            bfs_path, bfs_stats = bfs(tile_game)
            stats['bfs'][0] += bfs_stats['states_expanded']
            stats['bfs'][1] += bfs_stats['max_frontier_size']
            if bfs_path:
                stats['bfs'][2] += len(bfs_path)

            # DFS
            dfs_path, dfs_stats = dfs(tile_game)
            stats['dfs'][0] += dfs_stats['states_expanded']
            stats['dfs'][1] += dfs_stats['max_frontier_size']
            if dfs_path:
                stats['dfs'][2] += len(dfs_path)
        print("starting ID")
        # IDS
        ids_path, ids_stats = iterative_deepening_search(tile_game)
        stats['ids'][0] += ids_stats['states_expanded']
        stats['ids'][1] += ids_stats['max_frontier_size']
        if ids_path:
            stats['ids'][2] += len(ids_path)

    avg_stats = {algo: [val[0] / n_trials, val[1] / n_trials, val[2] / n_trials]
                 for algo, val in stats.items()}
    return avg_stats


def main() -> None:
    """
    Run 3 different search algorithms (BFS, DFS, IDS) on TileGame problems.
    The results of each search are printed to the console.
    """
    parser = argparse.ArgumentParser(
        description='Run search algorithms on TileGame problems.')
    parser.add_argument('--size', type=int, default=2,
                        help='Size of the TileGame (default: 2)')
    parser.add_argument('--trials', type=int, default=10,
                        help='Number of trials to run (default: 10)')
    parser.add_argument('--ids', action='store_true', help='Run IDS only')

    args = parser.parse_args()
    SIZE = args.size
    N_TRIALS = args.trials
    if args.ids:
        print(f"Running IDS on {N_TRIALS} {SIZE}x{SIZE} TileGame problems...")
        avg_stats = compile_stats(SIZE, N_TRIALS, True)
        print("IDS Average States Expanded: ", avg_stats['ids'][0])
        print("IDS Average Max Frontier Size: ", avg_stats['ids'][1])
        print("IDS Average Path Length: ", avg_stats['ids'][2])
    else:
        print(f"Running BFS, DFS, IDS on {N_TRIALS} {SIZE}x{SIZE} TileGame problems...")
        avg_stats = compile_stats(SIZE, N_TRIALS, False)
        print("BFS Average States Expanded: ", avg_stats['bfs'][0])
        print("DFS Average States Expanded: ", avg_stats['dfs'][0])
        print("IDS Average States Expanded: ", avg_stats['ids'][0])
        print("BFS Average Max Frontier Size: ", avg_stats['bfs'][1])
        print("DFS Average Max Frontier Size: ", avg_stats['dfs'][1])
        print("IDS Average Max Frontier Size: ", avg_stats['ids'][1])
        print("BFS Average Path Length: ", avg_stats['bfs'][2])
        print("DFS Average Path Length: ", avg_stats['dfs'][2])
        print("IDS Average Path Length: ", avg_stats['ids'][2])


if __name__ == "__main__":
    main()