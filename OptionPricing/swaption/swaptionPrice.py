# ========== Swaption Pricing Class ==========
class SwaptionPricer:
    """Handles pricing of European swaptions using Black's model."""

    def __init__(self, market_data, strike):
        self.market_data = market_data
        self.strike = strike
        self.swaption_black_prices = np.zeros_like(market_data.swaption_black_vol)

    def price_swaptions(self):
        """Computes swaption prices using Black's model."""
        for i, exercise_date in enumerate(self.market_data.exercise_dates):
            for j, tenor in enumerate(self.market_data.tenors):
                eur_ex_date = self.market_data.settlement_date + ql.Period(exercise_date, ql.Years)
                eur_mat_date = eur_ex_date + ql.Period(tenor, ql.Years)

                fixed_schedule = ql.Schedule(eur_ex_date, eur_mat_date, ql.Period(ql.Annual),
                                             self.market_data.calendar, ql.ModifiedFollowing,
                                             ql.ModifiedFollowing, ql.DateGeneration.Backward, False)
                floating_schedule = ql.Schedule(eur_ex_date, eur_mat_date, ql.Period(ql.Semiannual),
                                                self.market_data.calendar, ql.ModifiedFollowing,
                                                ql.ModifiedFollowing, ql.DateGeneration.Backward, False)

                euribor6m = ql.Euribor6M(self.market_data.term_structure)

                swap = ql.VanillaSwap(ql.VanillaSwap.Payer, 1000000, fixed_schedule, self.strike,
                                      self.market_data.day_count, floating_schedule, euribor6m, 0.0,
                                      self.market_data.day_count)

                vol_handle = ql.QuoteHandle(ql.SimpleQuote(self.market_data.swaption_black_vol[j, i]))
                swaption_vol = ql.ConstantSwaptionVolatility(
                    self.market_data.settlement_date, self.market_data.calendar,
                    ql.ModifiedFollowing, vol_handle, self.market_data.day_count
                )

                swaption = ql.Swaption(swap, ql.EuropeanExercise(eur_ex_date))
                swaption.setPricingEngine(ql.BlackSwaptionEngine(self.market_data.term_structure,
                                                                 ql.SwaptionVolatilityStructureHandle(swaption_vol)))

                self.swaption_black_prices[j, i] = swaption.NPV()

        print("Swaption pricing completed.")
        return self.swaption_black_prices
