from typing import List, Tuple, Dict, Optional
from queue import Queue
from search_problem import SearchProblem, State


class PathNotFoundError(Exception):
    def __init__(self, message="Path not found"):
        self.message = message
        super().__init__(self.message)
        
def bfs(problem: SearchProblem[State]) -> Tuple[Optional[List[State]], Dict[str, int]]:
    """
    Performs Breadth-First Search (BFS) on the given problem.

    Args:
        problem (SearchProblem[State]): The search problem to solve.

    Returns:
        Tuple[Optional[List[State]], Dict[str, int]]:
            - A list of states representing the solution path, or None if no solution was found.
            - A dictionary of search statistics, including:
                - 'path_length': The length of the final path.
                - 'states_expanded': The number of states expanded during the search.
                - 'max_frontier_size': The maximum size of the frontier during the search.
    """
    stats = {"path_length": 0, "states_expanded": 0, "max_frontier_size": 0}
    start = problem.get_start_state()
    frontier = Queue()
    visited = set([start])
    parents: Dict[State, State] = {}
    frontier.put(start)
    if problem.is_goal_state(start):
        return [start], {"path_length": 1, "states_expanded": 1, "max_frontier_size": 1}
    while not frontier.empty():
        current = frontier.get()
        stats["states_expanded"] += 1
        if problem.is_goal_state(current):
            path = reconstruct_path(parents, current, problem)
            stats["path_length"] = len(path) 
            return path, stats
        
        
        for neighbor in problem.get_successors(current):
            if neighbor not in visited:
                parents[neighbor] = current
                frontier.put(neighbor)
                visited.add(neighbor)

        stats["max_frontier_size"] = max(stats["max_frontier_size"], frontier.qsize())
            
                
                
                
    raise PathNotFoundError
    
    
    

def dfs(problem: SearchProblem[State]) -> Tuple[Optional[List[State]], Dict[str, int]]:
    """
    Performs a depth-first search (DFS) on the given search problem.

    Args:
        problem (SearchProblem[State]): The search problem to solve.

    Returns:
        Tuple[Optional[List[State]], Dict[str, int]]:
            - A list of states representing the solution path, or None if no solution was found.
            - A dictionary of search statistics, including:
                - 'path_length': The length of the final path.
                - 'states_expanded': The number of states expanded during the search.
                - 'max_frontier_size': The maximum size of the frontier during the search.
    """
    # TODO: Update these values
    stats = {"path_length": 0, "states_expanded": 0, "max_frontier_size": 0}
    start = problem.get_start_state()
    if problem.is_goal_state(start):
        return [start], {"path_length": 1, "states_expanded": 1, "max_frontier_size": 1}
    frontier = [start]
    parents: Dict[State, State] = {}
    visited = set([start])
    while frontier:
        current = frontier.pop()
        stats["states_expanded"] += 1
        if problem.is_goal_state(current):
            path = reconstruct_path(parents, current, problem)
            stats["path_length"] = len(path) 
            return path, stats
         

        for neighbor in problem.get_successors(current):
            if neighbor not in visited:
                parents[neighbor] = current
                frontier.append(neighbor)
                visited.add(neighbor)

        stats["max_frontier_size"] = max(stats["max_frontier_size"], len(frontier))
                        
    raise PathNotFoundError


def reconstruct_path(path: Dict[State, State], end: State, problem: SearchProblem[State]) -> List[State]:
    """
    Reconstructs the path from the start state to the given end state.
    
    This function traces back through the parent mapping to build the complete path
    from start to goal. The path is initially built in reverse order (goal to start)
    and then reversed to give the correct order.

    Args:
        path (Dict[State, State]): A dictionary mapping each state to its predecessor in the search.
        end (State): The goal state to trace back from.
        problem (SearchProblem[State]): The search problem to solve.

    Returns:
        List[State]: The reconstructed path from the start state to the goal state.
    """
    reverse_path = []
    while end != problem.get_start_state():
        reverse_path.append(end)
        end = path[end]
    reverse_path.append(problem.get_start_state())
    reverse_path.reverse()
    return reverse_path

############### SANDBOX ###############
def main() -> None:
    # Initialize the maze and generate it based on given dimensions
    print("Generated Maze:")
    width, height = 30, 30
    maze = Maze(width, height)
    
    # Run BFS and DFS to find paths
    print("BFS Path:")
    bfs_path, bfs_stats = bfs(maze)
    print(f"BFS found path: {bfs_path}")
    print(f"BFS stats: {bfs_stats}")
    maze.visualize_maze(path=bfs_path, algorithm_name="bfs")
    
    print("DFS Path:")
    dfs_path, dfs_stats = dfs(maze)
    print(f"DFS found path: {dfs_path}")
    print(f"DFS stats: {dfs_stats}")
    maze.visualize_maze(path=dfs_path, algorithm_name="dfs")


if __name__ == "__main__":
    main()
