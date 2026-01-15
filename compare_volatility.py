import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

class DeltaHedgingSimulator:
    def __init__(self, S0, K, T, r, sigma, n_steps):
        self.S = S0          # Initial Stock Price
        self.K = K           # Strike Price
        self.T = T           # Time to expiry (years)
        self.r = r           # Risk-free rate
        self.sigma = sigma   # Volatility
        self.dt = T / n_steps # Time step size
        self.n_steps = n_steps
        
        # Portfolio State
        self.cash = 0
        self.stock_inventory = 0
        self.pnl_history = []
        self.stock_price_history = [S0]
        self.initial_premium = 0

    def black_scholes_delta(self, S, time_left):
        if time_left <= 0: return 0
        d1 = (np.log(S / self.K) + (self.r + 0.5 * self.sigma ** 2) * time_left) / (self.sigma * np.sqrt(time_left))
        return norm.cdf(d1)

    def black_scholes_price(self, S, time_left):
        if time_left <= 0: return max(S - self.K, 0)
        d1 = (np.log(S / self.K) + (self.r + 0.5 * self.sigma ** 2) * time_left) / (self.sigma * np.sqrt(time_left))
        d2 = d1 - self.sigma * np.sqrt(time_left)
        return S * norm.cdf(d1) - self.K * np.exp(-self.r * time_left) * norm.cdf(d2)

    def run(self):
        #Sell the Option
        self.initial_premium = self.black_scholes_price(self.S, self.T)
        self.cash += self.initial_premium 
        
        current_time = self.T
        
        for step in range(self.n_steps):
            # Calculate Target Delta
            target_delta = self.black_scholes_delta(self.S, current_time)
            
            # Re-Hedge (Buy/Sell stock to match Delta)
            # We are Short the Call, so we need to hold Long Stock to neutralize
            desired_stock = target_delta
            trade_size = desired_stock - self.stock_inventory
            
            # Transaction Cost
            cost = trade_size * self.S
            self.cash -= cost
            self.stock_inventory += trade_size

            # Market Move
            # Volatility (self.sigma) drives stock price changes
            shock = np.random.normal(0, 1)
            self.S *= np.exp((self.r - 0.5 * self.sigma**2) * self.dt + self.sigma * np.sqrt(self.dt) * shock)
            self.stock_price_history.append(self.S)
            
            # Mark-to-Market PnL
            current_option_value = self.black_scholes_price(self.S, current_time)
            portfolio_value = self.cash + (self.stock_inventory * self.S) - current_option_value
            self.pnl_history.append(portfolio_value)
            
            current_time -= self.dt
            
        return self.stock_price_history, self.pnl_history, self.initial_premium

def run_comparison():
    # Settings
    S0 = 100
    K = 100
    T = 0.25 # 3 Months
    r = 0.05
    steps = 100
    
    # Scenario A: Low Volatility
    sigma_low = 0.15 # 15%
    sim_low = DeltaHedgingSimulator(S0, K, T, r, sigma_low, steps)
    stocks_low, pnl_low, premium_low = sim_low.run()
    
    # Scenario B: High Volatility
    sigma_high = 0.80 # 80%
    sim_high = DeltaHedgingSimulator(S0, K, T, r, sigma_high, steps)
    stocks_high, pnl_high, premium_high = sim_high.run()

    # PLOTTING
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Low Volatility
    ax1.set_title(f"Scenario A: Low Volatility (15%)\nPremium Collected: ${premium_low:.2f}")
    color = 'tab:blue'
    ax1.plot(stocks_low, color=color, label='Stock Price')
    ax1.set_ylabel('Stock Price', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    ax1_pnl = ax1.twinx()
    color = 'tab:green'
    ax1_pnl.plot(pnl_low, color=color, linestyle='--', label='PnL')
    ax1_pnl.set_ylabel('PnL ($)', color=color)
    ax1_pnl.tick_params(axis='y', labelcolor=color)
    # Set fixed range for PnL to compare fairly
    ax1_pnl.set_ylim(-5, 5)

    # Plot 2: High Volatility
    ax2.set_title(f"Scenario B: High Volatility (80%)\nPremium Collected: ${premium_high:.2f}")
    color = 'tab:red'
    ax2.plot(stocks_high, color=color, label='Stock Price')
    ax2.set_ylabel('Stock Price', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(True, alpha=0.3)
    
    ax2_pnl = ax2.twinx()
    color = 'tab:green'
    ax2_pnl.plot(pnl_high, color=color, linestyle='--', label='PnL')
    ax2_pnl.set_ylabel('PnL ($)', color=color)
    ax2_pnl.tick_params(axis='y', labelcolor=color)
    ax2_pnl.set_ylim(-5, 5)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_comparison()