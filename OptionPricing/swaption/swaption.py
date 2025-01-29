
import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class YieldCurve:
    def __init__(self, settlement_date, curve_dates, zero_rates):
        self.settlement_date = settlement_date
        self.day_count = ql.Actual360()
        self.calendar = ql.UnitedStates(ql.UnitedStates.Settlement)

        rate_helpers = [
            ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r)), ql.Period(i, ql.Years), 2, self.calendar,
                                 ql.ModifiedFollowing, True, self.day_count) for i, r in zip([1, 3, 5, 7, 10, 20, 30], zero_rates)
        ]

        self.yield_curve = ql.PiecewiseLogLinearDiscount(settlement_date, rate_helpers, self.day_count)
        self.term_structure = ql.YieldTermStructureHandle(self.yield_curve)

    def get_discount_factor(self, maturity_date):
        return self.term_structure.discount(maturity_date)

class HullWhiteModel:
    def __init__(self, yield_curve):
        self.yield_curve = yield_curve
        self.model = ql.HullWhite(self.yield_curve.term_structure)

    def calibrate(self, swaption_helpers):
        optimization_method = ql.LevenbergMarquardt()
        end_criteria = ql.EndCriteria(1000, 100, 1e-6, 1e-6, 1e-6)
        self.model.calibrate(swaption_helpers, optimization_method, end_criteria, ql.NoConstraint(), ql.DoubleVector(), ql.BoolVector())

    def get_params(self):
        return self.model.params()

class Swaption:
    def __init__(self, notional, strike, expiry_dates, model, vol):
        self.notional = notional
        self.strike = strike
        self.expiry_dates = expiry_dates
        self.model = model
        self.vol = vol

    def price_black(self):
        vol_handle = ql.QuoteHandle(ql.SimpleQuote(self.vol))
        swaption_vol = ql.ConstantSwaptionVolatility(
          self.expiry_dates[0],
          ql.UnitedStates(ql.UnitedStates.Settlement),  # Specify market convention
          ql.ModifiedFollowing,
          vol_handle,
          ql.Actual360()
    )
        engine = ql.BlackSwaptionEngine(self.model.yield_curve.term_structure, ql.SwaptionVolatilityStructureHandle(swaption_vol))
        return self._price(engine)

    def price_hull_white(self):
        engine = ql.TreeSwaptionEngine(self.model.model, 50)
        return self._price(engine)

    def _price(self, engine):
        fixed_schedule = ql.Schedule(self.expiry_dates[0], self.expiry_dates[-1], ql.Period(ql.Annual), ql.UnitedStates(ql.UnitedStates.Settlement), # Add ql.UnitedStates.Settlement
                                     ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Backward, False)
        floating_schedule = ql.Schedule(self.expiry_dates[0], self.expiry_dates[-1], ql.Period(ql.Semiannual), ql.UnitedStates(ql.UnitedStates.Settlement), # Add ql.UnitedStates.Settlement
                                        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Backward, False)
        euribor6m = ql.Euribor6M(self.model.yield_curve.term_structure)
        swap = ql.VanillaSwap(ql.VanillaSwap.Payer, self.notional, fixed_schedule, self.strike, ql.Actual360(),
                              floating_schedule, euribor6m, 0.0, ql.Actual360())

        swaption = ql.Swaption(swap, ql.EuropeanExercise(self.expiry_dates[0]))
        swaption.setPricingEngine(engine)
        return swaption.NPV()

class MonteCarloSimulator:
    def __init__(self, num_paths, time_grid, model):
        self.num_paths = num_paths
        self.time_grid = ql.TimeGrid(time_grid)
        self.model = model
    
    def simulate_paths(self):
        uniform_rng = ql.UniformRandomGenerator()
        gaussian_rng = ql.GaussianRandomGenerator(uniform_rng)
        rng = ql.GaussianRandomSequenceGenerator(uniform_seq_gen) # Pass the uniform sequence generator
        generator = ql.GaussianPathGenerator(self.model.model.process(), self.time_grid, rng, False)

        sample_path = generator.next()
        return sample_path.value()
