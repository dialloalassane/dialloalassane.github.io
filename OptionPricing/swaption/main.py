# ========== Market Volatility Plotting Function ==========
import Model 
import utils
import SwaptionPrice
import MarketDate 

def plot_volatility_surface(market_data):
    """Plots the swaption market volatility surface in a 3D mesh format."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create meshgrid for tenors and expiries
    X, Y = np.meshgrid(market_data.tenors, market_data.exercise_dates)

    # Create a colormap
    cmap = plt.cm.coolwarm

    # Plot the surface with colormap
    surf = ax.plot_surface(X, Y, market_data.swaption_black_vol, cmap=cmap, linewidth=0, antialiased=False)

    # Add a colorbar
    fig.colorbar(surf, shrink=0.5, aspect=5)

    # Set labels
    ax.set_xlabel('Tenor (Years)')
    ax.set_ylabel('Expiry (Years)')
    ax.set_zlabel('Volatility')

    # Set title
    plt.title('Swaption Market Volatility Surface')

    plt.show()

def main(): 
  settlement_date = ql.Date(21, 7, 2008)
  ql.Settings.instance().evaluationDate = settlement_date
  
  curve_dates = [settlement_date + ql.Period(i, ql.Years) for i in [1, 3, 5, 7, 10, 20, 30]]
  zero_rates = [0.019, 0.026, 0.031, 0.035, 0.04, 0.043, 0.043]
  yield_curve = YieldCurve(settlement_date, curve_dates, zero_rates)
  
  hw_model = HullWhiteModel(yield_curve)

  #Initialize market data
  market_data = MarketData(settlement_date)
    
  # Plot the market volatility surface
  plot_volatility_surface(market_data)

   
  
  # Define Swaption
  notional = 1e6
  strike = 0.045
  expiry_dates = [settlement_date + ql.Period(i, ql.Years) for i in range(1, 10)]
  swaption_vol = 0.20
  swaption = Swaption(notional, strike, expiry_dates, hw_model, swaption_vol)
  
  # Compute Prices
  black_price = swaption.price_black()
  hw_price = swaption.price_hull_white()
  
  print(f"Swaption Price (Black Model): {black_price:.6f}")
  print(f"Swaption Price (Hull-White Model): {hw_price:.6f}")
  
  # Monte Carlo Simulation
  simulation_years = np.arange(2008, 2018, 1)
  time_grid = list(np.linspace(0, 10, len(simulation_years)))
  num_trials = 1
  simulator = MonteCarloSimulator(num_trials, time_grid, hw_model)
  path = simulator.simulate_paths()
  
  # 3D Plot
  fig = plt.figure(figsize=(10, 7))
  ax = fig.add_subplot(111, projection='3d')
  X, Y = np.meshgrid(np.linspace(0, 10, 20), simulation_years)
  ax.plot_surface(X, Y, np.array(path), cmap='viridis')
  ax.set_xlabel("Tenor (Years)")
  ax.set_ylabel("Time (Years)")
  ax.set_zlabel("Zero Rate")
  ax.set_title("Evolution of the Zero Curve for Trial:1 of Hull-White Model")
  plt.show()
