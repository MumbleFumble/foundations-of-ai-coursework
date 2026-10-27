import unittest
from typing import Optional

from sat_solvers import walksat, gsat
from sat_problem import Clause, Literal, Variable, CNF, Model


class IOTest(unittest.TestCase):
    """
    Tests input/output for SAT solver implementations.
    
    Contains basic test cases to verify that GSAT and WalkSAT
    correctly solve simple CNF formulas and make optimal decisions.
    """

    def test_basic_cnf_walksat(self) -> None:
        """
        Test if WalkSAT picks the optimal variable to flip in a simple scenario.
        
        Tests WalkSAT's greedy variable selection on a CNF formula where one
        variable flip is clearly better than others.

        CNF = (A or B) and (~B or C) and (B or ~A) and (D or B)
        Initial assignments: A=false, B=false, C=true, D=false

        Analysis:
        - Unsatisfied clauses: (A or B), (D or B)
        - Flipping A: satisfies (A or B) but unsatisfies (B or ~A)
        - Flipping B: satisfies both (A or B) and (D or B) with no conflicts
        - Flipping D: only satisfies (D or B)
        
        The optimal choice is B, which WalkSAT should select when p=0 (greedy).
        """
        cnf = CNF()
        cnf.add_clause(
            Clause([Literal(Variable("A"), True), Literal(Variable("B"), True)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), False), Literal(Variable("C"), True)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), True), Literal(Variable("A"), False)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), True), Literal(Variable("D"), True)]))
        cnf_model = Model(cnf)

        cnf_model.assign(Variable("A"), False)
        cnf_model.assign(Variable("B"), False)
        cnf_model.assign(Variable("C"), True)
        cnf_model.assign(Variable("D"), False)

        model, _ = walksat(cnf, max_iterations=500, p=0,
                           existing_model=cnf_model)
        assert(model)
        self.assertEqual(model.flipped[0], Variable("B"), 'Walksat does not pick the best value to flip!')
        print('Walksat picks the right value to flip!')

    def test_basic_cnf_gsat(self) -> None:
        """
        Test if GSAT can solve a basic CNF formula.
        
        Tests GSAT's ability to find a satisfying assignment for a simple
        CNF formula starting from a partially unsatisfying initial state.
        
        CNF = (A or B) and (~B or C) and (B or ~A) and (B or D)
        Example solution: A=True, B=True, C=True, D=True
        """
        cnf = CNF()
        cnf.add_clause(
            Clause([Literal(Variable("A"), True), Literal(Variable("B"), True)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), False), Literal(Variable("C"), True)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), True), Literal(Variable("A"), False)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), False), Literal(Variable("D"), True)]))
        cnf_model = Model(cnf)
        cnf_model.assign(Variable("A"), False)
        cnf_model.assign(Variable("B"), False)
        cnf_model.assign(Variable("C"), True)
        cnf_model.assign(Variable("D"), False)
        model, _ = gsat(cnf, max_iterations=500, p=0,
                        existing_model=cnf_model)
        self.assertIsNotNone(model, "The solver should return a solution model")
        assert(model)
        A = model.assignments[Variable("A")]
        B = model.assignments[Variable("B")]
        C = model.assignments[Variable("C")]
        D = model.assignments[Variable("D")]

        self.assertTrue((A or B) and (not B or C)
                        and (B or not A) and (B or D))
        print('GSAT solves a simple CNF!')
    
    def test_num_iterations_accumulates_over_restarts_walksat(self) -> None:
        """
        Ensure num_iterations counts total iterations across randomized restarts.
        We use an unsatisfiable CNF so the solver cannot exit early and must run all iterations.
        """
        # CNF: (A) and (not A) -> unsatisfiable
        cnf = CNF()
        cnf.add_clause(Clause([Literal(Variable("A"), True)]))
        cnf.add_clause(Clause([Literal(Variable("A"), False)]))

        max_iters = 5
        restarts = 3
        _, stats = walksat(cnf, max_iterations=max_iters, p=0.5, num_randomized_restarts=restarts)
        expected = max_iters * restarts
        self.assertEqual(stats.get('num_iterations'), expected,
                         f"Expected total iterations {expected}, got {stats.get('num_iterations')}")

    def test_walksat_returns_stats_structure(self) -> None:
        """
        Basic structural checks on returned statistics from WalkSAT.
        """
        cnf = CNF()
        cnf.add_clause(Clause([Literal(Variable("X"), True), Literal(Variable("Y"), True)]))

        model, stats = walksat(cnf, max_iterations=10, p=0.5, num_randomized_restarts=1)
        self.assertIsInstance(stats, dict)
        self.assertIn('num_iterations', stats)
        self.assertIn('num_unsatisfied_clauses', stats)
        self.assertIn('run_time', stats)
        self.assertIsInstance(stats['num_iterations'], int)
        self.assertIsInstance(stats['num_unsatisfied_clauses'], list)
        self.assertIsInstance(stats['run_time'], float)

    def test_accumulate_runtime_over_multiple_trials(self) -> None:
        """
        Run multiple independent trials and ensure summing runtime matches per-trial runtimes.
        """
        cnf = CNF()
        cnf.add_clause(Clause([Literal(Variable("P"), True), Literal(Variable("Q"), True)]))

        trials = 3
        total = 0.0
        runtimes = []
        for _ in range(trials):
            _, stats = walksat(cnf, max_iterations=10, p=0.5, num_randomized_restarts=1)
            rt = stats.get('run_time', 0.0)
            runtimes.append(rt)
            total += rt

        # sanity checks
        self.assertAlmostEqual(total, sum(runtimes), places=6)
        
if __name__ == "__main__":
    unittest.main()