import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
import requests
import pandas as pd

# Replace with your Alpha Vantage API key
API_KEY = 'your_alpha_vantage_api_key'
BASE_URL = 'https://www.alphavantage.co/query'

# Function to fetch stock data
def fetch_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'Time Series (Daily)' in data:
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df
    else:
        print(f"Error fetching data for {symbol}: {data.get('Note', 'Unknown error')}")
        return None

# Function to add a stock to the portfolio
def add_stock(portfolio, symbol, shares):
    if symbol in portfolio:
        portfolio[symbol]['shares'] += shares
    else:
        portfolio[symbol] = {'shares': shares}
    print(f"Added {shares} shares of {symbol} to portfolio.")

# Function to remove a stock from the portfolio
def remove_stock(portfolio, symbol, shares):
    if symbol in portfolio:
        if portfolio[symbol]['shares'] > shares:
            portfolio[symbol]['shares'] -= shares
        elif portfolio[symbol]['shares'] == shares:
            del portfolio[symbol]
        else:
            print(f"Not enough shares to remove for {symbol}.")
    else:
        print(f"{symbol} not found in portfolio.")
    print(f"Removed {shares} shares of {symbol} from portfolio.")

# Function to track portfolio performance
def track_portfolio(portfolio):
    portfolio_data = {}
    for symbol, info in portfolio.items():
        df = fetch_stock_data(symbol)
        if df is not None:
            last_close_price = df.iloc[-1]['Close']
            portfolio_data[symbol] = {
                'shares': info['shares'],
                'last_close_price': last_close_price,
                'total_value': info['shares'] * float(last_close_price)
            }
    return portfolio_data

# Function to handle user input safely
def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Main function to interact with the user
def main():
    portfolio = {}
    while True:
        print("\n1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Portfolio")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = get_integer_input("Enter number of shares: ")
            add_stock(portfolio, symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = get_integer_input("Enter number of shares: ")
            remove_stock(portfolio, symbol, shares)
        elif choice == '3':
            portfolio_data = track_portfolio(portfolio)
            for symbol, data in portfolio_data.items():
                print(f"\n{symbol}:")
                print(f"  Shares: {data['shares']}")
                print(f"  Last Close Price: ${data['last_close_price']}")
                print(f"  Total Value: ${data['total_value']:.2f}")
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
