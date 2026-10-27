[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AkI1sl3k)
# assignment-2-informed-search


### Task 1
On the smaller 2×2 puzzles, all three algorithms finished almost instantly, with BFS expanding about 8 states on average, DFS about 16, and IDS about 13. When I moved up to 3×3 puzzles , the difference was dramatic: BFS expanded around 13,700 states, DFS over 91,000, and IDS about 53,000. Each trial on the 3×3 size took roughly 22–26 seconds to finish, compared to zero runtime on the 2×2. I saw that BFS consistently found the shortest paths and was the most efficient in runtime, while DFS explored  more states and IDS repeated searches, making it slower than BFS without being better. Increasing the number of trials mainly smoothed out averages but didn’t change the relative performance of the algorithms. I have quite a fast computer and it was taking over 5 mins to run a single trial for a 4x4 grid, the time scaling based off gride size is very rapid.


### Task 4a
My heuristic counts how many tiles are in the wrong row or column compared to their correct positions. Each misplaced row or column adds 1 to the heuristic,since correcting a misplaced row or column requires at least one swap. Athough one swap can move two umbers to their correct place, making this heurisitic also inadmissable (pessamistic).


### Task 4b
I am having many issues with my computer generating a graph, this is a consisent issue over mulutple labs and different classes. visualising a graph on my computer doesn't seem to work. However, just from comparing the theory Manhattan distance heuristics, my heuristic expands fewer states and runs faster but sometimes sacrifices optimality. Manhattan distance tends to guarantee optimal solutions, while my heuristic speeds up search at the cost of occasional suboptimal paths.

### Tests


Collaborators:

Hours spent on homework:

Known bugs:

AI Use Description:
used it to fix a few import issues due to me not having python 3.10.6 or tqdm. 

You must acknowledge use here and submit transcript if AI was used for portions of the assignment