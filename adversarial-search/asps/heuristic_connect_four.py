from heuristic_adversarial_search_problem import HeuristicAdversarialSearchProblem
from .connect_four_problem import ConnectFourProblem, ConnectFourState
from . import connect_four_utils


class HeuristicConnectFourProblem(ConnectFourProblem, HeuristicAdversarialSearchProblem):

    def heuristic(self, state: ConnectFourState):
        """
        A heuristic function for Connect 4.
        Sum up point values for all possible slices of 4 adjacent cells.
        The heuristic is the difference between the scores of the two players.

        Note: Player 1 is maximizing, player 2 is minimizing.

        Inputs:
            state: a ConnectFourState object representing the current board
        Outputs:
            heuristic value of the state
        """
        board = state.board
        cols = board.shape[1]
        board_score = 0

        # Score all possible connect 4 "slices"
        for slice in connect_four_utils.all_connect_four_slices(board):
            # Add the score from player 1's perspective (maximizer)
            # Subtract the score from player 2's perspective (minimizer)
            board_score += self.evaluate_slice(
                list(slice), 0) - self.evaluate_slice(
                list(slice), 1)

        return board_score

    @staticmethod
    def evaluate_slice(slice, player_index):
        """
        Evaluate a specific slice (4 adjacent cells)
        100 points for 4 in a row, 5 points for 3 in a row, 2 points for 2 in a row.

        Prioritize getting slices with your pieces and open spaces.

        Inputs:
            slice: a list of 4 integers representing the 4 adjacent cells
            player_index: an integer representing the player index (0 or 1) who we are evaluating for.
        Outputs:
            score: an integer representing the score of the slice
        """
        score = 0
        if slice.count(player_index) == 4:
            score += 100
        elif slice.count(player_index) == 3 and slice.count(0) == 1:
            score += 5
        elif slice.count(player_index) == 2 and slice.count(0) == 2:
            score += 2
        return score