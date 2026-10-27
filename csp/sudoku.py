import argparse
import os
import random
from typing import List, Dict, Tuple, Optional, Any

import examples
import numpy as np
from sat_problem import CNF, Clause, Literal, Model, Variable
from sat_solvers import walksat, gsat
from vizualize import print_sudoku, visualize_sudoku

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Sudoku(CNF):
    """
    A class representing a Sudoku problem as a CNF formula.
    
    Supports different sized Sudoku problems (4x4, 9x9, 16x16, etc.)
    by encoding the standard Sudoku constraints as logical clauses.
    """

    def __init__(self, starting_grid: Optional[List[List[int]]] = None) -> None:
        """
        Initialize a Sudoku problem with the given starting configuration.
        
        Args:
            starting_grid: 2D list representing the initial Sudoku state.
                          0 represents empty cells. Defaults to empty 4x4 grid.
        """
        super().__init__()
        if starting_grid is None:
            starting_grid = [[0]*4]*4
        self.starting_grid = starting_grid
        self.size = len(self.starting_grid)
        self.subgrid_size = int(np.sqrt(self.size))

        self.compile()

    def compile(self) -> None:
        """
        Add clauses to the CNF formula encoding the Sudoku constraints.
        """

        # cache for Variables
        variable_cache: Dict[Tuple[int, int, int], Variable] = {}

        def get_variable(row: int, col: int, num: int) -> Variable:
            key = (row, col, num)
            if key not in variable_cache:
                variable_cache[key] = Variable(f'x_{row}_{col}_{num}')
            return variable_cache[key]
        
        # Cell constraints
        for row in range(self.size):
            for col in range(self.size):
                clause = Clause([Literal(get_variable(row, col, num), True) for num in range(1, self.size + 1)])
                self.add_clause(clause)

                for num1 in range(1, self.size + 1):
                    for num2 in range(num1 + 1, self.size + 1):
                        clause = Clause([Literal(get_variable(row, col, num1), False),
                                         Literal(get_variable(row, col, num2), False)])
                        self.add_clause(clause)
        # Row constraints
        for row in range(self.size):
            for num in range(1, self.size + 1):
                clause = Clause([Literal(get_variable(row, col, num), True) for col in range(self.size)])
                self.add_clause(clause)

                for col1 in range(self.size):
                    for col2 in range(col1 + 1, self.size):
                        clause = Clause([Literal(get_variable(row, col1, num), False),
                                         Literal(get_variable(row, col2, num), False)])
                        self.add_clause(clause)
        # Column constraints
        for col in range(self.size):
            for num in range(1, self.size + 1):
                clause = Clause([Literal(get_variable(row, col, num), True) for row in range(self.size)])
                self.add_clause(clause)

                for row1 in range(self.size):
                    for row2 in range(row1 + 1, self.size):
                        clause = Clause([Literal(get_variable(row1, col, num), False),
                                         Literal(get_variable(row2, col, num), False)])
                        self.add_clause(clause)
        # Box constraints
        for box_row in range(self.subgrid_size):
            for box_col in range(self.subgrid_size):
                for num in range(1, self.size + 1):
                    clause = Clause([Literal(get_variable(box_row * self.subgrid_size + i,
                                                          box_col * self.subgrid_size + j, num), True)
                                     for i in range(self.subgrid_size)
                                     for j in range(self.subgrid_size)])
                    self.add_clause(clause)

                    for i1 in range(self.subgrid_size):
                        for j1 in range(self.subgrid_size):
                            for i2 in range(self.subgrid_size):
                                for j2 in range(self.subgrid_size):
                                    if (i1, j1) < (i2, j2):
                                        clause = Clause([Literal(get_variable(box_row * self.subgrid_size + i1,
                                                                              box_col * self.subgrid_size + j1, num), False),
                                                         Literal(get_variable(box_row * self.subgrid_size + i2,
                                                                              box_col * self.subgrid_size + j2, num), False)])
                                        self.add_clause(clause)
    def get_board(self, solution: Model) -> List[List[int]]:
        """
        Convert a solution model to a Sudoku board representation.

        Args:
            solution: Model containing variable assignments for the solved Sudoku
            
        Returns:
            2D list representing the completed Sudoku board with numbers 1-N
        """
        assignments = solution.assignments
        solution_grid = [[0] * self.size for _ in range(self.size)]

        for var, value in assignments.items():
            if value == 1:
                _, row, col, num = str(var).split('_')
                row = int(row)
                col = int(col)
                num = int(num)

                solution_grid[row][col] = num

        return solution_grid


def main() -> None:
    """
    Main function to solve Sudoku puzzles using SAT solvers.
    
    Parses command line arguments and runs either GSAT or WalkSAT
    on a Sudoku puzzle of specified difficulty.
    """
    parser = argparse.ArgumentParser(
        description="Solve the N-Queens problem using a SAT solver.")
    parser.add_argument("-p", type=float, default=0.5,
                        help="Probability parameter for GSAT/WalkSAT (default: 0.5)")
    parser.add_argument("--randomized_restarts", type=int, default=1,
                        help="Number of randomized restarts to run (default: 1)")
    parser.add_argument("--max_iterations", type=int, default=10000,
                        help="Maximum number of iterations (default: 10000)")
    parser.add_argument("--solver", type=str, default="walksat",
                        help="Solver to use (walksat or gsat)")
    parser.add_argument("--difficulty", type=str, default="medium",
                        help="Difficulty level of the Sudoku puzzle (easy, medium, hard)")
    args = parser.parse_args()

    # Try on empty 9x9 grid
    example_start_grids = examples.get_sudoku_puzzles()
    starting_grid = example_start_grids[args.difficulty][0]
    problem = Sudoku(starting_grid)

    if args.solver == "gsat":
        print("Running GSAT...")
        solution, stats = gsat(problem, max_iterations=args.max_iterations,
                               p=args.p, num_randomized_restarts=args.randomized_restarts)
        if solution:
            print("Solution found!")
            board = problem.get_board(solution)
            print("Runtime:", stats['run_time'])
            print_sudoku(board)
        else:
            print("No solution found.")

    elif args.solver == "walksat":
        print("Running WalkSAT...")
        solution, stats = walksat(problem, max_iterations=args.max_iterations,
                                  p=args.p, num_randomized_restarts=args.randomized_restarts)
        if solution:
            print("Solution found!")
            board = problem.get_board(solution)
            print_sudoku(board)
            print("Runtime:", stats['run_time'])
            visualize_sudoku(board)
        else:
            print("No solution found.")


if __name__ == "__main__":
    random.seed(42)
    main()