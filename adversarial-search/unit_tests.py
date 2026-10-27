
import unittest

from asps.game_dag import DAGState, GameDAG
from adversarial_search import alpha_beta, minimax


class IOTest(unittest.TestCase):
    """
    Tests IO for adversarial search implementations.
    Contains both DAG validity checks and optimality tests for Tic Tac Toe.
    """

    def _check_result(self, result: object, dag: GameDAG) -> None:
        """
        Tests whether the result is one of the possible actions of the DAG.
        """
        self.assertIsNotNone(result, "Output should not be None")
        start_state = dag.get_start_state()
        potential_actions = dag.get_available_actions(start_state)
        self.assertIn(result, potential_actions, "Output should be an available action")

    def test_minimax_dag(self) -> None:
        """Minimax returns a valid action on a simple GameDAG."""
        X = True
        _ = False
        matrix = [
            [_, X, X, _, _, _, _],
            [_, _, _, X, X, _, _],
            [_, _, _, _, _, X, X],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
        ]
        start_state = DAGState(0, 0)
        terminal_evaluations = {3: -1., 4: -2., 5: -3., 6: -4.}

        dag = GameDAG(matrix, start_state, terminal_evaluations)
        result, _ = minimax(dag)
        self._check_result(result, dag)

    def test_alpha_beta_dag(self) -> None:
        """Alpha-beta returns a valid action on a simple GameDAG."""
        X = True
        _ = False
        matrix = [
            [_, X, X, _, _, _, _],
            [_, _, _, X, X, _, _],
            [_, _, _, _, _, X, X],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
        ]
        start_state = DAGState(0, 0)
        terminal_evaluations = {3: -1., 4: -2., 5: -3., 6: -4.}

        dag = GameDAG(matrix, start_state, terminal_evaluations)
        result, _ = alpha_beta(dag)
        self._check_result(result, dag)

    def test_minimax_optimal_choice(self) -> None:
        matrix = [
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        start_state = DAGState(0, 0)
        terminal_evaluations = {3: -5., 4: 7.}

        dag = GameDAG(matrix, start_state, terminal_evaluations)

        action, _ = minimax(dag)
        assert action == 2, f"Expected action 2 (value 7), got {action}"

    def test_alpha_beta_optimal_choice(self) -> None:
        matrix = [
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        start_state = DAGState(0, 0)
        terminal_evaluations = {3: -5., 4: 7.}

        dag = GameDAG(matrix, start_state, terminal_evaluations)

        action, _ = alpha_beta(dag)
        assert action == 2, f"Expected action 2 (value 7), got {action}"



if __name__ == "__main__":
    unittest.main()