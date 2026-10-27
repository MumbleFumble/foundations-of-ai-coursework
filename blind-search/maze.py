from typing import List, Tuple, Optional, Dict, Set
import random
import matplotlib.pyplot as plt
from search_problem import SearchProblem


class MazeRoom:
    """
    Represents a single room or cell in the maze. Each room has walls on all 
    four sides (north, south, east, west) initially, and a flag indicating 
    whether the room has been visited.
    """
    def __init__(self) -> None:
        self.north = 1
        self.south = 1
        self.east = 1
        self.west = 1
        self.visited = False  # Initially, no room has been visited


class MazeState:
    """
    Represents a specific position within the maze and implements hashable behavior.

    Attributes:
        location (Tuple[int, int]): The current position in the maze.
        board (Tuple[Tuple[MazeRoom]]): The board of rooms that make up the maze.
    """
    def __init__(self, board: List[List[MazeRoom]], location: Tuple[int, int]) -> None:
        self.location = location
        self.board = board

    def __eq__(self, other) -> bool:
        return self.location == other.location

    def __hash__(self) -> int:
        return hash((self.location))

    def __repr__(self) -> str:
        return f"State({self.location})"


class Maze(SearchProblem[MazeState]):
    """
    A class representing a maze, which can be used for both maze generation and solving.

    Attributes:
        width (int): The width of the maze.
        height (int): The height of the maze.
        board (List[List[MazeRoom]]): A 2D list representing the maze grid, where each cell is a MazeRoom.
        start_state (MazeState): The starting state of the maze.
        goal_state (MazeState): The goal state of the maze.

    Methods:
        generate_board(): Generates the maze by randomly carving out paths.
        drunken_walk(row, col): Recursively carves out a maze by randomly walking through the board, removing walls.
        is_in_bounds(row, col): Checks whether a given position is within the bounds of the maze.
        opposite_direction(direction): Returns the opposite direction of the given direction.
        visualize_maze(path=None, algorithm_name=None): Visualizes the maze and optionally overlays a path explored by a search algorithm.
        get_start_state(): Returns the start state of the maze.
        is_goal_state(state): Determines whether the goal state of the maze has been reached.
        get_successors(state): Generates the successor states from the current state in the maze.
    """
    def __init__(self, width: int, height: int, start: Optional[Tuple[int, int]] = None, goal: Optional[Tuple[int, int]] = None, self_generating: bool = True, board: Optional[List[List['MazeRoom']]] = None) -> None:
        self.width = width
        self.height = height

        if not board:
            self.board = [[MazeRoom() for _ in range(width)] for _ in range(height)]
        else:
            self.board = board

        # Set start and goal positions
        start_pos = start if start else (0, 0)
        goal_pos = goal if goal else (height - 1, width - 1)
        
        self.start_state = MazeState(self.board, start_pos)
        self.goal_state = MazeState(self.board, goal_pos)

        if self_generating:
            self.generate_board()

    def generate_board(self) -> None:
        """Generates the maze by randomly carving out paths using the drunken walk algorithm."""
        # Start generating the maze from a random start position
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.drunken_walk(start_y, start_x)
    
    def drunken_walk(self, row: int, col: int) -> None:
        """
        Recursively carves out a maze by randomly walking through the board, removing walls.

        Args:
            row (int): The current row in the board.
            col (int): The current column in the board.
        """
        directions = ['north', 'south', 'east', 'west']
        random.shuffle(directions)  # Shuffle directions to ensure randomness
        self.board[row][col].visited = True  # Mark the current cell as visited

        for direction in directions:
            nx, ny = col, row
            if direction == 'north':
                ny -= 1
            elif direction == 'south':
                ny += 1
            elif direction == 'east':
                nx += 1
            elif direction == 'west':
                nx -= 1

            if not self.is_in_bounds(ny, nx):
                setattr(self.board[row][col], direction, 1)  # Wall if out of bounds
            else:
                if not self.board[ny][nx].visited:
                    setattr(self.board[row][col], direction, 0)
                    setattr(self.board[ny][nx], self.opposite_direction(direction), 0)
                    self.drunken_walk(ny, nx)
    
    def is_in_bounds(self, row: int, col: int) -> bool:
        """
        Checks whether a given position is within the bounds of the maze.

        Args:
            row (int): The row index to check.
            col (int): The column index to check.

        Returns:
            bool: True if the position is within the maze's boundaries, False otherwise.
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def opposite_direction(self, direction: str) -> str:
        """
        Returns the opposite direction of the given direction.

        Args:
            direction (str): The direction for which the opposite is needed.

        Returns:
            str: The opposite direction.
        """
        return {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east'
        }[direction]

    def visualize_maze(self, path: Optional[List[MazeState]] = None, algorithm_name: Optional[str] = None) -> None:
        """
        Visualizes the maze and optionally overlays a path explored by a search algorithm.

        Args:
            path (Optional[Tuple[MazeState]]): The path to visualize within the maze.
            algorithm_name (Optional[str]): The name of the algorithm used to find the path.
        """
        _, ax = plt.subplots(figsize=(12, 8))

        if algorithm_name:
            ax.set_title(f"Path being explored by {algorithm_name}")
        else:
            ax.set_title("Maze Layout")

        for y in range(self.height):
            for x in range(self.width):
                room = self.board[y][x]
                if room.north == 1:
                    ax.plot([x, x+1], [y, y], color='black')
                if room.south == 1:
                    ax.plot([x, x+1], [y+1, y+1], color='black')
                if room.east == 1:
                    ax.plot([x+1, x+1], [y, y+1], color='black')
                if room.west == 1:
                    ax.plot([x, x], [y, y+1], color='black')

        if path:
            path_x = [p.location[1] + 0.5 for p in path]  # Center the path marker in the cell
            path_y = [p.location[0] + 0.5 for p in path]
            ax.plot(path_x, path_y, color='red', linewidth=2, marker='o', markersize=5)  # Draw the path in red

        plt.gca().invert_yaxis()  # Invert y-axis to match the maze's coordinate system
        plt.xticks([])
        plt.yticks([])
        plt.title(f"Path found by {algorithm_name}")
        plt.show()

    #### USE THESE FUNCTIONS IN YOUR SEARCH AND TESTING #########
    def get_start_state(self) -> MazeState:
        """
        Returns the start state of the maze, which is the entry point 
        for maze generation or solving algorithms.

        Returns:
            MazeState: The initial state of the maze.
        """
        return self.start_state

    def is_goal_state(self, state: MazeState) -> bool:
        """
        Determines whether the goal state of the maze has been reached.

        Args:
            state (MazeState): The current state of the maze.

        Returns:
            bool: True if the current state is the goal state, False otherwise.
        """
        return state == self.goal_state
    
    def get_successors(self, state: MazeState) -> Set[MazeState]:
        """
        Generates the successor states from the current state in the maze.

        This method checks all possible directions (north, south, east, west) from the current 
        position in the maze and adds valid moves to the set of successors. A move is considered 
        valid if there is no wall blocking the path in that direction.

        Args:
            state (MazeState): The current state of the maze.

        Returns:
            set[MazeState]: A set containing each valid successor state.
        """
        successors = set()
        row, col = state.location[0], state.location[1]
        board = state.board  # Access the board from the state

        # Check all possible directions and add valid moves to successors
        if board[row][col].north == 0:  # Move North
            next_state = MazeState(board, (row - 1, col))
            successors.add(next_state)

        if board[row][col].south == 0:  # Move South
            next_state = MazeState(board, (row + 1, col))
            successors.add(next_state)

        if board[row][col].east == 0:  # Move East
            next_state = MazeState(board, (row, col + 1))
            successors.add(next_state)

        if board[row][col].west == 0:  # Move West
            next_state = MazeState(board, (row, col - 1))
            successors.add(next_state)

        return successors