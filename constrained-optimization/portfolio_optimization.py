import argparse
from typing import Dict, List, Tuple
import numpy as np
import cvxpy as cvx    
from load_stock_data import get_data

def calculate_stats(data: Dict[str, List[float]], stock_names: List[str]) -> Tuple[Dict[str, float], np.ndarray]:
    """
    Calculate expected ROI (Return On Investment) and variance for each stock in the provided data.
    The data provided gives daily stock prices at the end of market day normalized to initial price of stock.
    This means that each stock's starting price at the start of the previous year is 1.
    If a stock doubled in price (from 200 to 400), in normalized prices the stock will begin at 1 and end at 2.

    The total return of a stock is the final price for a stock divided by the starting point (which is 1...)
    Your function should return the stock return after one year and covariance of the daily prices for each stock.

    You may find the numpy methods np.cov (covariance) to be useful.

    :param data: dictionary of stock data. The key is the stock ticker, the value is a list of daily prices
    :return: dictionary of stock data with expected return, the covariance matrix
    """

    expected_returns: Dict[str, float] = {}
    for stock in stock_names:
        prices = data[stock]
        returns = np.array(prices, dtype=float)
        expected_returns[stock] = returns[-1]
    price_matrix = np.array([np.array(data[s], dtype=float) for s in stock_names])
    covariance_matrix = np.cov(price_matrix, rowvar=True)
    return expected_returns, covariance_matrix

    

def build_model(stock_returns: Dict[str, float], covariance_matrix: np.ndarray, maximum_risk: float, stock_order: List[str]) -> cvx.Problem:
    """
    Construct a CVXPY model to solve the portfolio optimization problem.
    For a given set of stocks with provided returns and covariances and a maximum risk,
    find the optimal portfolio weights that maximize return.

    :param stock_returns: dictionary of stock data. The key is the stock ticker, the value is the historical return of the stocks
    :param covariance_matrix: covariance matrix of the stock returns
    :param maximum_risk: maximum risk tolerance
    :param stock_order: list of stock tickers in the order they should be used (must match covariance matrix order)
    """
    print ("stock order:", stock_order)
    w = cvx.Variable(len(stock_order))
    returns = [stock_returns[stock] for stock in stock_order]
    returns = np.array(returns)
    # Objective: Maximize total return
    objective = cvx.Maximize(returns @ w)
    # Constraints
    constraints = []
    # Weights sum to 1
    constraints.append(cvx.sum(w) == 1)
    # Weights are non-negative
    constraints.append(w >= 0)
        # Risk constraint
    risk = cvx.quad_form(w, covariance_matrix)
    constraints.append(risk <= maximum_risk)
       
    problem = cvx.Problem(objective, constraints)
    # Return problem
    # you can set problem.weights = your variable for weights to have access to the weights outside of this method
    problem.weights = w
    return problem

def solve_model(model: cvx.Problem, stock_names: List[str]) -> Dict[str, float]:
    """
    Solve CVXPY model and transform the solution into a dictionary of stock weights
    :param model: CVXPY model
    :param stock_names: list of stock tickers (Names used throughout the file)
    :return: dictionary of stock weights
    """
    
    stock_weights = {}
    for i, stock in enumerate(stock_names):
        stock_weights[stock] = 0
    model.solve()
    for i, stock in enumerate(stock_names):
        stock_weights[stock] = float(model.weights[i].value)
    return stock_weights



def optimize_test_portfolio() -> None:
    """
    Make artificial data for testing
    """

    # Create a dictionary of stock data
    data = {
        "AAPL": [1, 1.02, 1.01, 1.03, 1.04],
        "GOOG": [1, 1.01, 1.02, 1.03, 0.99],
        "MSFT": [1, 0.99, 1.02, 1.03, 1.02],
    }

    # Calculate expected return and variance
    stock_order = list(data.keys())
    expected_returns, covariance_matrix = calculate_stats(data, stock_order)
    print("Expected Returns", expected_returns)
    print("Covariance Matrix", covariance_matrix)


    # 100 is very high, no restriction on variance
    max_risk = 100.00
    model = build_model(expected_returns, covariance_matrix, max_risk, stock_order)

    # Solve the model
    weights = solve_model(model, stock_order)
    print("no cap on risk (or very high)")
    print(weights)

    max_risk = 1.75e-4
    model = build_model(expected_returns, covariance_matrix, max_risk, stock_order)

    # Solve the model
    weights = solve_model(model, stock_order)
    print("Cap on risk of 1e-4, Can no longer buy single best stock")
    print(weights)

    max_risk = 1.5e-4
    model = build_model(expected_returns, covariance_matrix, max_risk, stock_order)

    # Solve the model
    weights = solve_model(model, stock_order)
    print("Cap on risk of 5e-5, can buy even less of best stock")
    print(weights)

def optimize_real_stock_portfolio(max_risk: float) -> None:
    """
    Create a model with real data and solve it

    :param max_risk: maximum risk tolerance
    """
    # Load data (already preprocessed)
    data = get_data()

    # Calculate expected return and variance
    stock_order = list(data.keys())
    expected_returns, covariance_matrix = calculate_stats(data, stock_order)

    # Build the model
    model = build_model(expected_returns, covariance_matrix, max_risk, stock_order)
    # Solve the model
    weights = solve_model(model, stock_order)

    print("Cap on risk of {}".format(max_risk))
    # print with precision
    stocks_bought = [(stock, weights[stock]) for stock in weights if weights[stock] > 0.001]
    sorted_stocks_bought = sorted(stocks_bought, key=lambda x: -x[1]) # sort by weight

    print("Stocks Bought: ")
    print(["{}: {:.2f}".format(s, w) for s, w in sorted_stocks_bought])

def main(max_risk: float = 0.001) -> None:
    print("="*40)
    print("Running with small synthetic test data")
    optimize_test_portfolio()
    print("="*40)
    print("Testing with real data")
    optimize_real_stock_portfolio(max_risk)

if __name__ == "__main__":
    # arg for risk tolerance
    parser = argparse.ArgumentParser(description="Portfolio optimization with risk constraints")
    parser.add_argument("--risk", type=float, default=0.001, 
                       help="Risk tolerance (portfolio variance limit).")
    args = parser.parse_args()
    main(max_risk=args.risk)