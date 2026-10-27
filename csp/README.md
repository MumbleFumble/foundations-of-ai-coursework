[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wAHdSca6)
# ReadME

Tell us about your implementation!

    For an n × n Sudoku where each cell can contain one of m digits, the CNF encoding uses one Boolean variable x_(r,c,d) [or x_(i,j,v) from the homeowkr webpage] for each cell (r,c) and each digit d.
    As such the total variables is: n^2 * m
    With m = 9 this becomes 9 * n^2. For the standard 9×9 Sudoku (n = 9) this is 9^3 or 729 Boolean variables.

Tell us about your tests!

tests/test_solvers_basic.py
    Tests that walksat and gsat return stats dictionaries with expected keys.
    Verifies walksat reproducibility when the RNG is seeded.
tests/test_multiple_trials.py
    Runs multiple small trials of WalkSAT and checks the accumulated runtime is recorded.


Answer the conceptual questions!

    Q1.
    GSAT neighborhood is the the entire CNF formula, at each step GSAT either picks a random variable (with probability p) or greedily flips the variable (neighbourhood of all variables) that most reduces the number of unsatisfied clauses.
    Where as the WalkSAT neighborhood is a random unsatisfied clause, then look at only the variables that are in that clause. WalkSAT either chooses a random variable from that clause (with probability p) or greedily flips the variable in the clause that best reduces unsatisfied clauses.
  
   With p = 1.0 WalkSAT performs purely random flips, but only among variables that appear in a currently unsatisfied clause. This restriction moves it toward variables that are problematic, even purely random flips will fix existing violations or move conflicts around in a useful way. GSAT with p = 1.0 flips uniformly at random over all variables and therefore has no direction, making it far less likely to resolve current unsatisfied clauses.

    
    

    Q2.
    In my results:
        GSAT: the fastest p with a 100% success rate in my table is p = 0.50 (Run Time 0.56s, Iterations 359). Several p failed (success rate 0). Small run time values for p with 0% success are not meaningful because they show failures or timeouts.
        WalkSAT: the fastest p in my table is also p = 0.50 (Run Time 0.01s, Iterations 80) with 100% success.
    Provided results:
        GSAT: best observed p = 0.50 (avg time 0.25s, avg iters 2618, success 1.00).
        WalkSAT: best observed p in the reference set is near 0.50 (very small times at p=0.50–0.70; p=0.20–0.60 also show strong performance).

    Both runs show p ≈ 0.5 is best choice.  There are however, differences in absolute runtimes/iterations are expected (implementation details, random seed, hardware, restart counts).
    WalkSAT succeeds across a wide range of p (including p=1 in some reference runs) because its random flips are drawn from variables in an unsatisfied clause whereas GSAT has poor success at p=1.
    This shows we should use p around 0.4–0.6 (0.5 is a good default). If you profile on other instance sets, repeat a small sweep to pick p for that problem family.

    Q3.
    Experimental design to estimate 100-Queens runtime with WalkSAT:
    from Q2. the p to pick seems to be p = 0.5.
    
    Measure runtime and iterations for size 20 with p = 0.5, using 20 trials per size. Record mean runtime and mean iterations.
    Find a scaling model (googled) iterations =  c * N^result to the measured mean iterations.
    Convert predicted iterations at N=100 to runtime using measured time-per-iteration (mean_runtime / mean_iterations) from mid-size runs.

    my experinemnt was taking so long that i added an extra file to just run the test i wanted.
     
     Total run time over 20 trial(s): 1.5183846950531006 seconds

    (all "=" are meaning estimated value but i cant do the squiggly line equal sign on my keyboard)~~

    would repeat with more sizes but for time sake only with 1 and 20
    t100 = t20 * (100/20)^2 = 1.52 * 25 = 31.25seconds.
    

Hours taken: 8

Collaborators:
    used google to look up code that can pick a random variable from given choices (for the random assignments of 1 or 0s)

Known Bugs: