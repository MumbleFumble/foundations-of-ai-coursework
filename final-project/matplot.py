import numpy as np
import matplotlib.pyplot as plt
from agents import MCTSAgent, RandomAgent
from go_search_problem import GoProblem
import time
import random

def analyze_mcts_thinking_evolution():
    """
    Track how MCTS's preferences change as it runs more simulations.
    Shows the top 5 actions' visit counts at different points in the search.
    """
    agent = MCTSAgent(c=np.sqrt(2))
    problem = GoProblem(size=5)
    start_state = problem.get_start_state()
    
    from agents import MCTSNode
    root = MCTSNode(start_state)
    
    snapshots = []
    snapshot_sims = [100, 300, 600, 1000]
    simulation_count = 0
    
    while simulation_count < snapshot_sims[-1]:
        leaf = agent._select(root)
        
        if not problem.is_terminal_state(leaf.state):
            agent._expand(leaf)
            
            for child in leaf.children:
                result = agent._simulate(child.state)
                agent._backpropagate(child, result)
                simulation_count += 1
                
                if simulation_count in snapshot_sims and len(snapshots) < len(snapshot_sims):
                    visits = [child.visits for child in root.children]
                    sorted_indices = np.argsort(visits)[::-1][:5]
                    snapshot_data = [(i, visits[i]) for i in sorted_indices]
                    snapshots.append((simulation_count, snapshot_data))
        else:
            result = problem.get_result(leaf.state)
            agent._backpropagate(leaf, result)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('How MCTS Thinking Evolves with More Simulations', fontsize=14)
    
    for idx, (sims, data) in enumerate(snapshots):
        ax = axes[idx // 2, idx % 2]
        
        actions = [f'A{d[0]}' for d in data]
        visits = [d[1] for d in data]
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        ax.barh(actions, visits, color=colors[:len(actions)])
        
        ax.set_xlabel('Visits')
        ax.set_ylabel('Action')
        ax.set_title(f'After {sims} simulations')
        ax.invert_yaxis()
        
        for i, v in enumerate(visits):
            pct = (v / sum(visits)) * 100
            ax.text(v, i, f' {pct:.0f}%', va='center')
    
    plt.tight_layout()
    plt.savefig('mcts_game_analysis.png', dpi=200, bbox_inches='tight')
    plt.close()


def analyze_exploration_vs_exploitation():
    """
    Compare how different C values distribute visits across actions.
    Uses a completely different starting position for variety.
    """
    c_values = [0.5, 1.4, 2.5, 5.0]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Exploration vs Exploitation: Different C Values', fontsize=14)
    
    problem = GoProblem(size=5)
    start_state = problem.get_start_state()
    
    for idx, c_val in enumerate(c_values):
        ax = axes[idx // 2, idx % 2]
        
        agent = MCTSAgent(c=c_val)
        
        from agents import MCTSNode
        root = MCTSNode(start_state)
        
        for _ in range(800):
            leaf = agent.select(root)
            
            if not problem.is_terminal_state(leaf.state):
                agent.expand(leaf)
                
                for child in leaf.children:
                    result = agent.simulate(child.state)
                    agent.backpropagate(child, result)
            else:
                result = problem.get_result(leaf.state)
                agent.backpropagate(leaf, result)
        
        if root.children:
            visits = [child.visits for child in root.children]
            total = sum(visits)
            sorted_visits = sorted(visits, reverse=True)
            
            percentages = [(v / total) * 100 for v in sorted_visits[:10]]
            
            x_pos = np.arange(len(percentages))
            ax.bar(x_pos, percentages, color='darkgreen', alpha=0.7)
            
            ax.set_xlabel('Action Rank')
            ax.set_ylabel('% of Total Visits')
            ax.set_title(f'C = {c_val}')
            ax.set_ylim(0, max(percentages) * 1.2)
            
            gini = sum(abs(i - j) for i in sorted_visits for j in sorted_visits) / (2 * len(visits) * sum(visits))
            ax.text(0.95, 0.95, f'Concentration: {gini:.2f}', 
                   transform=ax.transAxes, ha='right', va='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('mcts_convergence_analysis.png', dpi=200, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    analyze_mcts_thinking_evolution()
    analyze_exploration_vs_exploitation()


