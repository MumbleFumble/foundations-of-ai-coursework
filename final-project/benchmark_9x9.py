import matplotlib.pyplot as plt
import numpy as np
from game_runner import GameRunner, TournamentStats
from agents import MCTSAgentV2, MCTSAgentV1, MCTSAgentV0, RandomAgent, GreedyAgent, IterativeDeepeningAgent, MinimaxAgent, AlphaBetaAgent

def run_benchmark():
    # Configuration
    BOARD_SIZE = 9
    TIME_LIMIT = 15.0 # 15 seconds per player
    GAMES_PER_OPPONENT = 4 # Keep it low for speed (2 Black, 2 White)
    
    # Define Final Agent (V2 - Threaded + Rollout)
    final_agent_factory = lambda: MCTSAgentV2()
    
    # Define Opponents to benchmark against
    opponents = {
        "Random": lambda: RandomAgent(),
        "Greedy": lambda: GreedyAgent(),
        "IDS": lambda: IterativeDeepeningAgent(),
        "AlphaBeta (D2)": lambda: AlphaBetaAgent(depth_cutoff=2),
        "MCTS V0 (Single)": lambda: MCTSAgentV0(),
        "MCTS V1 (Threaded)": lambda: MCTSAgentV1()
    }
    
    results = {}
    
    print(f"Starting Benchmark for Final Agent (V2 Threaded+Rollout) on {BOARD_SIZE}x{BOARD_SIZE} Board")
    print(f"Time Limit: {TIME_LIMIT}s, Games per Opponent: {GAMES_PER_OPPONENT}")
    print("-" * 60)
    
    runner = GameRunner(board_size=BOARD_SIZE, time_limit=TIME_LIMIT, time_increment=1.0)
    
    for name, opp_factory in opponents.items():
        print(f"Playing against {name}...")
        
        # Create fresh agents for each tournament
        hero = final_agent_factory()
        villain = opp_factory()
        
        # Run tournament
        # Note: play_tournament handles alternating colors automatically
        stats = runner.play_tournament(hero, villain, num_games=GAMES_PER_OPPONENT, verbose=True)
        
        # Calculate Win Rate
        win_rate = (stats.player1_wins / stats.games_played) * 100
        results[name] = win_rate
        print(f"Result vs {name}: {win_rate:.1f}% Win Rate")
        print("-" * 30)

    # Plotting
    print("Generating Graph...")
    opp_names = list(results.keys())
    win_rates = list(results.values())
    
    plt.figure(figsize=(12, 6))
    
    # Create bars
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    bars = plt.bar(opp_names, win_rates, color=colors[:len(opp_names)])
    
    plt.ylim(0, 105) # Go slightly above 100 for label space
    plt.ylabel('Win Rate (%)')
    plt.title(f'MCTS V2 (Threaded+Rollout) Performance (9x9 Board)\nvs Various Opponents ({GAMES_PER_OPPONENT} games each)')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%',
                ha='center', va='bottom', fontweight='bold')
                
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_file = 'final_agent_performance_9x9.png'
    plt.savefig(output_file)
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    run_benchmark()
