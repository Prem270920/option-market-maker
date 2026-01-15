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
        
        # Portfolio
        self.cash = 0
        self.stock_inventory = 0
        self.pnl_history = []
        self.stock_price_history = [S0]

    def black_scholes_delta(self, S, time_left):
        """Calculate Delta (Risk)"""
        if time_left <= 0: return 0
        d1 = (np.log(S / self.K) + (self.r + 0.5 * self.sigma ** 2) * time_left) / (self.sigma * np.sqrt(time_left))
        return norm.cdf(d1)
    
    def black_scholes_price(self, S, time_left):
        """Calculate Option Price"""
        if time_left <= 0: return max(S - self.K, 0)
        d1 = (np.log(S / self.K) + (self.r + 0.5 * self.sigma ** 2) * time_left) / (self.sigma * np.sqrt(time_left))
        d2 = d1 - self.sigma * np.sqrt(time_left)
        return S * norm.cdf(d1) - self.K * np.exp(-self.r * time_left) * norm.cdf(d2)
    
    def run_simulation(self):
        print(f"STARTING SIMULATION: {self.n_steps} STEPS")
        
        # SELL 1 Call Option at the start
        # collect cash from selling the option
        initial_option_price = self.black_scholes_price(self.S, self.T)
        self.cash += initial_option_price 
        print(f"Sold Option for ${initial_option_price:.2f}. Cash: ${self.cash:.2f}")

        current_time = self.T

        for step in range(self.n_steps):
            # Calculate current Delta
            target_delta = self.black_scholes_delta(self.S, current_time)
            
            # If we sold the call, we are "Short Delta". To be neutral, we must BUY stock
            desired_stock = target_delta
            trade_size = desired_stock - self.stock_inventory
            
            if abs(trade_size) > 0.001: # trade if difference is significant
                cost = trade_size * self.S
                self.cash -= cost
                self.stock_inventory += trade_size

            # simulate Market Move 
            # Brownian Motion formula: S_new = S_old * exp(...)
            shock = np.random.normal(0, 1)
            self.S *= np.exp((self.r - 0.5 * self.sigma**2) * self.dt + self.sigma * np.sqrt(self.dt) * shock)
            self.stock_price_history.append(self.S)
            
            # Track PnL (Mark-to-Market)
            # PnL = Cash + (Stock Value) - (Liability: Value of Option we sold)
            current_option_value = self.black_scholes_price(self.S, current_time)
            portfolio_value = self.cash + (self.stock_inventory * self.S) - current_option_value
            self.pnl_history.append(portfolio_value)
            
            current_time -= self.dt

        # Final Report
        print(f" SIMULATION END ")
        print(f"Final Stock Price: ${self.S:.2f}")
        print(f"Final PnL: ${self.pnl_history[-1]:.2f}")
        
        # Plotting
        self.plot_results()

    def plot_results(self):
        fig, ax1 = plt.subplots()
        
        color = 'tab:blue'
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Stock Price', color=color)
        ax1.plot(self.stock_price_history, color=color, label='Stock Price')
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx() 
        color = 'tab:green'
        ax2.set_ylabel('My PnL ($)', color=color)
        ax2.plot(self.pnl_history, color=color, linestyle='--', label='Hedged PnL')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title("Delta Hedging Simulation: Surviving Volatility")
        plt.show()

if __name__ == "__main__":
    sim = DeltaHedgingSimulator(S0=100, K=100, T=0.25, r=0.05, sigma=0.2, n_steps=100)
    sim.run_simulation()