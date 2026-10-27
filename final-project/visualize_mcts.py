import matplotlib.pyplot as plt
import numpy as np
import time
from agents import MCTSAgent, RandomAgent
from go_search_problem import GoProblem
import os

def visualize_mcts_heatmap():
    # 1. Setup Game
    problem = GoProblem(size=5)
    state = problem.get_start_state()
    
    # Play a few moves to get a non-empty board
    # Let's play a standard opening: Black center, White corner
    state = problem.transition(state, 12) # Center (2,2)
    state = problem.transition(state, 0)  # Top-left (0,0)
    
    # 2. Run MCTS
    agent = MCTSAgent()
    print("Running MCTS for 3 seconds...")
    
    # Run get_move. This will populate agent.last_root
    agent.get_move(state, time_limit=3.0)
    
    root = agent.last_root
    if root is None:
        print("Error: No root found.")
        return

    # 3. Extract Visits
    visits_grid = np.zeros((5, 5))
    
    total_visits = 0
    pass_visits = 0
    
    for child in root.children:
        action = child.action
        if action == 25: # Pass
            pass_visits = child.visits
            continue
            
        row = action // 5
        col = action % 5
        visits_grid[row, col] = child.visits
        total_visits += child.visits
        
    print(f"Total visits recorded on board: {total_visits}")
    print(f"Pass visits: {pass_visits}")

    # 4. Plot
    plt.figure(figsize=(8, 6))
    plt.imshow(visits_grid, cmap='viridis', interpolation='nearest')
    cbar = plt.colorbar()
    cbar.set_label('Number of Visits', rotation=270, labelpad=15)
    
    plt.title(f'MCTS Visit Distribution (Total Visits: {total_visits + pass_visits})\nState: Black(2,2), White(0,0) -> Black to Move')
    
    # Annotate
    for i in range(5):
        for j in range(5):
            val = visits_grid[i, j]
            if val > 0:
                color = "white" if val > visits_grid.max()/2 else "black"
                plt.text(j, i, int(val), ha="center", va="center", color=color)
    
    # Mark existing pieces
    # Black at 12 (2,2), White at 0 (0,0)
    # We use coordinates (x, y) -> (col, row) for text
    plt.text(2, 2, "B", ha="center", va="center", color="red", fontweight='bold', fontsize=16, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    plt.text(0, 0, "W", ha="center", va="center", color="red", fontweight='bold', fontsize=16, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    plt.xticks(range(5))
    plt.yticks(range(5))
    plt.xlabel('Column')
    plt.ylabel('Row')
    
    plt.tight_layout()
    output_path = 'mcts_visit_heatmap.png'
    plt.savefig(output_path)
    print(f"Saved heatmap to {output_path}")

def visualize_time_per_move():
    print("\nSimulating a game to measure time per move...")
    problem = GoProblem(size=5)
    state = problem.start_state
    
    # Agent setup
    agent = MCTSAgent()
    opponent = RandomAgent()
    
    # Time setup
    time_limit = 30.0 # Standard 30s game
    time_remaining = time_limit
    
    times = []
    moves = []
    
    move_num = 1
    max_moves = 50
    
    while not problem.is_terminal_state(state) and move_num <= max_moves:
        player = state.player_to_move()
        
        if player == 0: # Black (MCTS)
            start = time.time()
            # Pass remaining time to agent
            action = agent.get_move(state, time_remaining)
            end = time.time()
            duration = end - start
            
            times.append(duration)
            moves.append(move_num)
            
            time_remaining -= duration
            # Add increment if game runner does, but let's assume simple sudden death or small increment
            # GameRunner usually adds increment. Let's add 1s increment to be realistic
            time_remaining += 1.0 
            
            state = problem.transition(state, action)
        else: # White (Opponent)
            action = opponent.get_move(state, 1.0)
            state = problem.transition(state, action)
            
        move_num += 1
        
    print(f"Game finished in {move_num} moves.")
    print(f"Time remaining: {time_remaining:.2f}s")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(moves, times, marker='o', linestyle='-', color='b', label='MCTS Move Time')
    
    # Add average line
    if times:
        avg_time = np.mean(times)
        plt.axhline(y=avg_time, color='g', linestyle='--', label=f'Average ({avg_time:.2f}s)')
    
    plt.title('MCTS Time Spent per Move (30s Game + 1s Inc)')
    plt.xlabel('Move Number')
    plt.ylabel('Time Spent (seconds)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    output_path = 'mcts_time_per_move.png'
    plt.savefig(output_path)
    print(f"Saved time plot to {output_path}")

if __name__ == "__main__":
    visualize_mcts_heatmap()
    visualize_time_per_move()
