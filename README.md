# 📉 Options Market Maker Simulator

### "Surviving the Crash: A Study in Dynamic Delta Hedging"

A quantitative simulation engine that mimics the core business model of firms like Optiver. This project demonstrates how a Market Maker collects premiums and manages directional risk (Delta) using dynamic re-hedging, even during simulated market crashes.

## 🚀 The "Why"
Market Makers sell insurance (Options) to the market. They collect cash upfront (Premium) but take on the risk that the stock moves against them.
**The Goal:** How do we keep the cash without going bankrupt when the market crashes?
**The Solution:** Dynamic Delta Hedging.

## ⚙️ How It Works
This Python engine simulates a "trading day" 100 times per second:
1.  **Pricing:** Calculates Fair Value and Greeks (Delta, Gamma, Theta) using the **Black-Scholes Model**.
2.  **Chaos:** Simulates random stock price movements using **Geometric Brownian Motion**.
3.  **Hedging:** Automatically buys/sells the underlying asset to maintain a **Delta-Neutral** position.

## 📊 Visual Results
I ran the simulation under two distinct market regimes to test the algorithm's robustness.

### Scenario A: The Calm Market (15% Volatility)
* **Premium Collected:** ~$3.60
* **Result:** Hedging was efficient. PnL remained flat and stable.

### Scenario B: The Crisis (80% Volatility)
* **Premium Collected:** ~$16.40 (Higher risk = Higher premium)
* **Result:** The algorithm fought hard against **Gamma Risk**. Despite the stock crashing 45%, the Portfolio PnL remained stable, proving the hedge worked.

### Simulation Chart<img width="1400" height="600" alt="simulation_chart" src="https://github.com/user-attachments/assets/4e78a8fe-77a4-41c9-b213-43ac1c4e4841" />


## 🛠️ Tech Stack
* **Python:** Core logic and simulation loop.
* **NumPy & SciPy:** For standard normal distribution (`norm.cdf`) and Brownian motion math.
* **Matplotlib:** For visualizing the "Stock Price vs. Hedged PnL" performance.

## 💻 How to Run
1. Clone the repo:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/optiver-market-maker.git](https://github.com/YOUR_USERNAME/optiver-market-maker.git)
