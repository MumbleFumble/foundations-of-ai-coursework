import random
import time
import os
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Any, List

import numpy as np
import torch
from torch import nn

from go_search_problem import GoProblem, GoState, Action, HeuristicGoProblem
from heuristic_go_problems import GoProblemSimpleHeuristic, GoProblemLearnedHeuristic
from models import ValueNetwork, load_model
from adversarial_search import minimax, alpha_beta
from heuristic_go_problems import get_features

MAXIMIZER = 0
MIMIZER = 1

class GameAgent(ABC):
    """Abstract base class for all Go game agents."""
    
    @abstractmethod
    def get_move(self, state: GoState, time_limit: float) -> Action:
        """Get the best move for the given state within the time limit.
        
        Args:
            state: Current game state
            time_limit: Maximum time in seconds to spend on this move
            
        Returns:
            Action index representing the chosen move
        """
        pass

    def reset(self):
        """Reset any internal state of the agent if necessary.
            Called after a new game is started.
        """
        pass


class RandomAgent(GameAgent):
    # An Agent that makes random moves

    def __init__(self):
        self.search_problem = GoProblem()

    def get_move(self, game_state: GoState, time_limit: float) -> Action:
        """
        get random move for a given state
        """
        actions = self.search_problem.get_available_actions(game_state)
        return random.choice(actions)

    def __str__(self):
        return "RandomAgent"


class GreedyAgent(GameAgent):
    def __init__(self, search_problem=GoProblemSimpleHeuristic()):
        super().__init__()
        self.search_problem = search_problem

    def get_move(self, game_state: GoState, time_limit: float) -> Action:
        """
        get move of agent for given game state.
        Greedy agent looks one step ahead with the provided heuristic and chooses the best available action
        (Greedy agent does not consider remaining time)

        Args:
            game_state (GameState): current game state
            time_limit (float): time limit for agent to return a move
        """
        # Create new GoSearchProblem with provided heuristic
        search_problem = self.search_problem

        # Player 0 is maximizing
        if game_state.player_to_move() == MAXIMIZER:
            best_value = -float('inf')
        else:
            best_value = float('inf')
        best_action = None

        # Get Available actions
        actions = search_problem.get_available_actions(game_state)

        # Compare heuristic of every reachable next state
        for action in actions:
            new_state = search_problem.transition(game_state, action)
            value = search_problem.heuristic(new_state, new_state.player_to_move())
            if game_state.player_to_move() == MAXIMIZER:
                if value > best_value:
                    best_value = value
                    best_action = action
            else:
                if value < best_value:
                    best_value = value
                    best_action = action

        # Return best available action
        return best_action

    def __str__(self):
        """
        Description of agent (Greedy + heuristic/search problem used)
        """
        return "GreedyAgent + " + str(self.search_problem)

#############################################
# 
#
# Part 1: Basic Adversarial Search Algorithms
#
#
#############################################

class MinimaxAgent(GameAgent):
    def __init__(self, depth_cutoff=1, search_problem=GoProblemSimpleHeuristic()):
        super().__init__()
        self.depth = depth_cutoff
        self.search_problem = search_problem

    def get_move(self, game_state: GoState, time_limit: float) -> Action:
        """
        Get move of agent for given game state using minimax algorithm

        MinimaxAgents should not consider time limit, they simply search to their specified depth_cutoff
        If your agent is running out of time, you should use a shorter cutoff depth
        Args:
            game_state (GameState): current game state
            time_limit (float): time limit for agent to return a move
        Returns:
            best_action (Action): best action for current game state
        """
        self.search_problem.set_start_state(game_state)
        best_action, stats = minimax(self.search_problem, cutoff_depth=self.depth)
        return best_action

    def __str__(self):
        return f"MinimaxAgent w/ depth {self.depth} + " + str(self.search_problem)


