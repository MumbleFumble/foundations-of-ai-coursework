"""
Bayesian Network

This module provides a basic framework for working with Bayesian Networks,
including structure representation, conditional probability table,
and Monte Carlo sampling for inference.
"""

from dataclasses import dataclass
from platform import node
from typing import Dict, List, Set, Optional, Any, Tuple
import pandas as pd
from collections import defaultdict
from utils import print_network_summary
import random

@dataclass
class CPT:
    """
    Conditional Probability Table dataclass.
    
    Stores the conditional probabilities for a node given its parents.
    For a node with no parents, this CPT represents the prior probability.
    
    Attributes:
        node: The name of the node this CPT represents
        parents: List of parent node names
        table: Dictionary mapping (parent_values, outcome) -> probability
               For nodes with no parents: {outcome: probability}
               For nodes with parents: {(parent1_val, parent2_val, ...): {outcome: prob}}
    """
    node: str
    parents: List[str]
    table: Dict[Any, Any]
    
    def get_probability(self, outcome: str, 
                       parent_values: Optional[Dict[str, str]] = None) -> float:
        """
        Get the conditional probability of an outcome given complete parent values.
        
        This method retrieves P(outcome | parent_values) from the CPT. For nodes
        without parents, this returns the prior probability P(outcome).

        Args:
            outcome: The outcome value for this node (e.g., "High", "Low")
            parent_values: Dictionary mapping parent names to their values
                          Required for nodes with parents, None for root nodes
                          Example: {"Smoking": "Yes", "Exercise": "High"}
            
        Returns:
            float: Conditional probability P(outcome | parent_values)
            
        Raises:
            ValueError: If parent_values is incomplete for nodes with parents
            
        Examples:
            # For a root node (no parents) (The Smoking node)
            cpt.get_probability("Yes")  # P(Smoking=Yes)
             
            # For a node with parents (The BloodPressure node)
            cpt.get_probability("High", {"Smoking": "Yes", "Exercise": "Low"})
        """
        
        
        
        probability_distribution = None 

        # Ensure all parent values are provided (if node has parents), no need to modify
        if parent_values and len(parent_values) != len(self.parents):
            missing_parents = set(self.parents) - set(parent_values.keys())
            extra_parents = set(parent_values.keys()) - set(self.parents)
            error_msg = f"Incomplete parent specification for node '{self.node}'."
            if missing_parents:
                error_msg += f" Missing parents: {missing_parents}."
            if extra_parents:
                error_msg += f" Extra parents provided: {extra_parents}."
            raise ValueError(error_msg)
        
        if not self.parents:
            print (f"Getting prior probability for root node '{self.node}'")
            print (f"Outcome: {outcome}, Probability: {self.table.get(outcome, 0.0)}")
            return self.table.get(outcome, 0.0)

        # Create parent configuration tuple in the correct order
        parent_configuration = tuple(parent_values[parent] for parent in self.parents)

        probability_distribution = self.table[parent_configuration]
    
        # Return the probability for the requested outcome
        return probability_distribution[outcome]
    

