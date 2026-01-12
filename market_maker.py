import numpy as np
from scipy.stats import norm

class OptionMarketMaker:
    def __init__(self, spot_price, volatility, risk_free_rate=0.05):
        self.S = spot_price       # Current Stock Price 
        self.sigma = volatility   # Implied Volatility
        self.r = risk_free_rate   # Interest Rate 

    def d1_d2(self, K, T):
        """Standard Black-Scholes mathods to calculate d1 and d2."""
        d1 = (np.log(self.S / K) + (self.r + 0.5 * self.sigma ** 2) * T) / (self.sigma * np.sqrt(T))
        d2 = d1 - self.sigma * np.sqrt(T)
        return d1, d2
    
    def get_price_and_greeks(self, K, T):
        """
        Calculates Fair Value + The Greeks.
        K = Strike Price, T = Time to Expiry (years)
        """
        d1, d2 = self.d1_d2(K, T)

        # Fair Value Calculation
        price = self.S * norm.cdf(d1) - K * np.exp(-self.r * T) * norm.cdf(d2)

        # The Greeks Calculation
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (self.S * self.sigma * np.sqrt(T))
        theta = -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(T)) - self.r * K * np.exp(-self.r * T) * norm.cdf(d2)

        return price, delta, gamma, theta
    
    def make_market(self, K, days_left):
        """
        Simulates quoting a Bid/Ask spread.
        """
        T = days_left / 365.0
        fair_value, delta, gamma, theta = self.get_price_and_greeks(K, T)
        
        # We charge a spread to make profit
        spread = 0.04  # $0.04 spread
        bid = fair_value - (spread / 2)
        ask = fair_value + (spread / 2)

        print(f"Fair Value:   ${fair_value:.4f}")
        print(f"My Market:    BID ${bid:.2f}  |  ASK ${ask:.2f}")
        print(f"Spread:       ${spread:.2f} (My Profit)")
        print(f"\n*** RISK METRICS ***")
        print(f"Delta: {delta:.4f}  (If stock +$1, option +${delta:.2f})")
        print(f"Gamma: {gamma:.4f}  (Risk Acceleration)")
        print(f"Theta: {theta:.4f}  (I lose ${abs(theta)/365:.2f} per day)")
    
if __name__ == "__main__":
    # Stock is $100. Volatility is 30%.
    mm = OptionMarketMaker(spot_price=100, volatility=0.3)
    
    # Pricing a $100 Call Option expiring in 30 days
    mm.make_market(K=100, days_left=30)
    
