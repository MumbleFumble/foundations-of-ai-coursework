"""
Utility functions for Bayesian Networks
"""

from typing import Dict, List, Any, TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from bayesian_network import BayesianNetwork, CPT


def print_network_structure(network: "BayesianNetwork") -> None:
    """
    Print the structure of a Bayesian Network in a readable format.
    
    Args:
        network: The BayesianNetwork to display
    """
    print("=" * 60)
    print("Bayesian Network Structure")
    print("=" * 60)
    
    print("Edges:")
    edges = []
    for parent in network.nodes:
        for child in network.get_children(parent):
            edges.append((parent, child))
    
    if edges:
        for parent, child in sorted(edges):
            print(f"  {parent} -> {child}")
    else:
        print("No edges?")
    print()


def print_cpt(cpt: "CPT", title: str | None = None) -> None:
    """
    Print a single CPT as a nicely formatted table.
    
    Args:
        cpt: The CPT to display
        title: Optional title for the table
    """
    if title:
        print(f"\n{title}")
    else:
        print(f"\nCPT for {cpt.node}")
    
    print("-" * 50)
    
    # Handle root nodes (no parents)
    if not cpt.parents:
        print(f"{'Value':<15} {'Probability':<15}")
        print("-" * 30)
        for value, prob in sorted(cpt.table.items()):
            print(f"{value:<15} {prob:<15.4f}")
        print()
        return
    
    # Handle nodes with parents
    # Get all possible outcomes for this node
    all_outcomes = set()
    for config_probs in cpt.table.values():
        if isinstance(config_probs, dict):
            all_outcomes.update(config_probs.keys())
    all_outcomes = sorted(list(all_outcomes))
    
    # Create header
    parent_header = " | ".join(f"{p:<10}" for p in cpt.parents)
    outcome_header = " | ".join(f"{o:<10}" for o in all_outcomes)
    full_header = f"{parent_header} || {outcome_header}"
    print(full_header)
    print("=" * len(full_header))
    
    # Print each configuration (sort by string representation to avoid type comparison issues)
    try:
        sorted_items = sorted(cpt.table.items())
    except TypeError:
        # If sorting fails due to mixed types, sort by string representation
        sorted_items = sorted(cpt.table.items(), key=lambda x: str(x[0]))
    
    for parent_config, outcome_probs in sorted_items:
        if isinstance(parent_config, tuple):
            parent_vals = " | ".join(f"{str(v):<10}" for v in parent_config)
        else:
            parent_vals = f"{str(parent_config):<10}"
        
        if isinstance(outcome_probs, dict):
            prob_vals = []
            for outcome in all_outcomes:
                prob = outcome_probs.get(outcome, 0.0)
                prob_vals.append(f"{prob:<10.4f}")
            prob_str = " | ".join(prob_vals)
        else:
            prob_str = f"{outcome_probs:<10.4f}"
        
        print(f"{parent_vals} || {prob_str}")
    print()


def print_all_cpts(network: "BayesianNetwork") -> None:
    """
    Print all CPTs in the network in topological order.
    
    Args:
        network: The BayesianNetwork whose CPTs to display
    """
    print("=" * 60)
    print("CONDITIONAL PROBABILITY TABLES")
    print("=" * 60)
    
    try:
        topo_order = network.get_topological_order()
    except:
        # Fallback if topological sort fails
        topo_order = sorted(network.nodes)
    
    for node in topo_order:
        if node in network.cpts:
            print_cpt(network.cpts[node])


def print_network_summary(network: "BayesianNetwork") -> None:
    """
    Print a complete summary of the Bayesian Network.
    
    Args:
        network: The BayesianNetwork to summarize
    """
    print_network_structure(network)
    print_all_cpts(network)
    
    # Print summary statistics
    print("=" * 60)
    print("NETWORK SUMMARY")
    print("=" * 60)
    print(f"Total nodes: {len(network.nodes)}")
    print(f"Total edges: {sum(len(children) for children in network.edges.values())}")
    print(f"Root nodes: {[node for node in network.nodes if not network.get_parents(node)]}")
    print(f"Leaf nodes: {[node for node in network.nodes if not network.get_children(node)]}")
    print()


def print_query_result(query_node: str, query_value: str, evidence: Dict[str, str], 
                      probability: float, num_samples: int = 0) -> None:
    """
    Print the result of a probability query in a readable format.
    
    Args:
        query_node: The queried node
        query_value: The queried value
        evidence: Evidence dictionary
        probability: The computed probability
        num_samples: Number of samples used (if applicable)
    """
    print("-" * 50)
    print("QUERY RESULT")
    print("-" * 50)
    
    # Format the query
    query_str = f"P({query_node} = {query_value}"
    if evidence:
        evidence_str = ", ".join(f"{k} = {v}" for k, v in evidence.items())
        query_str += f" | {evidence_str}"
    query_str += ")"
    
    print(f"Query: {query_str}")
    print(f"Result: {probability:.6f}")
    
    if num_samples:
        print(f"Samples used: {num_samples:,}")
    
    print("-" * 50)
    print()