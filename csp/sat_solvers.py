import time
from typing import Optional, Tuple, Dict, List, Any
from sat_problem import CNF, Model, Variable
import random
import matplotlib.pyplot as plt
import tqdm
import copy


def randomly_assign_model(model: Model) -> None:
    """
        Randomly assign each variable in model to either a 0 or 1 with uniform probability.
    """
    for lit in model.variables:
        model.assignments[lit] = random.choice([0, 1])


def gsat(cnf_formula: CNF, max_iterations: int = 10000, p: float = 0.5, num_randomized_restarts: int = 1, existing_model: Optional[Model] = None) -> Tuple[Optional[Model], Dict[str, Any]]:
    """
    Implements the GSAT (Greedy-SAT) algorithm for solving SAT problems.
    
    GSAT uses a greedy approach with random restarts to search for satisfying
    assignments. At each step, it either randomly flips a variable (exploration)
    or greedily flips the variable that maximizes satisfied clauses (exploitation).

    Args:
        cnf_formula: A CNF formula to solve
        max_iterations: Maximum number of variable flips to perform
        p: Probability of choosing a random variable to flip (vs greedy choice)
        num_randomized_restarts: Number of random restarts to attempt
        existing_model: Optional starting model (used primarily for testing)

    Returns:
        Tuple containing:
            - Model that satisfies the CNF formula (None if no solution found)
            - Dictionary with run statistics:
                * num_iterations: Number of iterations performed
                * num_unsatisfied_clauses: List of unsatisfied clause counts per iteration
                * run_time: Total execution time
    """

    stats: Dict[str, Any] = {
        'num_iterations': 0,
        'num_unsatisfied_clauses': [],
        'run_time': 0
    }

    start_time = time.time()
    for restarts in range(num_randomized_restarts):
        if restarts == 0 and existing_model is not None:
            model = existing_model
        else:
            model = Model(cnf_formula)
            randomly_assign_model(model)

        for i in range(max_iterations):
            stats['num_iterations'] += 1
            unsatisfied_clauses = model.get_unsatisfied_clauses()
            num_unsatisfied = len(unsatisfied_clauses)
            stats['num_unsatisfied_clauses'].append(num_unsatisfied)

            if num_unsatisfied == 0:
                stats['run_time'] = time.time() - start_time
                return model, stats

            if random.random() < p:
                flip_var = random.choice(list(model.variables))
                model.flip(flip_var)
            else:
                best_var = None
                best_num_unsatisfied = num_unsatisfied

                for var in model.variables:
                    model.flip(var)
                    num_unsatisfied = len(model.get_unsatisfied_clauses())
                    if num_unsatisfied < best_num_unsatisfied:
                        best_num_unsatisfied = num_unsatisfied
                        best_var = var
                    model.flip(var)

                if best_var is not None:
                    model.flip(best_var)
    stats['run_time'] = time.time() - start_time
    return None, stats



def walksat(cnf_formula: CNF, max_iterations: int = 100000, p: float = 0.5, num_randomized_restarts: int = 1, existing_model: Optional[Model] = None) -> Tuple[Optional[Model], Dict[str, Any]]:
    """
    Implements the WalkSAT algorithm for solving SAT problems.
    
    WalkSAT focuses on unsatisfied clauses by selecting a random unsatisfied
    clause and then either randomly flipping a variable in that clause or
    greedily choosing the variable that maximizes satisfied clauses.

    Args:
        cnf_formula: A CNF formula to solve
        max_iterations: Maximum number of variable flips to perform
        p: Probability of choosing a random variable to flip (vs greedy choice)
        num_randomized_restarts: Number of random restarts to attempt
        existing_model: Optional starting model (used primarily for testing)

    Returns:
        Tuple containing:
            - Model that satisfies the CNF formula (None if no solution found)
            - Dictionary with run statistics:
                * num_iterations: Number of iterations performed
                * num_unsatisfied_clauses: List of unsatisfied clause counts per iteration
                * run_time: Total execution time
    """
    stats: Dict[str, Any] = {
        'num_iterations': 0,
        'num_unsatisfied_clauses': [],
        'run_time': 0
    }

    start_time = time.time()

    for restarts in range(num_randomized_restarts):
        if restarts == 0 and existing_model is not None:
            model = existing_model
        else:
            model = Model(cnf_formula)
            randomly_assign_model(model)

        for i in range(max_iterations):
            stats['num_iterations'] += 1
            unsatisfied_clauses = model.get_unsatisfied_clauses()
            num_unsatisfied = len(unsatisfied_clauses)
            stats['num_unsatisfied_clauses'].append(num_unsatisfied)

            if num_unsatisfied == 0:
                stats['run_time'] = time.time() - start_time
                return model, stats

            clause = random.choice(model.get_unsatisfied_clauses())
            if clause is None:
                continue

            if random.random() < p:
                flip_var = random.choice(clause.get_variables())
                model.flip(flip_var)
            else:
                best_var = None
                best_num_unsatisfied = num_unsatisfied

                for var in clause.get_variables():
                    model.flip(var)
                    num_unsatisfied = len(model.get_unsatisfied_clauses())
                    if num_unsatisfied < best_num_unsatisfied:
                        best_num_unsatisfied = num_unsatisfied
                        best_var = var
                    model.flip(var)

                if best_var is not None:
                    model.flip(best_var)
    
    stats['run_time'] = time.time() - start_time
    return None, stats