class AlphaBetaAgent(GameAgent):
    def __init__(self, depth_cutoff=1, search_problem=GoProblemSimpleHeuristic()):
        super().__init__()
        self.depth = depth_cutoff
        self.search_problem = search_problem

    def get_move(self, game_state: GoState, time_limit: float) -> Action:
        """
        Get move of agent for given game state using alpha-beta algorithm

        AlphaBetaAgents should not consider time limit, they simply search to their specified depth_cutoff
        If your agent is running out of time, you should use a shorter cutoff depth

        Args:
            game_state (GameState): current game state
            time_limit (float): time limit for agent to return a move
        Returns:
            best_action (Action): best action for current game state
        """
        self.search_problem.set_start_state(game_state)
        best_action, stats = alpha_beta(self.search_problem, cutoff_depth=self.depth)
        return best_action

    def __str__(self):
        return f"AlphaBeta w/ depth {self.depth} + " + str(self.search_problem)



def create_value_agent_from_model():
    """
    Create agent object from saved model. 
    This (or other methods like this) will be how your agents will be created in gradescope and in the final tournament.

    In the game_runner file, there is a factory function that will call this function to create an agent.
    You can run games with your agent against other agents by running game_runner.py with the appropriate command line arguments.
    """
    
    
    # Model path
    model_path = "value_model.pt"

    # Get feature size from a sample state
    sample_problem = GoProblem(5)
    sample_state = sample_problem.get_start_state()
    features = get_features(sample_state)
    feature_size = len(features)
    
    # Load the trained model
    model = load_model(model_path, ValueNetwork(feature_size))
    
    # Create heuristic search problem with the learned model
    heuristic_search_problem = GoProblemLearnedHeuristic(model, size=5)

    # Use AlphaBetaAgent with depth 3 (safe depth from testing)
    learned_agent = AlphaBetaAgent(depth_cutoff=3, search_problem=heuristic_search_problem)

    return learned_agent


################################################
#
# Part 2: Advanced Adversarial Search Algorithms
#
################################################

class IterativeDeepeningAgent(GameAgent):
    def __init__(self, cutoff_time=1, search_problem=GoProblemSimpleHeuristic()):
        super().__init__()
        self.cutoff_time = cutoff_time
        self.search_problem = search_problem

    def get_move(self, game_state, time_limit):
        """
        Get move of agent for given game state using iterative deepening algorithm (+ alpha-beta).
        Iterative deepening is a search algorithm that repeatedly searches for a solution to a problem,
        increasing the depth of the search with each iteration.

        The advantage of iterative deepening is that you can stop the search based on the time limit, rather than depth.
        The recommended approach is to modify your implementation of Alpha-beta to stop when the time limit is reached
        and run IDS on that modified version.

        Args:
            game_state (GameState): current game state
            time_limit (float): time limit for agent to return a move
        Returns:
            best_action (Action): best action for current game state
        """
        start_time = time.time()
        time_cushion = max(0.2, time_limit * 0.25)
        max_time = time_limit - time_cushion
        
        best_action = None
        depth = 1
        
        actions = self.search_problem.get_available_actions(game_state)
        if actions:
            best_action = actions[0]
        
        while True:
            time_remaining = max_time - (time.time() - start_time)
            
            if time_remaining <= 0:
                break
            
            action = self._alpha_beta_with_time(
                game_state, 
                depth, 
                start_time, 
                max_time
            )
            
            if action is not None:
                best_action = action
                depth += 1
            else:
                break
        
        return best_action

    def _alpha_beta_with_time(self, root_state, cutoff_depth, start_time, max_time):
        """
        Alpha-beta pruning with time constraints.
        Returns None if time runs out, otherwise returns best action.
        """
        best_action = None
        best_value = None
        alpha = -float("inf")
        beta = float("inf")
        player = root_state.player_to_move()
        
        actions = self.search_problem.get_available_actions(root_state)
        
        for action in actions:
            if time.time() - start_time >= max_time:
                return None
            
            successor = self.search_problem.transition(root_state, action)
            val = self._alpha_beta_helper(
                successor, 
                1, 
                cutoff_depth, 
                alpha, 
                beta, 
                start_time, 
                max_time
            )
            
            if val is None:
                return None
            
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
        
        return best_action

    def _alpha_beta_helper(self, state, depth, cutoff_depth, alpha, beta, start_time, max_time):
        """
        Recursive alpha-beta helper with time checking.
        Returns None if time runs out.
        """
        if time.time() - start_time >= max_time:
            return None
        
        if self.search_problem.is_terminal_state(state):
            return self.search_problem.get_result(state)
        
        if depth >= cutoff_depth:
            return self.search_problem.heuristic(state, state.player_to_move())
        
        player = state.player_to_move()
        actions = self.search_problem.get_available_actions(state)
        
        if player == 0:
            value = -float("inf")
            for action in actions:
                if time.time() - start_time >= max_time:
                    return None
                child = self.search_problem.transition(state, action)
                child_val = self._alpha_beta_helper(
                    child, depth + 1, cutoff_depth, alpha, beta, start_time, max_time
                )
                if child_val is None:
                    return None
                value = max(value, child_val)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for action in actions:
                if time.time() - start_time >= max_time:
                    return None
                child = self.search_problem.transition(state, action)
                child_val = self._alpha_beta_helper(
                    child, depth + 1, cutoff_depth, alpha, beta, start_time, max_time
                )
                if child_val is None:
                    return None
                value = min(value, child_val)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def __str__(self):
        return f"IterativeDeepneing + " + str(self.search_problem)
    

