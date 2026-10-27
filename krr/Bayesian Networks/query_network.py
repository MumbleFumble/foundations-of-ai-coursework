#!/usr/bin/env python3
"""
Task 3.2: Car Diagnostics Questions

Use your estimate_probability method to answer the questions about the car diagnostics network.
Complete the TODOs below and run this script to see your results.
"""

from generate_car_dataset import create_car_diagnosis_network

def main():
    # Create the car diagnostics network
    network = create_car_diagnosis_network()
    
    network = network.create_network_from_data('car_data.csv')
    #Question 1
    print("Q1.")
    print(network.estimate_probability(
        query_node="Car Starts",
        query_value=True,
        evidence=None,
        num_samples=100000
    ))


    #Question 2
    print("Q2.")
    print(network.estimate_probability(
        query_node="Battery Voltage",
        query_value="Strong",
        evidence={"Battery Age": "New", "Charging System": "Okay"},
        num_samples=100000

    ))
   

    #Question 3
    print("Q3.")
    evidence = {"Car Starts": False, "Headlights": "Dim", "Car Cranks": True}

    p_fuel = network.estimate_probability("Fuel System", "Faulty", evidence, 100000)
    p_spark = 1 - network.estimate_probability("Spark Plugs", "Okay", evidence, 100000)
    p_alt = network.estimate_probability("Alternator", "Faulty", evidence, 100000)
    print(f"  P(Fuel System=Faulty | evidence) = {p_fuel}")
    print(f"  P(Spark Plugs=Faulty | evidence) = {p_spark}")
    print(f"  P(Alternator=Faulty | evidence) = {p_alt}")
    # Decide which component is broken
    probs = {"FuelSystem": p_fuel, "SparkPlugs": p_spark, "Alternator": p_alt}
    likely_issue = max(probs, key=probs.get)
    print(f"Most likely cause of the problem: {likely_issue}")
    

if __name__ == "__main__":
    main()