class BayesianNetwork:
    """
    Bayesian Network implementation.
    
    A Bayesian Network is a probabilistic graphical model that represents
    a set of variables and their conditional dependencies via a directed
    acyclic graph (DAG). Each node represents a random variable, and each
    edge represents a conditional dependency between variables.
    
    Attributes:
        nodes: Set of node names in the network
        edges: Dictionary mapping parent nodes to lists of children
        parents: Dictionary mapping child nodes to lists of parents
        cpts: Dictionary mapping node names to their CPTs
        node_domains: Dictionary mapping node names to their possible outcome values
    """
    
    def __init__(self):
        """Initialize an empty Bayesian Network."""
        self.nodes: Set[str] = set()
        self.edges: Dict[str, List[str]] = defaultdict(list)  # node -> list of children
        self.parents: Dict[str, List[str]] = defaultdict(list)  # node -> list of parents
        self.cpts: Dict[str, CPT] = {}  # node -> CPT
        self.node_domains: Dict[str, Set[str]] = defaultdict(set)  # node -> possible values
    
    def add_node(self, node: str, domain: List[str]) -> None:
        """
        Add a node to the network.
        
        Args:
            node: Name of the node
            domain: List of possible values for this node
        """
        self.nodes.add(node)
        self.node_domains[node] = set(domain)
    
    def add_edge(self, parent: str, child: str) -> None:
        """
        Add a directed edge from parent to child.
        
        Args:
            parent: Parent node name
            child: Child node name
        """
        if parent not in self.nodes or child not in self.nodes:
            raise ValueError("Both nodes must be added to the network before creating edges")
        
        if child not in self.edges[parent]:
            self.edges[parent].append(child)
        if parent not in self.parents[child]:
            self.parents[child].append(parent)
    
    def remove_edge(self, parent: str, child: str) -> None:
        """
        Remove a directed edge from parent to child.
        
        Args:
            parent: Parent node name
            child: Child node name
        """
        if child in self.edges[parent]:
            self.edges[parent].remove(child)
        if parent in self.parents[child]:
            self.parents[child].remove(parent)
    
    def get_parents(self, node: str) -> List[str]:
        """Get the list of parent nodes for a given node."""
        return self.parents[node].copy()
    
    def get_children(self, node: str) -> List[str]:
        """Get the list of child nodes for a given node."""
        return self.edges[node].copy()
    
    def build_cpt_from_data(self, node: str, data: pd.DataFrame) -> CPT:
        """
        Build a Conditional Probability Table for a node from training data.
        
        This method learns the conditional probabilities P(node | parents) by counting
        occurrences in the training data and normalizing to get probabilities.
        
        Algorithm:
        1. Extract relevant columns (node + its parents) from the data
        2. For nodes with no parents: Count frequencies and normalize by total
        3. For nodes with parents: Count occurrences for each parent configuration, normalize
        
        Args:
            node: Name of the node to build CPT for
            data: Training data as a pandas DataFrame with columns for all network nodes
            
        Returns:
            CPT: Conditional Probability Table with learned probabilities
            
        Raises:
            ValueError: If node is not in the network or required columns missing from data
        """
        # Validate input parameters
        if node not in self.nodes:
            raise ValueError(f"Node '{node}' is not in the network")
        
        if node not in data.columns:
            raise ValueError(f"Node '{node}' is not found in the data columns")
        
        parents = self.get_parents(node)
        # Case 1: Node has no parents - calculate prior probabilities P(node)
        if not parents:
            probs = data[node].value_counts(normalize=True).to_dict()
            return CPT(node=node, parents=[], table=probs)

        # Case 2: Node has parents - calculate conditional probabilities P(node | parents)
        cpt_table = {}
        grouped = data.groupby(parents, sort=False)

        for parent_vals, group in grouped:
            if not isinstance(parent_vals, tuple):
                parent_vals = (parent_vals,)

            parent_vals = tuple(
                group.name if isinstance(group.name, tuple) else group.name
            ) if hasattr(group, "name") else parent_vals

            probs = group[node].value_counts(normalize=True).to_dict()

            cpt_table[parent_vals] = probs

        return CPT(node=node, parents=parents, table=cpt_table)
             

    
    def build_all_cpts_from_data(self, data: pd.DataFrame) -> None:
        """
        Build CPTs for all nodes in the network from training data.
        
        Args:
            data: Training data as a pandas DataFrame containing columns
                  for all nodes in the network
                  
        Raises:
            ValueError: If required columns are missing from the data
        """
        # Build CPT for each node
        for node in self.nodes:
            cpt = self.build_cpt_from_data(node, data)
            self.cpts[node] = cpt
    
    def forward_sample(self, num_samples: int = 1000) -> List[Dict[str, str]]:
        """
        Generate samples from the Bayesian Network using prior sampling.
        
        Prior sampling generates samples by traversing nodes in topological order,
        sampling each node's value based on its conditional probability given its
        parents' already-sampled values.
        
        Algorithm:
        1. Get nodes in topological order (parents before children)
        2. For each sample:
           a. Initialize empty sample dictionary 
           b. For each node in topological order:
              - Get its CPT and parent values from current sample
              - Sample a value according to the conditional probabilities
              - Add the sampled value to the current sample
        
        Args:
            num_samples: Number of samples to generate
            
        Returns:
            List of complete samples, where each sample is a dictionary
            mapping node names to their sampled values
        """
        samples = []
        topo_order = self.get_topological_order()
        for _ in range(num_samples):
            sample = {}
            for node in topo_order:
                sample[node] = self._sample_node_value(node, sample)
            samples.append(sample)
        return samples
    
    def _sample_node_value(self, node: str, current_sample: Dict[str, str]) -> str:
        """
        Sample a value for a single node given the current partial sample.
        
        Args:
            node: Node to sample a value for
            current_sample: Dictionary containing values for nodes sampled so far
            
        Returns:
            Sampled value for the node

        """
        cpt = self.cpts[node]
        
        
        if cpt.parents:
            parent_values = {p: current_sample[p] for p in self.get_parents(node)}
            
            parent_config = tuple(parent_values[p] for p in cpt.parents)
            
            spread = cpt.table.get(parent_config)
        else:
            spread = cpt.table

        if not spread:
            #if no valid spread found, return a uniform distribution over possible values
            #RECOMMENDATION FROM TA DUE TO ERROR WHEN MAKING THE CAR DATASET
            #error couldn't be found, but this is a safeguard
            outcomes = list(self.node_domains[node])
            probs = [1/len(outcomes)] * len(outcomes)
            return random.choices(outcomes, probs)[0]

        outcomes = list(spread.keys())
        probs = list(spread.values())
        return random.choices(outcomes, probs)[0]
      


    def estimate_probability(self, query_node: str, query_value: str,
                           evidence: Optional[Dict[str, str]] = None,
                           num_samples: int = 10000) -> float:
        """
        Estimate probability using Monte Carlo rejection sampling.
        
        This method implements rejection sampling to estimate conditional probabilities.
        It generates samples from the network, rejects those that don't match the
        evidence, and calculates the proportion of remaining samples where the
        query node has the specified value.
        
        Algorithm:
        1. Generate samples using forward sampling
        2. Filter out samples that don't match the evidence (rejection step)
        3. Among remaining samples, count those where query_node = query_value
        4. Return: (matching samples) / (total valid samples)
        
        Args:
            query_node: Name of the node to query
            query_value: Specific value to query for
            evidence: Dictionary of observed evidence {node_name: observed_value}
                     None if no evidence (calculating prior probability)
            num_samples: Number of samples to generate for estimation
            
        Returns:
            Estimated probability as a float between 0 and 1
        """
        
        # Step 1: Generate samples from the network
        samples = self.forward_sample(num_samples)

        # Step 2: Filter samples that match the evidence (rejection sampling)
        if evidence is None: 
            valid_samples = [s for s in samples if True]
        else:
            valid_samples = [
            s for s in samples
            if all(s.get(var) == val for var, val in evidence.items())
            ]
        
        # Step 3: Handle case where no samples match the evidence (return zero probability)
        if len(valid_samples) == 0:
            return 0.0
        
        # Step 4: Count samples where query_node has the desired query_value
        valid_count = sum(1 for s in valid_samples if s[query_node] == query_value)  
        print(f"Total samples generated: {len(samples)}")
        print(f"Valid samples after evidence filtering: {len(valid_samples)}")
        # Step 5: Return estimated probability
        return valid_count / len(valid_samples)
    

    def get_topological_order(self) -> List[str]:
        """
        Get nodes in topological order (parents before children).
        
        Topological ordering ensures that for every directed edge (u, v),
        node u appears before node v in the ordering. This is essential
        for forward sampling where we must sample parent nodes before
        their children.
                
        Returns:
            List of node names in topological order
        """
        visited = set()
        order = []
        
        def dfs(node):
            """Recursive implementation of DFS"""
            if node in visited:
                return
            
            for child in self.edges[node]:
                dfs(child)
            visited.add(node)
            order.append(node)
        
        for node in self.nodes:
            if node not in visited:
                dfs(node)

        # Reverse for correct ordering (i.e., root nodes first)
        order.reverse()
        return order
    
    def print_network(self) -> None:
        """
        Print a complete summary of the Bayesian Network structure and CPTs.
        """
        print_network_summary(self)
    
    def create_network_from_data(self, data_file: str) -> 'BayesianNetwork':
        """
        Create a new network with the same structure but CPTs learned from data.
        
        Args:
            data_file: Path to CSV file containing training data
            
        Returns:
            New BayesianNetwork with data-learned CPTs
        """
        
        # Load data
        data = pd.read_csv(data_file)
        
        # Create new network with same structure
        data_network = BayesianNetwork()
        
        # Copy structure from current network
        for node in self.nodes:
            data_network.add_node(node, list(self.node_domains[node]))
        for parent in self.nodes:
            for child in self.get_children(parent):
                data_network.add_edge(parent, child)
        
        # Build CPTs from data
        data_network.build_all_cpts_from_data(data)
        
        return data_network


# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Bayesian Network Analysis Tool')
    parser.add_argument('--dataset', '-d', type=str, 
                       help='CSV dataset file to analyze (e.g., heart_data.csv, car_data.csv)')
    parser.add_argument('--network', '-n', type=str, choices=['heart', 'car'],
                       help='Which network to use (heart or car)')
    
    args = parser.parse_args()
    
    # Import networks based on choice
    if args.network == 'heart':
        from heart_disease_network import create_heart_disease_network
        network = create_heart_disease_network()
        print("Using Heart Disease Network")
        
        # If dataset provided, learn CPTs from data
        if args.dataset:
            print(f"Learning CPTs from dataset: {args.dataset}")
            network = network.create_network_from_data(args.dataset)
            print("CPTs learned from data!")
        
        network.print_network()
    elif args.network == 'car':
        try:
            from generate_car_dataset import create_car_diagnosis_network
            network = create_car_diagnosis_network()
            print("Using Car Diagnosis Network")
            
            # If dataset provided, learn CPTs from data
            if args.dataset:
                print(f"Learning CPTs from dataset: {args.dataset}")
                network = network.create_network_from_data(args.dataset)
                print("CPTs learned from data!")
            
            network.print_network()
        except ImportError:
            print("Could not import Car Diagnostics Dataset")
    else:
        print("Example usage of BayesianNetwork analysis methods:")
        print("python bayesian_network.py --network heart --dataset heart_data.csv")
        print("python bayesian_network.py --network car --dataset car_data.csv") 
        print("python bayesian_network.py --network heart")