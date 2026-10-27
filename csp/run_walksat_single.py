import argparse
import random
from n_queens import NQueens
from sat_solvers import walksat

def main():
    parser = argparse.ArgumentParser(description="Run WalkSAT on N-Queens with a fixed p")
    parser.add_argument("-n", type=int, default=8, help="N for N-Queens")
    parser.add_argument("--p", type=float, default=0.5, help="probability p for WalkSAT")
    parser.add_argument("--num_trials", type=int, default=1, help="number of trials")
    parser.add_argument("--max_iterations", type=int, default=10000, help="max iterations per restart")
    parser.add_argument("--randomized_restarts", type=int, default=1, help="number of randomized restarts")
    args = parser.parse_args()

    total_run_time = 0.0
    for t in range(args.num_trials):
        problem = NQueens(args.n)
        model, stats = walksat(problem,
                               p=args.p,
                               max_iterations=args.max_iterations,
                               num_randomized_restarts=args.randomized_restarts)
        found = model is not None
        run_time = stats.get('run_time', 0.0)
        total_run_time += run_time
        print(f"Trial {t+1}: found={found}, run_time={run_time}, num_iterations={stats.get('num_iterations')}, final_unsat={stats.get('num_unsatisfied_clauses')[-1] if stats.get('num_unsatisfied_clauses') else None}")

    print(f"Total run time over {args.num_trials} trial(s): {total_run_time} seconds")

if __name__ == "__main__":
    random.seed(42)
    main()