class MCTSNode:
    def __init__(self, state, parent=None, children=None, action=None):
        # GameState for Node
        self.state = state

        # Parent (MCTSNode)
        self.parent = parent
        
        # Children List of MCTSNodes
        if children is None:
            children = []
        self.children = children
        
        # Number of times this node has been visited in tree search
        self.visits = 0
        
        # Value of node (number of times simulations from children results in win)
        self.value = 0
        
        # Action that led to this node
        self.action = action

    def __hash__(self):
        """
        Hash function for MCTSNode is hash of state
        """
        return hash(self.state)
    
import concurrent.futures

class MCTSAgentV0(GameAgent):
    def __init__(self, c=np.sqrt(2),value_model = None):
        """
        Args: 
            c (float): exploration constant of UCT algorithm
        """
        super().__init__()
        self.c = c
        
        # Initialize Search problem
        self.search_problem = GoProblem()
        # initiate last root and buffer time. I use last root for my graphing
        self.last_root = None
        self.buffer_time = 0.25
        
        # Load value model if not provided
        if value_model is None:
            model_path = "value_model.pt"
            if os.path.exists(model_path):
                try:
                    # 5x5 board has 53 features
                    self.value_model = ValueNetwork(53)
                    self.value_model = load_model(model_path, self.value_model)
                    self.value_model.eval() # Set to eval mode
                except Exception as e:
                    self.value_model = None
            else:
                self.value_model = None
        else:
            self.value_model = value_model

    def get_move(self, game_state: GoState, time_limit: float) -> Action:
        """
        Get move of agent for given game state using MCTS algorithm
        
        Args:
            game_state (GameState): current game state
            time_limit (float): time limit for agent to return a move
        Returns:
            best_action (Action): best action for current game state
        """
        # 0. Hybrid Strategy: Switch to IDS for endgame (last 9 moves)
        # Only use Hybrid Strategy if we have a valid model (5x5) or if we trust the heuristic
        # For 9x9, simple heuristic is too weak, so we skip hybrid unless we have a 9x9 model
        empty_points_count = np.sum(game_state.get_empty_spaces())
        
        if empty_points_count <= 9 and game_state.size == 5:
            # Use IDS with Value Heuristic (if available) for exact endgame search
            if self.value_model is not None:
                search_prob = GoProblemLearnedHeuristic(model=self.value_model)
            else:
                search_prob = GoProblemSimpleHeuristic()
            
            # Custom IDS implementation to maximize time usage
            start_time = time.time()
            # Use almost all remaining time, leaving just a small buffer
            # In endgame, we want to solve the game, so we spend aggressively
            time_cushion = 0.2
            max_time = time_limit - time_cushion
            
            best_action = None
            depth = 1
            
            # Get initial best action (greedy)
            actions = search_prob.get_available_actions(game_state)
            if actions:
                best_action = actions[0]
            
            # Iterative Deepening Loop
            while True:
                time_remaining = max_time - (time.time() - start_time)
                if time_remaining <= 0:
                    break
                
                # Use the helper from IterativeDeepeningAgent (we can instantiate it to use its methods)
                # Or just use alpha_beta directly if we want to control it
                # Let's use a temporary agent to reuse the logic but with our time control
                temp_agent = IterativeDeepeningAgent(search_problem=search_prob)
                
                # We call the internal helper directly to avoid the cushion logic of the agent
                action = temp_agent._alpha_beta_with_time(
                    game_state, 
                    depth, 
                    start_time, 
                    max_time
                )
                
                if action is not None:
                    best_action = action
                    depth += 1
                else:
                    break
            
            return best_action

        # 1. Time Management
        # Estimate remaining moves (empty / 2)
        est_remaining_moves = max(1, empty_points_count / 2)
        
        # Base allocation
        allocation = time_limit / est_remaining_moves
        
        # Safety factor (Aggressive)
        if time_limit > 5:
            allocation *= 0.95
        else:
            allocation *= 0.98
            
        # Cap at 98% of remaining time to avoid timeout
        allocation = min(allocation, time_limit * 0.98)
        
        # Set deadline
        start_time = time.time()
        self.deadline = start_time + allocation

        root = MCTSNode(state=game_state)
        self.last_root = root
        
        iteration_count = 0
        player = game_state.player_to_move()
        
        # while time remaining select, expand, simulate then backpropagate
        while time.time() < self.deadline:
            # Check time before each iteration
            if time.time() >= self.deadline:
                break
            
            iteration_count += 1
            leaf = self.select(root)
            
            # Check time before expand
            if time.time() >= self.deadline:
                break
            
            children = self.expand(leaf)
            
            # Check time before simulate
            if time.time() >= self.deadline:
                break
            
            # Simulate ALL children using batch processing (much more accurate)
            if children:
                results = self.simulate(children)
                self.backpropagate(children, results)

        elapsed = time.time() - start_time
        
        # choose the most visited root
        if not root.children:
            return self.search_problem.get_available_actions(game_state)[-1]
        
        # best child
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.action

    def select(self, node: MCTSNode) -> MCTSNode:
        """
        SELECT: Start at root, repeatedly choose child with highest UCT until reaching a leaf.
        
        Args:
            node: Starting node (root)
        Returns:
            A leaf node (no children) or terminal node
        """
        current = node
        
        while len(current.children) > 0:
            if self.search_problem.is_terminal_state(current.state):
                return current
            
            # Calculate total visits across all children
            total = sum(child.visits for child in current.children) + 1
            
            # Choose child with highest UCT value
            current = max(
                current.children,
                key=lambda child: self.uct(child, total)
            )
        
        return current

    def uct(self, node: MCTSNode, parent_visits: int) -> float:
        """
        Calculate UCT value for a node.
        Since node tracks wins for its own player (opponent of parent),
        we want LOW win rate (good for us = bad for opponent).
        
        UCT(s) = (1 - w/n) + c * sqrt(ln(N)/n)
        
        Args:
            node: Node to calculate UCT for
            parent_visits: Number of visits to parent node
        Returns:
            UCT value
        """
        if node.visits == 0:
            return float('inf')
        
        # Standard UCT: prefer HIGH win rate (value tracks parent player's wins)
        win_rate = node.value / node.visits
        exploration = self.c * np.sqrt(np.log(parent_visits) / node.visits)
        uct_score = win_rate + exploration
        
        # Debug UCT calculation (uncomment to enable)
        # if np.random.rand() < 0.001:
        #     print(f"  [UCT] Action {node.action}: visits={node.visits}, value={node.value}, win_rate={win_rate:.3f}, exploration={exploration:.3f}, UCT={uct_score:.3f}")
        
        return uct_score

    def expand(self, node: MCTSNode) -> list:
        """
        EXPAND: Generate ALL legal actions and create child nodes.
        Per spec: if terminal, return [leaf] to still backpropagate.
        
        Args:
            node: Leaf node to expand
        Returns:
            List of new children (or [node] if terminal)
        """
        if self.search_problem.is_terminal_state(node.state):
            return [node]
        
        actions = self.search_problem.get_available_actions(node.state)
        
        for action in actions:
            child_state = self.search_problem.transition(node.state, action)
            child_node = MCTSNode(child_state, parent=node, action=action)
            node.children.append(child_node)
        
        return node.children

    def simulate(self, children: list) -> list:
        """
        SIMULATE: Evaluate children using Value Network, Heuristic, or Random Rollout.
        Optimized for batch processing with Value Network.
        
        Args:
            children: List of child nodes to simulate
        Returns:
            List of results (values from BLACK's perspective, [-1, 1])
        """
        results = [None] * len(children)
        nn_indices = []
        nn_features = []
        
        # Check if we can use the model (must be 5x5)
        use_model = (self.value_model is not None)
        if children and children[0].state.size != 5:
            use_model = False
        
        # 1. Identify terminal states and prepare NN batch
        for i, child in enumerate(children):
            # Check time periodically (not every child to save overhead)
            if i % 5 == 0 and time.time() >= self.deadline:
                break
                
            state = child.state
            
            if self.search_problem.is_terminal_state(state):
                results[i] = self.search_problem.get_result(state)
            elif use_model:
                try:
                    nn_indices.append(i)
                    nn_features.append(get_features(state))
                except Exception:
                    # Fallback to heuristic if feature extraction fails
                    heuristic_val = GoProblemSimpleHeuristic().heuristic(state, 0)
                    results[i] = np.tanh(heuristic_val / 2.0)
            else:
                # Fallback to heuristic if no model
                heuristic_val = GoProblemSimpleHeuristic().heuristic(state, 0)
                results[i] = np.tanh(heuristic_val / 2.0)
        
        # 2. Run Value Network in batch
        if nn_indices:
            try:
                features_tensor = torch.tensor(nn_features, dtype=torch.float32)
                with torch.no_grad():
                    values = self.value_model(features_tensor).numpy().flatten()
                
                for idx, val in zip(nn_indices, values):
                    results[idx] = np.clip(val, -1, 1)
            except Exception as e:
                # Fallback if batch fails
                for idx in nn_indices:
                    heuristic_val = GoProblemSimpleHeuristic().heuristic(children[idx].state, 0)
                    results[idx] = np.tanh(heuristic_val / 2.0)

        # 3. Fill any remaining Nones (e.g. if time ran out or logic gap)
        # This ensures we return a list of same length as children
        final_results = []
        for i in range(len(children)):
            if results[i] is not None:
                final_results.append(results[i])
            else:
                # Default neutral value if something went wrong or time out
                final_results.append(0.0)
                
        return final_results

    def backpropagate(self, children: list, results: list):
        """
        BACKPROPAGATE: Update visits and values up to root.
        Value tracks wins for the node's parent player.
        
        Args:
            children: List of child nodes
            results: List of simulation results (values from BLACK's perspective, [-1, 1])
        """
        for child, result in zip(children, results):
            curr = child
            
            # Convert result (Black's perspective [-1, 1]) to [0, 1] probability of Black winning
            prob_black_win = (result + 1) / 2.0
            
            while curr is not None:
                curr.visits += 1
                
                # curr.state.player_to_move() is the player who will move NEXT.
                # So the player who just moved (and chose curr) is the OPPONENT.
                # We want to update the value for the player who chose curr.
                
                next_player = curr.state.player_to_move()
                
                if next_player == 1: # White to move, so Black just moved
                    # We want to add Black's win probability
                    curr.value += prob_black_win
                else: # Black to move, so White just moved
                    # We want to add White's win probability
                    curr.value += (1.0 - prob_black_win)
                
                curr = curr.parent

    def best_action(self, root: MCTSNode) -> Action:
        """
        Select the best action from root node.
        Returns the action of the child with the most visits (per spec).
        
        Args:
            root: Root node of MCTS tree
        Returns:
            Action with most visits
        """
        if not root.children:
            actions = self.search_problem.get_available_actions(root.state)
            return random.choice(actions) if actions else None
        
        # Select child with most visits (per spec requirement)
        best_child = max(root.children, key=lambda child: child.visits)
        
        return best_child.action

    def __str__(self):
        return "FINALV0 (single)"

