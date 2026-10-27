from typing import Dict, Tuple, Optional, Union

from adversarial_search_problem import (
    Action,
    State as GameState,
)
from go_search_problem import HeuristicGoProblem



def minimax(asp: HeuristicGoProblem, cutoff_depth: float = float('inf')) -> Tuple[Action, Dict[str, int]]:
    """
    Implement the minimax algorithm for adversarial search problems.
    
    Minimax is a recursive algorithm used for finding the optimal move in two-player,
    zero-sum games. It assumes both players play optimally by maximizing their own
    score and minimizing their opponent's score.

    Args:
        asp: A HeuristicGoProblem representing the game.
        cutoff_depth: Maximum search depth (0 = start state, 1 = one move ahead).
                     Uses heuristic evaluation when cutoff is reached.

    Returns:
        Tuple containing:
            - Best action to take from the current state
            - Dictionary with search statistics including 'states_expanded'
    """
    best_action = None
    best_value = None 
    stats = {
        'states_expanded': 0
    }
    start_state = asp.get_start_state()

    def minimax_helper(state: GameState, depth: int) -> float:
        if asp.is_terminal_state(state):
            return asp.get_result(state)
        if depth >= cutoff_depth:
            return asp.heuristic(state, state.player_to_move())
        stats["states_expanded"] += 1
        player = state.player_to_move()
        actions = asp.get_available_actions(state)
        if player == 0:  # Maximizing 
            return max(
                minimax_helper(asp.transition(state, a), depth + 1) for a in actions
            )
        else:  # Minimizing 
            return min(
                minimax_helper(asp.transition(state, a), depth + 1) for a in actions
            )

    # Choose the best move for the current player
    player = start_state.player_to_move()
    for action in asp.get_available_actions(start_state):
        successor = asp.transition(start_state, action)
        val = minimax_helper(successor, 1)
        if best_action is None:
            best_action, best_value = action, val
        else:
            if player == 0 and val > best_value:
                best_action, best_value = action, val
            elif player == 1 and val < best_value:
                best_action, best_value = action, val

    return best_action, stats
    


def alpha_beta(asp: HeuristicGoProblem, cutoff_depth: float = float('inf')) -> Tuple[Action, Dict[str, int]]:
    """
    Implements the alpha-beta pruning algorithm for adversarial search.
    
    Alpha-beta pruning is an optimization of the minimax algorithm that eliminates
    branches that cannot possibly influence the final decision. It maintains two
    values (alpha and beta) representing the best options found so far for the
    maximizing and minimizing players respectively.

    Args:
        asp: A HeuristicGoProblem representing the game.
        cutoff_depth: Maximum search depth (0 = start state, 1 = one move ahead).
                     Uses heuristic evaluation when cutoff is reached.

    Returns:
        Tuple containing:
            - Best action to take from the current state
            - Dictionary with search statistics including 'states_expanded'
    """
    best_action = None
    alpha = -float("inf")
    beta = float("inf")
    stats = {
        'states_expanded': 0  # Increase by 1 for every state transition
    }
    start_state = asp.get_start_state()

    def alpha_beta_helper(state: GameState, depth: int, alpha: float, beta: float) -> float:
        if asp.is_terminal_state(state):
            return asp.get_result(state)
        if depth >= cutoff_depth:
            return asp.heuristic(state, state.player_to_move())

        stats["states_expanded"] += 1
        player = state.player_to_move()
        if player == 0:
            value = -float("inf")
            for a in asp.get_available_actions(state):
                child = asp.transition(state, a)
                value = max(value, alpha_beta_helper(child, depth + 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for a in asp.get_available_actions(state):
                child = asp.transition(state, a)
                value = min(value, alpha_beta_helper(child, depth + 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    player = start_state.player_to_move()
    for action in asp.get_available_actions(start_state):
        successor = asp.transition(start_state, action)
        val = alpha_beta_helper(successor, 1, alpha, beta)
        if best_action is None:
            best_action, best_value = action, val
        else:
            if player == 0 and val > best_value:
                best_action, best_value = action, val
            elif player == 1 and val < best_value:
                best_action, best_value = action, val

        if player == 0:
            alpha = max(alpha, best_value)
        else:
            beta = min(beta, best_value)

    return best_action, stats
