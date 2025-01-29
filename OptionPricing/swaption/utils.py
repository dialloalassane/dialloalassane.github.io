# ========== Market Volatility Plotting Function ==========
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

