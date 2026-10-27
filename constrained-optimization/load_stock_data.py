from typing import Dict, List
import pandas as pd

def load_data(filename: str) -> pd.DataFrame:
    """
    Load stock data from CSV file.
    Extract data only from the last year
    """
    df = pd.read_csv(filename)
    
    # Convert numeric columns to float
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert date column
    df['Date'] = pd.to_datetime(df['Date'])
    latest_date = df['Date'].max()
    one_year_ago = latest_date - pd.DateOffset(years=1)
    df = df[df['Date'] >= one_year_ago]
    
    # Remove duplicate entries for same ticker on same date (keep first)
    df = df.drop_duplicates(subset=['Date', 'Ticker'], keep='first')
    
    # Sort by date and ticker
    df = df.sort_values(['Ticker', 'Date'])
    
    # Ensure all stocks have the same length by finding common dates
    # First, find the maximum number of observations any stock has
    ticker_counts = df.groupby('Ticker').size()
    print(f"Ticker observation counts: min={ticker_counts.min()}, max={ticker_counts.max()}, mean={ticker_counts.mean():.1f}")
    
    # Find the set of dates that all remaining tickers have
    all_dates = set(df['Date'].unique())
    for ticker in df['Ticker'].unique():
        ticker_dates = set(df[df['Ticker'] == ticker]['Date'])
        all_dates = all_dates.intersection(ticker_dates)
    
    # Keep only the common dates
    df = df[df['Date'].isin(all_dates)]
    
    # Sort again after filtering
    df = df.sort_values(['Ticker', 'Date'])
    
    return df

def normalize_stock_data(stock_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize stock data so that each ticker's first price becomes 1.0."""
    # Create a copy and ensure proper sorting
    df = stock_df.copy()
    df = df.sort_values(['Ticker', 'Date'])
    
    # Calculate normalized prices (first price = 1.0)
    first_prices = df.groupby('Ticker')['Close'].transform('first')
    df['Normalized_Close'] = df['Close'] / first_prices
    
    return df

def create_price_dictionary(df: pd.DataFrame) -> Dict[str, List[float]]:
    """Create a dictionary of normalized stock prices with split adjustments."""
    # Normalize the data (this now includes split adjustments)
    df_norm = normalize_stock_data(df)
    
    # Create dictionary of price series
    price_dict: Dict[str, List[float]] = {}
    
    for ticker, group in df_norm.groupby('Ticker'):
        # Only include stocks with full data
        group_df = group.sort_values('Date')  # type: ignore
        prices = group_df['Normalized_Close'].tolist()
        price_dict[str(ticker)] = prices
    
    return price_dict

def get_data() -> Dict[str, List[float]]:
    """Load and analyze stock data with split adjustments."""
    df = load_data('World-Stock-Prices-Dataset.csv')
    
    # Check if data might already be split-adjusted
    split_stocks = df[df['Stock Splits'] > 0]['Ticker'].nunique()

    
    price_dict = create_price_dictionary(df)
    total_stocks = len(price_dict)
    
    for stock in price_dict:
        # Since data is normalized with first price = 1.0, final price is the total return
        print(f"{stock}: {price_dict[stock][-1]:.3f} (total return: {price_dict[stock][-1] - 1:.1%})")
    return price_dict
