[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zZXfiJny)
# README

## Tell us about your implementation!


## Answer the conceptual questions!#

### Part 1
    Q1. 
        Tournament Results:
        Games played: 100
        GreedyAgent + Simple Heuristic wins: 40 (40.0%)
        RandomAgent wins: 60 (60.0%)
        GreedyAgent + Simple Heuristic wins as BLACK: 16
        RandomAgent wins as BLACK: 26
        GreedyAgent + Simple Heuristic avg move time: 0.004s
        RandomAgent avg move time: 0.002s
        GreedyAgent + Simple Heuristic min time remaining: 26.9s
        RandomAgent min time remaining: 27.0s


        In the tournament Random won 60% of the games and ends up with a score of +20, while Greedy ends up at −20, and even as Black (the first mover), Random still comes out ahead. At first this looks odd, Greedy is “thinking” and Random is literally guessing. but the issue is that Greedy’s heuristic is way too naive. Since it only counts stones on the board, it keeps playing moves that look good immediately but are terrible for long-term territory or capture, which means Random accidentally does better just by not following the same predictable, short-sighted pattern. Timing isn’t the problem either: both agents stay under time limits so the difference really comes down to decision quality. In short, even a "smart" agent loses if its heuristic is dumb, which sets the stage for why we need deeper search and better evaluation going forward.

    Q2.
        It seems the greedyagent is alwasy trying to go wide and maximise count but odesn't really try to defend itself at all or have concept of gathering territory. just placing and capturing. which ends up spreading it thin and by the end of the game its lost many pieces and has little territory causing it to lose the majority of the games and it seems to be doing gneerally this n every game i played against it.

    Q3.
        
        If you change order in GreedyAgent, it no longer behaves deterministically, so games don’t always unfold the same way, and its win rate fluctuates (roughly 35 to 45% instead of a steady 40%). This happens because the simple heuristic frequently rates many moves as equally good, and randomizing the order changes which one gets picked, making the agent slightly less predictable and occasionally lucking into better patterns. the heuristic is still extremely weak (it only counts stones), there’s no lookahead, and it still has no understanding of territory, capture, or life and death. shuffling reduces exploitable repetition and adds variance, but it doesn’t solve the core issue: a bad evaluation plus greedy search will still make bad moves.

    Q4.

        By testing different search depths under Go’s 30-second time limit, I found that MinimaxAgent is only reliably safe at depth 2 (0.06s per move), while depth 3 becomes risky due to long early-game branching, and higher depths exceed the limit. AlphaBeta, however, can safely search one ply deeper, running comfortably at depth 3 (0.92s per move) but timing out at depth 4. This demonstrates the practical value of alpha-beta pruning: with the same time, it explores more of the search space and has a larger buffer against timeouts. Both agents are better than RandomAgent at their safe depths, showing how even a small amount of lookahead improves play. Overall, depth 2 for Minimax and depth 3 for Alpha-Beta provide the best balance between strategic strength and timing safety.

### Part 2

    Q1.    
        Tournament Results (8 Games):
        - MCTS wins: 8 (100.0%)
        - IDS wins: 0 (0.0%)
        
        In an 8-game tournament where each agent played as the first player (Black) in half the games, my MCTS agent achieved a perfect 100% win rate against the Iterative Deepening agent. The MCTS agent consistently outperformed the opponent regardless of turn order, maintaining safe time margins throughout. 

        
    Q2.     
      
        The figures reveal how MCTS builds confidence through simulation. The first graph shows that as MCTS runs more simulations, it progressively concentrates visits on promising actions early on, visits are spread kinda evenly as it explores, but by 1000 simulations, one or two actions dominate, showing MCTS has converged on what it believes is best. The second graph demonstrates the exploration-exploitation trade-off controlled by the C parameter: with low C (0.5), MCTS heavily exploits the current best action (top action gets over half of visits), while high C (5.0) forces broader exploration (top action only gets 20%, visits spread more evenly). The Gini coefficient quantifies this—lower values mean more uniform exploration, higher values mean focused exploitation. Together, these graphs show MCTS doesn't use a hand-crafted heuristic; instead, it builds an implicit evaluation function through statistics, where visit counts represent confidence and the UCT formula balances trying new moves versus doubling down on known good ones.

    Q3. MCTS Analysis
        I generated a heatmap visualizing the MCTS visit distribution for a specific board state (Black at center, White at top-left). The heatmap shows that the agent does not search uniformly; instead, it heavily concentrates its simulations on a few key tactical points adjacent to the existing stones, while largely ignoring empty corners that have little immediate strategic value. This demonstrates the effectiveness of the UCT formula in guiding the search towards relevant moves, allowing the agent to "think" deeply about critical conflicts rather than wasting resources on irrelevant areas of the board.

        Additionally, I generated a time-per-move graph (mcts_time_per_move) which tracks the agent's time spent per move over a full 30-second game. The graph illustrates the agent's dynamic time management strategy, where the time allocation for each turn is calculated based on the remaining time bank divided by the estimated number of moves left (derived from empty board spaces). This results in a curve where the agent spends more time on complex mid-game positions when the time bank is full, it has a massive spike in the mid game since thats where the decisions matter the most and are the hardest to decide.

## Hours taken:
    Part 1. 9
    part 2. 16

## Collaborators:

## Known Bugs:
    np.array has ssome red underline for an arguements error but ti causes no issue and i can't figure out how to stop it .
## AI Use Description:
    had to ask chat how certain matplotlib functions work, mostly just copied from other matplotlib functions from other homeowrks