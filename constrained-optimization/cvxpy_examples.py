from typing import Dict, List
import cvxpy as cvx
from matplotlib import pyplot as plt
import numpy as np

def optimal_diet_list_form() -> None:
    """
    Formulate the dieting problem using a list of constraints and variables instead of matrices and vectors
    This is easier to read and code if you are not familiar with matrix notation
    """
    #  Define foods and nutrients
    foods = ['apple', 'banana', 'carrot', 'chicken', 'rice', 'milk']
    nutrients = ['calories', 'protein', 'carbs', 'fat']
    # How much of each nutrient each food has
    food_nutrient_values = {
        'apple': {'calories': 95, 'protein': 0.3, 'carbs': 25, 'fat': 0.4},
        'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4},
        'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 9, 'fat': 0.2},
        'chicken': {'calories': 142, 'protein': 31, 'carbs': 0, 'fat': 3.6},
        'rice': {'calories': 130, 'protein': 2.6, 'carbs': 28, 'fat': 0.3},
        'milk': {'calories': 100, 'protein': 8, 'carbs': 12, 'fat': 3.2},
    }
    recommended_nutrient_values = {
        'calories': 2000,
        'protein': 50,
        'carbs': 300,
        'fat': 65,
    }
    # How much each food costs in $
    food_costs = {
        'apple': 0.5,
        'banana': 0.3,
        'carrot': 0.2,
        'chicken': 2.5,
        'rice': 0.8,
        'milk': 1.2,
    }

    # Construct list of variables x (x_i => how much of food i to purchase)
    x = []
    for f in foods:
        x.append(cvx.Variable())
    
    # Construct costs of each food (using same order of foods as for x)
    costs = []
    for f in foods:
        costs.append(food_costs[f])

    # Define a total cost, which will be our entire objective
    total_cost = 0
    for i, f in enumerate(foods):
        total_cost += costs[i] * x[i]

    # Objective is to minimize the cost of the food
    objective = cvx.Minimize(total_cost)

    # Define constraints
    constraints = []
    for n in nutrients:
        # For each nutrient, create a variable to be the total amount of nutrient n given x_i
        amount_of_nutrient = 0
        for i, f in enumerate(foods):
            amount_of_nutrient += food_nutrient_values[f][n] * x[i]
        constraints.append(amount_of_nutrient >= recommended_nutrient_values[n])
    
    # You can't eat negative food...
    for i in range(len(foods)):
        constraints.append(x[i] >= 0)

    # Create the problem object
    problem = cvx.Problem(objective, constraints)
    problem.solve()

    print("Diet problem (list form)")
    print("Status:", problem.status)
    print("Optimal value:", problem.value)
    for i, food in enumerate(foods):
        print(food, "=", x[i].value)

    

def optimal_diet_matrix_form() -> None:
    """
    Optimal dieting problem, using formulation involving x, c, A, b as vectors
    The advantage of using a matrix formulation, is that we already know the problem will take the form:

    min c^T x
    s.t. Ax <= b
    x >= 0

    The only challenge remaining is to determine what c, A, and b are.
    """

    # Define foods and nutrients
    foods = ['apple', 'banana', 'carrot', 'chicken', 'rice', 'milk']
    nutrients = ['calories', 'protein', 'carbs', 'fat']
    # How much of each nutrient each food has
    food_nutrient_values = {
        'apple': {'calories': 95, 'protein': 0.3, 'carbs': 25, 'fat': 0.4},
        'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4},
        'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 9, 'fat': 0.2},
        'chicken': {'calories': 142, 'protein': 31, 'carbs': 0, 'fat': 3.6},
        'rice': {'calories': 130, 'protein': 2.6, 'carbs': 28, 'fat': 0.3},
        'milk': {'calories': 100, 'protein': 8, 'carbs': 12, 'fat': 3.2},
    }
    recommended_nutrient_values = {
        'calories': 2000,
        'protein': 50,
        'carbs': 300,
        'fat': 65,
    }
    # How much each food costs in $
    food_costs = {
        'apple': 0.5,
        'banana': 0.3,
        'carrot': 0.2,
        'chicken': 2.5,
        'rice': 0.8,
        'milk': 1.2,
    }

    # Create the decision variables
    x = cvx.Variable(len(foods), nonneg=True)

    c = []
    for f in foods:
        c.append(food_costs[f])
    c = np.array(c)

    # Define the objective function
    objective = cvx.Minimize(c.T @ x)

    # Define the constraints
    A = []
    b = []

    for n in nutrients:
        A.append([])
        for f in foods:
            A[-1].append(food_nutrient_values[f][n])
        b.append(recommended_nutrient_values[n])
    
    A = np.array(A)
    b = np.array(b)

    constraints = [A @ x >= b, x >= 0]

    problem = cvx.Problem(objective, constraints)
    problem.solve()
    # Problem.foods can now be called to get the variables x
    problem.foods = x 

    print("Diet problem (matrix form)")
    print("Status:", problem.status)
    print("Optimal value:", problem.value)
    for i, food in enumerate(foods):
        print(food, "=", problem.foods[i].value)

