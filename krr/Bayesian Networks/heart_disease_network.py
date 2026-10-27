#!/usr/bin/env python3
"""
Heart Disease Bayesian Network
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bayesian_network import BayesianNetwork, CPT


def create_heart_disease_network():
    """
    Create the heart disease Bayesian network as specified in handout.md.
    
    Network structure:
    Smoking -> Blood Pressure -> Heart Disease Risk -> ECG Results
    Exercise -> Blood Pressure, Cholesterol -> Heart Disease Risk
    
    Returns:
        BayesianNetwork: Configured heart disease network
    """
    network = BayesianNetwork()
    
    # Add nodes with their possible values
    network.add_node("Smoking", ["Yes", "No"])
    network.add_node("Exercise", ["High", "Low"])
    network.add_node("BloodPressure", ["High", "Normal"])
    network.add_node("Cholesterol", ["High", "Normal"])
    network.add_node("HeartDiseaseRisk", ["High", "Low"])
    network.add_node("ECGResults", ["Abnormal", "Normal"])
    
    # Add edges to define the structure
    network.add_edge("Smoking", "BloodPressure")
    network.add_edge("Exercise", "BloodPressure")
    network.add_edge("Exercise", "Cholesterol")
    network.add_edge("Smoking", "HeartDiseaseRisk")
    network.add_edge("BloodPressure", "HeartDiseaseRisk")
    network.add_edge("Cholesterol", "HeartDiseaseRisk")
    network.add_edge("HeartDiseaseRisk", "ECGResults")
        
    smoking_cpt = CPT(
        node="Smoking",
        parents=[],
        table={"Yes": 0.20, "No": 0.80}
    )
    network.cpts["Smoking"] = smoking_cpt
    
    exercise_cpt = CPT(
        node="Exercise",
        parents=[],
        table={"High": 0.30, "Low": 0.70}
    )
    network.cpts["Exercise"] = exercise_cpt
    
    bp_cpt = CPT(
        node="BloodPressure",
        parents=["Smoking", "Exercise"],
        table={
            ("No", "High"): {"High": 0.15, "Normal": 0.85},
            ("No", "Low"): {"High": 0.30, "Normal": 0.70},
            ("Yes", "High"): {"High": 0.25, "Normal": 0.75},
            ("Yes", "Low"): {"High": 0.50, "Normal": 0.50}
        }
    )
    network.cpts["BloodPressure"] = bp_cpt
    
    cholesterol_cpt = CPT(
        node="Cholesterol",
        parents=["Exercise"],
        table={
            ("High",): {"High": 0.25, "Normal": 0.75},
            ("Low",): {"High": 0.45, "Normal": 0.55}
        }
    )
    network.cpts["Cholesterol"] = cholesterol_cpt
    
    hd_risk_cpt = CPT(
        node="HeartDiseaseRisk",
        parents=["Smoking", "BloodPressure", "Cholesterol"],
        table={
            ("No", "Normal", "Normal"): {"High": 0.05, "Low": 0.95},
            ("No", "High", "Normal"): {"High": 0.10, "Low": 0.90},
            ("No", "Normal", "High"): {"High": 0.08, "Low": 0.92},
            ("No", "High", "High"): {"High": 0.15, "Low": 0.85},
            ("Yes", "Normal", "Normal"): {"High": 0.12, "Low": 0.88},
            ("Yes", "High", "Normal"): {"High": 0.25, "Low": 0.75},
            ("Yes", "Normal", "High"): {"High": 0.20, "Low": 0.80},
            ("Yes", "High", "High"): {"High": 0.40, "Low": 0.60}
        }
    )
    network.cpts["HeartDiseaseRisk"] = hd_risk_cpt
    
    ecg_cpt = CPT(
        node="ECGResults",
        parents=["HeartDiseaseRisk"],
        table={
            ("High",): {"Abnormal": 0.60, "Normal": 0.40},
            ("Low",): {"Abnormal": 0.20, "Normal": 0.80}
        }
    )
    network.cpts["ECGResults"] = ecg_cpt
    
    return network

def create_heart_disease_dataset(network, num_samples=1000, outfile='heart_data.csv'):
    """
    Method for creating example dataset of heart disease cases.
    Only works after all of bayesian_network.py has been implemented.

    Used to create output file, which can be loaded to test CPT creation.
    """
    samples = network.forward_sample(num_samples)
    with open(outfile, 'w') as f:
        import pandas as pd
        df = pd.DataFrame(samples)
        df.to_csv(f, index=False)


if __name__ == "__main__":
    network = create_heart_disease_network()
    network.print_network()
    create_heart_disease_dataset(network)