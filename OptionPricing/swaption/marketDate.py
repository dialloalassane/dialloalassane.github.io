import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ========== Market Data Class ==========
class MarketData:
    """Handles market data such as zero curve, volatilities, and rates."""

    def __init__(self, settlement_date):
        self.settlement_date = settlement_date
        self.day_count = ql.Actual360()
        self.calendar = ql.UnitedStates(ql.UnitedStates.Settlement)
        self.compounding = ql.Compounded
        self.compounding_frequency = ql.Annual

        # Zero Curve Data
        self.curve_dates = [self.settlement_date + ql.Period(i, ql.Years) for i in [1, 3, 5, 7, 10, 20, 30]]
        self.zero_rates = [0.019, 0.026, 0.031, 0.035, 0.04, 0.043, 0.043]

        # Create the Zero Curve
        self.zero_curve = ql.ZeroCurve(self.curve_dates, self.zero_rates, self.day_count, self.calendar,
                                       ql.Linear(), self.compounding, self.compounding_frequency)
        self.term_structure = ql.YieldTermStructureHandle(self.zero_curve)

        # Volatility Matrix
        self.swaption_black_vol = np.array([
            [0.22, 0.21, 0.19, 0.17, 0.15, 0.13, 0.12],
            [0.21, 0.19, 0.17, 0.16, 0.15, 0.13, 0.11],
            [0.20, 0.18, 0.18, 0.16, 0.15, 0.14, 0.12],
            [0.19, 0.17, 0.17, 0.15, 0.14, 0.13, 0.12],
            [0.18, 0.16, 0.16, 0.14, 0.13, 0.12, 0.11],
            [0.15, 0.14, 0.14, 0.13, 0.12, 0.12, 0.11],
            [0.13, 0.13, 0.12, 0.11, 0.11, 0.10, 0.09]
        ])

        self.exercise_dates = [1, 2, 3, 4, 5, 7, 10]
        self.tenors = [1, 2, 3, 4, 5, 7, 10]

        print("Market data initialized successfully.")