class MCTSAgentV1(MCTSAgentV0):
    def __init__(self, c=np.sqrt(2), value_model=None):
        super().__init__(c, value_model)
        # Use ThreadPoolExecutor for parallel simulations
        # Max workers can be tuned. 4 is usually a safe bet for desktop CPUs.
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def simulate(self, children: list) -> list:
        """
        SIMULATE: Evaluate children using Multithreading.
        Overrides the single-threaded simulate method.
        """
        # Check if we can use the model (must be 5x5)
        use_model = (self.value_model is not None)
        if children and children[0].state.size != 5:
            use_model = False
            
        # If using model (5x5), stick to batch processing (it's faster than threading for NN)
        if use_model:
            return super().simulate(children)
            
        # For 9x9 (Heuristic), use Threading
        # Define helper function for single simulation
        def evaluate_child(child):
            state = child.state
            if self.search_problem.is_terminal_state(state):
                return self.search_problem.get_result(state)
            else:
                # Fallback to heuristic
                heuristic_val = GoProblemSimpleHeuristic().heuristic(state, 0)
                return np.tanh(heuristic_val / 2.0)

        # Submit all children to executor
        # We map the function over the children list
        # This runs evaluations in parallel
        try:
            results = list(self.executor.map(evaluate_child, children))
        except Exception as e:
            # Fallback to sequential if threading fails
            results = []
            for child in children:
                results.append(evaluate_child(child))
                
        return results

    def __str__(self):
        return "FINALV1 (threaded)"

