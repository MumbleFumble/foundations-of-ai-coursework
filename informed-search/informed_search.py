from queue import LifoQueue, PriorityQueue, Queue
from typing import List, Dict, Optional, Tuple, Any
from search_problem import State
from heuristic_search_problem import HeuristicSearchProblem
from tile_game import HeuristicTileGame, TileGame
from heuristics import admissible_heuristic, inadmissible_heuristic
from search import PathNotFoundError


def astar(problem: HeuristicSearchProblem) -> Tuple[Optional[List[State]], Dict[str, Any]]:
    """
    A* search algorithm implementation.

    Args:
        problem (HeuristicSearchProblem): The problem to solve, must provide a heuristic function.

    Returns:
        Tuple[Optional[List[State]], Dict[str, Any]]: 
            - A list of states representing the solution path, or None if no solution found.
            - A dictionary of search statistics including path_length, states_expanded, max_frontier_size.
    """
    # TODO: Implement A*
    #using f(n) = g(n) + h(n), where f is the total estimated cost, g is the cost to reach the node,
    #  and h is the heuristic estimate to the goal.
    stats = {
                "path_length": 0,
                "states_expanded": 0,
                "max_frontier_size": 0
            }
    path = []
    start = problem.get_start_state()
    frontier = PriorityQueue()
    frontier.put((problem.heuristic(start), start))  
    parents: Dict[State, Optional[State]] = {start: None}
    g_cost: Dict[State, float] = {start: 0}
    visited = set()
    
    while not frontier.empty():
        stats["max_frontier_size"] = max(stats["max_frontier_size"], frontier.qsize())

        f, current = frontier.get()

        if current not in visited:
            visited.add(current)

            stats["states_expanded"] += 1

            if problem.is_goal_state(current):
                while current is not None: # not back at the start
                    path.append(current)
                    current = parents[current]
                path.reverse()
                stats["path_length"] = len(path) - 1
                return path, stats

            for successor in problem.get_successors(current):
                temp_g = g_cost[current] + 1  
                if successor not in g_cost or temp_g < g_cost[successor]:
                    g_cost[successor] = temp_g
                    f_score = temp_g + problem.heuristic(successor)
                    frontier.put((f_score, successor))
                    parents[successor] = current


    raise PathNotFoundError()


def main() -> None:
    dim = 3
    tg = TileGame(dim)
    # admissible_tile_game = HeuristicTileGame(
    #     dim, start_state=tg.get_start_state(), heuristic=admissible_heuristic)
    inadmissible_tile_game = HeuristicTileGame(
        dim, start_state=tg.get_start_state(), heuristic=inadmissible_heuristic)

    path_inadmissible, stats_inadmissible = astar(inadmissible_tile_game)
    print("path (inadmissible):")
    tg.print_pretty_path(path_inadmissible)
    print("stats (inadmissible):", stats_inadmissible)
    print('-'*110)


if __name__ == "__main__":
    main()