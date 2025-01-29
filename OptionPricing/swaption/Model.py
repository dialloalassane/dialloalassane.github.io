# ========== Hull-White Calibration Class ==========
class HullWhiteCalibrator:
    """Handles calibration of Hull-White model using swaptions."""

    def __init__(self, market_data, swaption_pricer):
        self.market_data = market_data
        self.swaption_pricer = swaption_pricer
        self.hw_model = ql.HullWhite(self.market_data.term_structure)

    def calibrate_model(self):
        """Calibrates the Hull-White model to swaption prices."""
        swaption_helpers = []
        for i, exercise_date in enumerate(self.market_data.exercise_dates):
            for j, tenor in enumerate(self.market_data.tenors):
                if self.market_data.swaption_black_vol[j, i] <= 0:
                    continue

                eur_ex_date = self.market_data.settlement_date + ql.Period(exercise_date, ql.Years)
                eur_mat_date = eur_ex_date + ql.Period(tenor, ql.Years)

                fixed_schedule = ql.Schedule(eur_ex_date, eur_mat_date, ql.Period(ql.Annual),
                                             self.market_data.calendar, ql.ModifiedFollowing,
                                             ql.ModifiedFollowing, ql.DateGeneration.Backward, False)

                euribor6m = ql.Euribor6M(self.market_data.term_structure)

                vol_handle = ql.QuoteHandle(ql.SimpleQuote(self.market_data.swaption_black_vol[j, i]))

                helper = ql.SwaptionHelper(ql.Period(exercise_date, ql.Years), ql.Period(tenor, ql.Years),
                                           vol_handle, euribor6m, ql.Period(ql.Annual),
                                           self.market_data.day_count, self.market_data.day_count,
                                           self.market_data.term_structure)

                swaption_helpers.append(helper)

        optimization_method = ql.LevenbergMarquardt()
        end_criteria = ql.EndCriteria(1000, 100, 1e-6, 1e-6, 1e-6)

        self.hw_model.calibrate(swaption_helpers, optimization_method, end_criteria, ql.NoConstraint())

        print(f"\nCalibrated Hull-White Parameters:")
        print(f"Alpha (mean reversion): {self.hw_model.params()[0]:.6f}")
        print(f"Sigma (volatility): {self.hw_model.params()[1]:.6f}")
