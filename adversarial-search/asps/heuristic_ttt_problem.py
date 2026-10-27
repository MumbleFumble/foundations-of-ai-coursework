from heuristic_adversarial_search_problem import HeuristicAdversarialSearchProblem
from .ttt_problem import TTTState, TTTProblem

SPACE = " "
X = "X"  # Player 0 is X
O = "O"  # Player 1 is O
PLAYER_SYMBOLS = [X, O]


class HeuristicTTTProblem(TTTProblem, HeuristicAdversarialSearchProblem):

    def heuristic(self, state: TTTState) -> float:
        """
        TODO: Fill this out with your own heuristic function! You should make sure that this
        function works with boards of any size; if it only works for 3x3 boards, you won't be
        able to properly test ab-cutoff for larger board sizes!
        """
        #If it still could lead to a win for the current player (no opponent symbols block it), score it positively, the closer the more points.
        #If it still could lead to a win for the opponent, score it negatively. pretty basic but it worked a bit better than the other idea
        # of using just hwo had the longest chain on the board.

        board = state.board
        size = len(board)
        player_symbol = PLAYER_SYMBOLS[state.player_to_move()]
        opponent_symbol = PLAYER_SYMBOLS[1 - state.player_to_move()]
        heuristic = 0
        def evaluate_line(line, heuristic):
            if player_symbol in line and opponent_symbol in line:
                return
            if player_symbol in line:
                count = sum(1 for cell in line if cell == player_symbol)
                heuristic += pow(10, count)
            elif opponent_symbol in line:
                count = sum(1 for cell in line if cell == opponent_symbol)
                heuristic -= pow(10, count)

        for i in range(size):
            evaluate_line(board[i], heuristic)
            evaluate_line([board[r][i] for r in range(size)], heuristic)

        evaluate_line([board[i][i] for i in range(size)], heuristic)
        evaluate_line([board[i][size - 1 - i] for i in range(size)], heuristic)
        return heuristic
