import argparse
from typing import Dict, Any, Union, List
import numpy as np
import pandas as pd
import cvxpy as cvx
import matplotlib.pyplot as plt

def load_data(path: str) -> pd.DataFrame:
    """
    Load time series data from CSV file.
    
    Args:
        path: File path to the CSV file containing time series data
        
    Returns:
        DataFrame containing the loaded data
    """
    return pd.read_csv(path)

def build_and_solve_model(args: Dict[str, Any]) -> Dict[str, Union[float, None]]:
    """
    Build and solve the energy planning problem described in the handout.
    args is a dictionary of input constants, we extract the data into variables for you already.
    Returns a dictionary of results.

    Your should build a model, solve the model, and then populate the results dictionary with the results.
    """
    #was having runtime errors and issues with very large numbers, so scaled everything down by 1000
    f = 1000
    # Solar capacity factors (CFs) (how sunny it is every hour)
    solar_cf = np.array(args["solar_cf"])
    # Wind CFs (how windy it is every hour)
    wind_cf = np.array(args["wind_cf"])
    # How much money a solar panel that produces 1 kW of energy every hour at full CF costs
    solar_cost = np.array(args["solar_cost"])
    # How much money a windmill that produces 1 kW of energy every hour at full CF costs
    wind_cost = np.array(args["wind_cost"])
    # How much money a battery that stores 1 kWh of energy costs
    battery_cost = np.array(args["li_ion_cost"])
    # How much money a metal-air battery that stores 1 kWh of energy costs
    metal_air_cost = np.array(args["metal_air_cost"])
    # How efficient a battery is (How much energy you put in storage for 1 unit of energy generated)
    battery_efficiency = np.array(args["battery_efficiency"])
    # How efficient a battery is (How much energy you put in storage for 1 unit of energy generated)
    metal_air_efficiency = np.array(args["metal_air_efficiency"])
    # Total demand for every hour (kW)
    demand = np.array(args["demand"]) / f

    #Decision variables:

    solar_capacity = cvx.Variable(nonneg=True)
    wind_capacity = cvx.Variable(nonneg=True)
    battery_capacity = cvx.Variable(nonneg=True)
    metal_air_capacity = cvx.Variable(nonneg=True)

    # Energy produced by solar panels each hour
    battery_charge = cvx.Variable(len(demand))
    battery_discharge = cvx.Variable(len(demand))
    battery_state = cvx.Variable(len(demand))
    metal_air_charge = cvx.Variable(len(demand))
    metal_air_discharge = cvx.Variable(len(demand))
    metal_air_state = cvx.Variable(len(demand))

    constraints = []

    #start with 0
    constraints.append(battery_state[0] == 0)
    constraints.append(metal_air_state[0] == 0)

    for t, demand_t in enumerate(demand):
        #meet demand
        constraints.append(
            solar_capacity * solar_cf[t] +
            wind_capacity * wind_cf[t] +
            battery_discharge[t] +
            metal_air_discharge[t] 
            >=
            demand_t +
            battery_charge[t] +
            metal_air_charge[t]
        )
        #battery not over max
        constraints.append(battery_state[t] <= battery_capacity)
        constraints.append(metal_air_state[t] <= metal_air_capacity)

        if t > 0:
            #battery state update
            constraints.append(
                battery_state[t] == 
                battery_state[t-1] + 
                battery_efficiency * battery_charge[t] - 
                battery_discharge[t]
            )
            constraints.append(
                metal_air_state[t] == 
                metal_air_state[t-1] + 
                metal_air_efficiency * metal_air_charge[t] - 
                metal_air_discharge[t]
            )
        #non-negativity
        constraints.append(battery_charge[t] >= 0)
        constraints.append(battery_discharge[t] >= 0)
        constraints.append(metal_air_charge[t] >= 0)
        constraints.append(metal_air_discharge[t] >= 0)
        constraints.append(battery_state[t] >= 0)
        constraints.append(metal_air_state[t] >= 0)

        #objective
    total_cost = (
        (f * solar_cost) * solar_capacity +
        (f * wind_cost) * wind_capacity +
        (f * battery_cost) * battery_capacity +
        (f * metal_air_cost) * metal_air_capacity
    )
    objective = cvx.Minimize(total_cost)
    problem = cvx.Problem(objective, constraints)
    problem.solve(solver=cvx.SCS)

    results = {}
    # How much solar was built
    results["solar_capacity"] = round(float(solar_capacity.value * 1000)) if solar_capacity.value is not None else None
    # How much wind was built
    results["wind_capacity"] = round(float(wind_capacity.value * 1000)) if wind_capacity.value is not None else None
    # How much the total system cost (objective value of problem)
    results["total_cost"] = round(float(problem.value)) if problem.value is not None else None
    # how much total Li-ion battery capacity was built
    results["battery_capacity"] = round(float(battery_capacity.value * 1000)) if battery_capacity.value is not None else None
    # How much metal-air battery capacity was built
    results["metal_air_capacity"] = round(float(metal_air_capacity.value * 1000)) if metal_air_capacity.value is not None else None

    return results

def plan_for_RI(fraction_of_year: float) -> None:
    """
    Use data from RI to plan energy production and storage.
    Loads the desired data, processes it, and then calls build_and_solve_model.
    """

    SOLAR_COST = 0.014772123 * 1000
    WIND_COST = 0.015913707 * 1000
    BATTERY_COST = 0.007351353 * 1000
    METAL_AIR_COST = 0.000214378 * 1000
    wind_data = load_data("RI_wind.csv")
    solar_data = load_data("RI_solar.csv")
    demand_data = load_data("RI_demand.csv")
    
    # Use wind data length as reference for fraction calculation
    reference_length = len(wind_data)
    target_length = int(reference_length * fraction_of_year)
    
    wind_cf = wind_data[:target_length]
    solar_cf = solar_data[:target_length]
    demand = demand_data[:target_length]
    results = build_and_solve_model({
        "solar_cf": solar_cf["s_cfs"],
        "wind_cf": wind_cf["w_cfs"],
        "solar_cost": SOLAR_COST,
        "wind_cost": WIND_COST,
        "li_ion_cost": BATTERY_COST,
        "metal_air_cost": METAL_AIR_COST,
        "demand": demand["demand (kW)"],
        "battery_efficiency": 0.86,
        "metal_air_efficiency": 0.46
    })

    print(results)

def main(fraction_of_year: float) -> None:
    plan_for_RI(fraction_of_year)

if __name__ == "__main__":
    # Take as argument fraction of year to model
    args = argparse.ArgumentParser()
    args.add_argument("--fraction_of_year", type=float, default=1.0)
    args = args.parse_args()

    main(args.fraction_of_year)