class MCTSAgentV2(MCTSAgentV1):
    def __init__(self, c=np.sqrt(2), value_model=None, rollout_limit=10):
        super().__init__(c, value_model)
        self.rollout_limit = rollout_limit

    def simulate(self, children: list) -> list:
        """
        SIMULATE: Evaluate children using Multithreading with Rollouts.
        """
        # Check if we can use the model (must be 5x5)
        use_model = (self.value_model is not None)
        if children and children[0].state.size != 5:
            use_model = False
            
        # If using model (5x5), stick to batch processing
        if use_model:
            return super(MCTSAgentV0, self).simulate(children) # Call V0's simulate
            
        # For 9x9, use Threading with Rollouts
        def evaluate_child_with_rollout(child):
            state = child.state.clone() # Clone to avoid modifying tree state
            
            # 1. Check immediate terminal
            if self.search_problem.is_terminal_state(state):
                return self.search_problem.get_result(state)
            
            # 2. Perform Rollout
            moves_simulated = 0
            while not self.search_problem.is_terminal_state(state) and moves_simulated < self.rollout_limit:
                actions = self.search_problem.get_available_actions(state)
                if not actions:
                    break
                # Random move
                action = random.choice(actions)
                state = self.search_problem.transition(state, action)
                moves_simulated += 1
            
            # 3. Evaluate Final State
            if self.search_problem.is_terminal_state(state):
                return self.search_problem.get_result(state)
            else:
                # Heuristic at cutoff
                heuristic_val = GoProblemSimpleHeuristic().heuristic(state, 0)
                return np.tanh(heuristic_val / 2.0)

        # Submit all children to executor
        try:
            results = list(self.executor.map(evaluate_child_with_rollout, children))
        except Exception as e:
            results = []
            for child in children:
                results.append(evaluate_child_with_rollout(child))
                
        return results

    def __str__(self):
        return "FINALV2 (threaded+rollout)"

# Alias for backward compatibility
MCTSAgent = MCTSAgentV2
    

###################################################
#
# Part 3: Final Agent
#
###################################################

def get_final_agent_5x5():
    """Called to construct agent for final submission for 5x5 board"""
    return None
def get_final_agent_9x9():
    """Called to construct agent for final submission for 9x9 board"""
    return MCTSAgent()
