#!/usr/bin/env python3
"""
Car Diagnosis Bayesian Network
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bayesian_network import BayesianNetwork, CPT

def create_car_diagnosis_network():
    """
    Create the car diagnosis Bayesian network for automotive fault detection.
    
    Network structure covers the complete automotive electrical and mechanical systems:
    - Electrical: Main Fuse, Alternator, Battery systems
    - Ignition: Distributor, Spark Plugs, Spark system
    - Starting: Starter Motor, Battery Voltage, Cranking system  
    - Fuel/Air: Fuel System, Air Filter systems
    - Final outcome: Car Starts
    
    Returns:
        BayesianNetwork: Configured car diagnosis network
    """
    network = BayesianNetwork()
    
    # Define node outcomes
    outcomes = {
        "Main Fuse": ["Okay", "Blown"],
        "Battery Age": ["New", "Old", "Very Old"],
        "Alternator": ["Okay", "Faulty"],
        "Charging System": ["Okay", "Faulty"],
        "Battery Voltage": ["Strong", "Weak", "Dead"],
        "Voltage at Plug": ["Strong", "Weak", "None"],
        "Distributor": ["Okay", "Faulty"],
        "Spark Timing": ["Good", "Bad", "Very Bad"],
        "Spark Quality": ["Good", "Bad", "Very Bad"],
        "Spark Plugs": ["Okay", "Too Wide", "Fouled"],
        "Starter Motor": ["Okay", "Faulty"],
        "Starter System": ["Okay", "Faulty"],
        "Car Cranks": ["True", "False"],
        "Headlights": ["Bright", "Dim", "Off"],
        "Fuel System": ["Okay", "Faulty"],
        "Air Filter": ["Clean", "Dirty"],
        "Air System": ["Okay", "Faulty"],
        "Car Starts": ["True", "False"],
    }
    
    # Add all nodes with their domains
    for node, domain in outcomes.items():
        network.add_node(node, domain)
    
    # Define network structure (edges)
    edges = {
        "Main Fuse": ["Voltage at Plug", "Starter System"],
        "Voltage at Plug": ["Spark Quality"],
        "Distributor": ["Spark Timing", "Voltage at Plug"],
        "Spark Timing": ["Car Starts"],
        "Spark Quality": ["Car Starts"],
        "Spark Plugs": ["Spark Quality"],
        "Alternator": ["Charging System"],
        "Charging System": ["Battery Voltage"],
        "Battery Age": ["Battery Voltage"],
        "Battery Voltage": ["Starter System", "Voltage at Plug", "Headlights"],
        "Starter Motor": ["Starter System"],
        "Fuel System": ["Car Starts"],
        "Air Filter": ["Air System"],
        "Air System": ["Car Starts"],
        "Starter System": ["Car Cranks"],
        "Car Cranks": ["Car Starts"],
    }
    
    # Add all edges
    for parent, children in edges.items():
        for child in children:
            network.add_edge(parent, child)
    
    # Define conditional probability tables
    cpts = {
        # Root nodes (no parents)
        "Alternator": {
            "parents": [],
            "table": {
                "Okay": 0.997,
                "Faulty": 0.003
            }
        },
        
        "Battery Age": {
            "parents": [],
            "table": {
                "New": 0.4,
                "Old": 0.4,
                "Very Old": 0.2
            }
        },
        
        "Main Fuse": {
            "parents": [],
            "table": {
                "Okay": 0.99,
                "Blown": 0.01
            }
        },
        
        "Distributor": {
            "parents": [],
            "table": {
                "Okay": 0.99,
                "Faulty": 0.01
            }
        },
        
        "Starter Motor": {
            "parents": [],
            "table": {
                "Okay": 0.995,
                "Faulty": 0.005
            }
        },
        
        "Spark Plugs": {
            "parents": [],
            "table": {
                "Okay": 0.7,
                "Too Wide": 0.1,
                "Fouled": 0.2
            }
        },
        
        "Fuel System": {
            "parents": [],
            "table": {
                "Okay": 0.9,
                "Faulty": 0.1
            }
        },
        
        "Air Filter": {
            "parents": [],
            "table": {
                "Clean": 0.9,
                "Dirty": 0.1
            }
        },
        
        # Nodes with one parent
        "Charging System": {
            "parents": ["Alternator"],
            "table": {
                ("Okay",): {"Okay": 0.5, "Faulty": 0.5},
                ("Faulty",): {"Okay": 0.0, "Faulty": 1.0}
            }
        },
        
        "Headlights": {
            "parents": ["Battery Voltage"],
            "table": {
                ("Strong",): {"Bright": 0.94, "Dim": 0.01, "Off": 0.05},
                ("Weak",): {"Bright": 0.0, "Dim": 0.95, "Off": 0.05},
                ("Dead",): {"Bright": 0.0, "Dim": 0.0, "Off": 1.0}
            }
        },
        
        "Car Cranks": {
            "parents": ["Starter System"],
            "table": {
                ("Okay",): {"True": 0.8, "False": 0.2},
                ("Faulty",): {"True": 0.05, "False": 0.95}
            }
        },
        
        "Spark Timing": {
            "parents": ["Distributor"],
            "table": {
                ("Okay",): {"Good": 0.9, "Bad": 0.09, "Very Bad": 0.01},
                ("Faulty",): {"Good": 0.2, "Bad": 0.3, "Very Bad": 0.5}
            }
        },
        
        "Air System": {
            "parents": ["Air Filter"],
            "table": {
                ("Clean",): {"Okay": 0.9, "Faulty": 0.1},
                ("Dirty",): {"Okay": 0.3, "Faulty": 0.7}
            }
        },
        
        # Nodes with two parents
        "Battery Voltage": {
            "parents": ["Charging System", "Battery Age"],
            "table": {
                ("Okay", "New"): {"Strong": 0.95, "Weak": 0.04, "Dead": 0.01},
                ("Okay", "Old"): {"Strong": 0.8, "Weak": 0.15, "Dead": 0.05},
                ("Okay", "Very Old"): {"Strong": 0.6, "Weak": 0.3, "Dead": 0.1},
                ("Faulty", "New"): {"Strong": 0.008, "Weak": 0.3, "Dead": 0.692},
                ("Faulty", "Old"): {"Strong": 0.004, "Weak": 0.2, "Dead": 0.796},
                ("Faulty", "Very Old"): {"Strong": 0.002, "Weak": 0.1, "Dead": 0.898}
            }
        },
        
        "Spark Quality": {
            "parents": ["Spark Plugs", "Voltage at Plug"],
            "table": {
                ("Okay", "Strong"): {"Good": 1.0, "Bad": 0.0, "Very Bad": 0.0},
                ("Okay", "Weak"): {"Good": 0.0, "Bad": 1.0, "Very Bad": 0.0},
                ("Okay", "None"): {"Good": 0.0, "Bad": 0.0, "Very Bad": 1.0},
                ("Too Wide", "Strong"): {"Good": 0.0, "Bad": 1.0, "Very Bad": 0.0},
                ("Too Wide", "Weak"): {"Good": 0.0, "Bad": 0.0, "Very Bad": 1.0},
                ("Too Wide", "None"): {"Good": 0.0, "Bad": 0.0, "Very Bad": 1.0},
                ("Fouled", "Strong"): {"Good": 0.0, "Bad": 1.0, "Very Bad": 0.0},
                ("Fouled", "Weak"): {"Good": 0.0, "Bad": 0.0, "Very Bad": 1.0},
                ("Fouled", "None"): {"Good": 0.0, "Bad": 0.0, "Very Bad": 1.0}
            }
        },
        
        # Nodes with three parents
        "Voltage at Plug": {
            "parents": ["Main Fuse", "Distributor", "Battery Voltage"],
            "table": {
                ("Okay", "Okay", "Strong"): {"Strong": 0.9, "Weak": 0.05, "None": 0.05},
                ("Okay", "Okay", "Weak"): {"Strong": 0.0, "Weak": 0.9, "None": 0.1},
                ("Okay", "Okay", "Dead"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0},
                ("Okay", "Faulty", "Strong"): {"Strong": 0.1, "Weak": 0.1, "None": 0.8},
                ("Okay", "Faulty", "Weak"): {"Strong": 0.0, "Weak": 0.1, "None": 0.9},
                ("Okay", "Faulty", "Dead"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0},
                ("Blown", "Okay", "Strong"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0},
                ("Blown", "Okay", "Weak"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0},
                ("Blown", "Okay", "Dead"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0},
                ("Blown", "Faulty", "Strong"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0},
                ("Blown", "Faulty", "Weak"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0},
                ("Blown", "Faulty", "Dead"): {"Strong": 0.0, "Weak": 0.0, "None": 1.0}
            }
        },
        
        "Starter System": {
            "parents": ["Main Fuse", "Starter Motor", "Battery Voltage"],
            "table": {
                ("Okay", "Okay", "Strong"): {"Okay": 0.98, "Faulty": 0.02},
                ("Okay", "Okay", "Weak"): {"Okay": 0.9, "Faulty": 0.1},
                ("Okay", "Okay", "Dead"): {"Okay": 0.1, "Faulty": 0.9},
                ("Okay", "Faulty", "Strong"): {"Okay": 0.02, "Faulty": 0.98},
                ("Okay", "Faulty", "Weak"): {"Okay": 0.01, "Faulty": 0.99},
                ("Okay", "Faulty", "Dead"): {"Okay": 0.005, "Faulty": 0.995},
                ("Blown", "Okay", "Strong"): {"Okay": 0.0, "Faulty": 1.0},
                ("Blown", "Okay", "Weak"): {"Okay": 0.0, "Faulty": 1.0},
                ("Blown", "Okay", "Dead"): {"Okay": 0.0, "Faulty": 1.0},
                ("Blown", "Faulty", "Strong"): {"Okay": 0.0, "Faulty": 1.0},
                ("Blown", "Faulty", "Weak"): {"Okay": 0.0, "Faulty": 1.0},
                ("Blown", "Faulty", "Dead"): {"Okay": 0.0, "Faulty": 1.0}
            }
        },
        
        # Node with five parents - Car Starts
        "Car Starts": {
            "parents": ["Car Cranks", "Fuel System", "Spark Quality", "Air System", "Spark Timing"],
            "table": {
                # Car Cranks = True
                ("True", "Okay", "Good", "Okay", "Good"): {"True": 0.99, "False": 0.01},
                ("True", "Okay", "Good", "Okay", "Bad"): {"True": 0.98, "False": 0.02},
                ("True", "Okay", "Good", "Okay", "Very Bad"): {"True": 0.7, "False": 0.3},
                ("True", "Okay", "Good", "Faulty", "Good"): {"True": 0.8, "False": 0.2},
                ("True", "Okay", "Good", "Faulty", "Bad"): {"True": 0.75, "False": 0.25},
                ("True", "Okay", "Good", "Faulty", "Very Bad"): {"True": 0.6, "False": 0.4},
                ("True", "Okay", "Bad", "Okay", "Good"): {"True": 0.7, "False": 0.3},
                ("True", "Okay", "Bad", "Okay", "Bad"): {"True": 0.65, "False": 0.35},
                ("True", "Okay", "Bad", "Okay", "Very Bad"): {"True": 0.5, "False": 0.5},
                ("True", "Okay", "Bad", "Faulty", "Good"): {"True": 0.6, "False": 0.4},
                ("True", "Okay", "Bad", "Faulty", "Bad"): {"True": 0.5, "False": 0.5},
                ("True", "Okay", "Bad", "Faulty", "Very Bad"): {"True": 0.4, "False": 0.6},
                ("True", "Okay", "Very Bad", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("True", "Okay", "Very Bad", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Okay", "Very Bad", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Okay", "Very Bad", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("True", "Okay", "Very Bad", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Okay", "Very Bad", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Faulty", "Good", "Okay", "Good"): {"True": 0.1, "False": 0.9},
                ("True", "Faulty", "Good", "Okay", "Bad"): {"True": 0.05, "False": 0.95},
                ("True", "Faulty", "Good", "Okay", "Very Bad"): {"True": 0.02, "False": 0.98},
                ("True", "Faulty", "Good", "Faulty", "Good"): {"True": 0.05, "False": 0.95},
                ("True", "Faulty", "Good", "Faulty", "Bad"): {"True": 0.02, "False": 0.98},
                ("True", "Faulty", "Good", "Faulty", "Very Bad"): {"True": 0.01, "False": 0.99},
                ("True", "Faulty", "Bad", "Okay", "Good"): {"True": 0.05, "False": 0.95},
                ("True", "Faulty", "Bad", "Okay", "Bad"): {"True": 0.02, "False": 0.98},
                ("True", "Faulty", "Bad", "Okay", "Very Bad"): {"True": 0.01, "False": 0.99},
                ("True", "Faulty", "Bad", "Faulty", "Good"): {"True": 0.02, "False": 0.98},
                ("True", "Faulty", "Bad", "Faulty", "Bad"): {"True": 0.01, "False": 0.99},
                ("True", "Faulty", "Bad", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Faulty", "Very Bad", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("True", "Faulty", "Very Bad", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Faulty", "Very Bad", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Faulty", "Very Bad", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("True", "Faulty", "Very Bad", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("True", "Faulty", "Very Bad", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                
                # Car Cranks = False (all result in Car Starts = False)
                ("False", "Okay", "Good", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Good", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Good", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Good", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Good", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Good", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Bad", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Bad", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Bad", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Bad", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Bad", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Bad", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Very Bad", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Very Bad", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Very Bad", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Very Bad", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Very Bad", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Okay", "Very Bad", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Good", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Good", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Good", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Good", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Good", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Good", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Bad", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Bad", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Bad", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Bad", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Bad", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Bad", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Very Bad", "Okay", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Very Bad", "Okay", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Very Bad", "Okay", "Very Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Very Bad", "Faulty", "Good"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Very Bad", "Faulty", "Bad"): {"True": 0.0, "False": 1.0},
                ("False", "Faulty", "Very Bad", "Faulty", "Very Bad"): {"True": 0.0, "False": 1.0}
            }
        }
    }
    # Add all CPTs to the network
    for node, cpt_data in cpts.items():
        cpt = CPT(
            node=node,
            parents=cpt_data["parents"],
            table=cpt_data["table"]
        )
        network.cpts[node] = cpt
    
    return network


def create_car_diagnosis_dataset(network, num_samples=10000, outfile='car_data.csv'):
    """
    Method for creating example dataset of car diagnosis cases.
    Only works after all of bayesian_network.py has been implemented.

    Used to create output file, which can be loaded to test CPT creation.
    """
    samples = network.forward_sample(num_samples)
    with open(outfile, 'w') as f:
        import pandas as pd
        df = pd.DataFrame(samples)
        
        # Reorder columns to match logical flow (root nodes first, Car Starts last)
        column_order = [
            "Alternator", "Battery Age", "Main Fuse", "Distributor", "Starter Motor", 
            "Spark Plugs", "Fuel System", "Air Filter",
            "Charging System", "Battery Voltage", "Voltage at Plug", "Starter System",
            "Headlights", "Car Cranks", "Spark Timing", "Spark Quality", "Air System",
            "Car Starts"
        ]
        df = df[column_order]
        df.to_csv(f, index=False)


if __name__ == "__main__":
    network = create_car_diagnosis_network()
    network.print_network()
    create_car_diagnosis_dataset(network)

