from typing import Optional, Any, Union
import numpy as np
import torch
from go_search_problem import GoState, HeuristicGoProblem
BLACK = 0
WHITE = 1

def get_features(game_state):
    """
    Map a game state to a list of features.
    
    Input:
        game_state: dict or GoState to encode into a fixed size list of features
    Output:
        features: list of features (53 for 5x5 board)
    """
    # Handle both dict format (from dataset) and GoState objects
    if isinstance(game_state, dict):
        board = game_state["board"]
        white_board = board[0]  
        black_board = board[1]
        player_to_move = game_state["player_to_move"]
        white_count = len(game_state["white_pieces"])
        black_count = len(game_state["black_pieces"])
    else:
        # GoState object
        board = game_state.get_board()
        white_board = board[0]
        black_board = board[1]
        player_to_move = game_state.player_to_move()
        white_count = len(game_state.get_pieces_coordinates(1))
        black_count = len(game_state.get_pieces_coordinates(0))

    features = []
    # Add all board positions (50 features for 5x5)
    features.extend(white_board.flatten().tolist())
    features.extend(black_board.flatten().tolist())
    
    # Add metadata features
    features.append(player_to_move)
    features.append(1 if white_count > black_count else 0)
    features.append(1 if black_count > white_count else 0)
    
    return features

class GoProblemSimpleHeuristic(HeuristicGoProblem):
    def __init__(self, size: int = 5, state=None, player_to_move: int = 0):
        super().__init__(size=size, state=state, player_to_move=player_to_move)

    def heuristic(self, state, player_index):
        """
        Very simple heuristic that just compares the number of pieces for each player
        
        Having more pieces than the opponent means that some were captured, capturing is generally good.
        Returns value from BLACK's perspective: positive = good for BLACK, negative = good for WHITE.
        """
        black_stones = len(state.get_pieces_coordinates(BLACK))
        white_stones = len(state.get_pieces_coordinates(WHITE))

        return black_stones - white_stones

    def __str__(self) -> str:
        return "Simple Heuristic"


class GoProblemLearnedHeuristic(HeuristicGoProblem):
    def __init__(self, model=None, size: int = 5, state=None, player_to_move: int = 0):
        super().__init__(size=size, state=state, player_to_move=player_to_move)
        self.model = model

    def encoding(self, state):
        """
        Get encoding of state (convert state to features)
        
        Input:
            state: GoState to encode into a fixed size list of features
        Output:
            features: list of features
        """
        features = get_features(state)
        return features

    def heuristic(self, state, player_index):
        """
        Return heuristic (value) of current state
        
        Input:
            state: GoState to encode into a fixed size list of features
            player_index: index of player to evaluate heuristic for
        Output:
            value: heuristic (value) of current state
        """
        # Get features and convert to tensor
        features = self.encoding(state)
        features_tensor = torch.tensor(features, dtype=torch.float32)
        
        # Get model prediction
        self.model.eval()
        with torch.no_grad():
            value = self.model(features_tensor).item()
        
        # The model outputs value from BLACK's perspective
        # If we're evaluating for WHITE (player_index=1), negate the value
        if player_index == 1:
            value = -value

        return value

    def __str__(self) -> str:
        return "Learned Heuristic"