def manufacturing_example() -> None:
    """
    How much of each good should we make to maximize profit?
    Given a set of goods, and a set of raw materials, a profit for each good,
    and a usage of each raw material for each good, how much of each good should we make to maximize profit?
    """
    # Define goods and materials
    # Note: this can be done in many forms, this tends to be the most human readable format,
    # even if more efficient data structures exist
    goods = ['shirt', 'pants', 'hat', 'shoes']
    raw_materials = ['cotton', 'leather', 'thread', 'rubber', 'plastic', 'metal']
    profit = {'shirt': 10, 'pants': 15, 'hat': 5, 'shoes': 20}
    raw_material_usage = {
        'shirt': {'cotton': 2, 'thread': 1, 'plastic': 1, 'leather': 0, 'metal': 0, 'rubber': 0},
        'pants': {'cotton': 2, 'thread': 3, 'plastic': 2, 'metal': 1, 'leather': 0, 'rubber': 0},
        'hat': {'leather': 1, 'thread': 1, 'plastic': 1, 'rubber': 0, 'metal': 0, 'cotton': 1},
        'shoes': {'leather': 2, 'thread': 2, 'rubber': 1, 'plastic': 1, 'metal': 0, 'cotton': 0},
    }
    raw_material_availability = {
        'cotton': 100,
        'leather': 50,
        'thread': 200,
        'rubber': 50,
        'plastic': 100,
        'metal': 20,
    }

    n_goods = len(goods)

    # cvx.Variable() constructs a single variable, cvx.Variable(n) constructs a n-length vector
    # Define X to be a vector of length n_goods
    x = cvx.Variable(n_goods, nonneg=True)
    
    # make cost vector
    profits = []
    for g in goods:
        profits.append(profit[g])
    
    # turn c into a numpy array (required if going to be used with dot product)
    c = np.array(profits)

    # Objective is almost always c^T times X. In python, matrix multiplication can be written as @
    objective = cvx.Maximize(c.T @ x)

    # Constraints
    # Construct a list of lists A, where A[i] is the list of much each good uses raw_material[i]
    A = []
    for r in raw_materials:
        # Add new row to A
        A.append([])
        for g in goods:
            A[-1].append(raw_material_usage[g][r])

    # construct b vector, b is the limit of each raw material availability
    b = []
    for r in raw_materials:
        b.append(raw_material_availability[r])
    
    # Again, convert to numpy array for matrix multiplication
    A = np.array(A)
    b = np.array(b)

    # Ax <= b
    # @ is matrix multiplication
    constraints = [A @ x <= b]

    # create the problem object and solve
    prob = cvx.Problem(objective, constraints)
    prob.solve()
    print("Manufacturing problem")
    print("Status:", prob.status)
    print("Optimal value:", prob.value)

    # Nice Printing of resulting amounts
    for i, good in enumerate(goods):
        print(good, "=", x.value[i])

def optimal_control() -> None:
    """
    Formulate a model and solve for the optimal control of a rocket.

    In this example, we wish to land a rocket on the moon while using the least amount of fuel.
    Our acceleration is capped at 5m/s^2.
    The rocket starts at 1000m above the moon's surface and has a velocity of 0.
    The moon's gravity is 1.625m/s^2.
    """

    # Define initial parameters
    initial_height = 1000
    gravity = -1.625
    max_acceleration = 5.00

    # We need to discretize time so that there are discrete timesteps we make decisions at
    # delta_t tells how how often we can make a decision to accelerate or not (0.1 seconds, in this case)
    delta_t = 0.1

    # when we wish to land
    goal_time = 120

    # How many timesteps it will take total
    n = int(goal_time / delta_t)

    # Define variables (things that change in our problem) as cvx.Variables
    accelerations = cvx.Variable(n)
    velocities = cvx.Variable(n)
    positions = cvx.Variable(n)

    # Define objective (minimize total acceleration)
    objective = cvx.Minimize(cvx.sum(accelerations))
    
    constraints = []

    # Assume the rocket starts at rest with 0 acceleration and velocity
    constraints.append(positions[0] == initial_height)
    constraints.append(velocities[0] == 0)
    constraints.append(accelerations[0] == 0)

    # For each timestep, we have the following constraints    
    for i in range(1, n):
        # Velocity = old_velocity + total acceleration (due to thrust and gravity) * delta time
        constraints.append(velocities[i] == velocities[i-1] + accelerations[i]*delta_t + gravity*delta_t)
        # Position = old_position + velocity * delta t
        constraints.append(positions[i] == positions[i-1] + velocities[i]*delta_t)
        # Position cannot be negative (no crashes)
        constraints.append(positions[i] >= 0)
        # Acceleration cannot be greater than max_acceleration, cannot be negative
        constraints.append(0 <= accelerations[i])
        constraints.append(accelerations[i] <= max_acceleration)
    
    # Land softly!
    constraints.append(velocities[n-1] == 0)
    constraints.append(positions[n-1] == 0)

    # Create the problem object
    problem = cvx.Problem(objective, constraints)
    problem.solve()

    print("Optimal control problem")
    print("Status:", problem.status)
    print("Optimal value:", problem.value)
    print("Optimal accelerations:", accelerations.value)
    plt.plot(positions.value, label="height")
    plt.xlabel("Timestep (in 1/10th of a second)")
    plt.ylabel("Height (in meters)")
    plt.show()

if __name__ == "__main__":
    optimal_diet_list_form()
    optimal_diet_matrix_form() 
    manufacturing_example()
    optimal_control()