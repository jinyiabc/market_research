import pandas as pd
from datetime import datetime, date
import QuantLib as ql

def date_manipulate(x):
    x = datetime.strptime(x, '%m月%d日')
    return x

def p2f(x):
    return float(x.strip('%'))/100

def d2q(x):
    day = int(x.split('/')[1])
    year = int(x.split('/')[2])
    month = int(x.split('/')[0])
    return ql.Date(day, month, year)

if __name__ == '__main__':

    """
    GLOBAL SETTINGS
    """
    settlement_date = ql.Date(27, 1, 2022)
    ql.Settings.instance().evaluationDate = ql.Date(27, 1, 2022)
    """
    Assumption: Yield Curve do not change during holding period.
    """


    commercial_bank_chinabond = pd.read_csv('../resource/commecial_bank_sub_latest.CSV',
                                            parse_dates=['COUPON_DATE'],
                                            date_parser=date_manipulate,
                                            )
    length = len(commercial_bank_chinabond)
    calculated_clean_price = []
    for i in range(length):
        ticker = commercial_bank_chinabond.iloc[i]
        """
        INFORMATION
                Symbol                                                                            1105001.IB
                Short Name                                                                ICBC 5.56% B310630
                Close (D)\r\n[Trade Date] Last Closing Day\r\n[Price Type] Dirty Price              103.1889
                Bid Yield (Optimal)\r\n[Trade Date] Last Closing Day\r\n[Unit] %                         NaN
                Initial Face Value                                                                     100.0
                Latest Bond Rating                                                                       AAA
                Maturity Date                                                                     2031-06-30
                Coupon Type                                                            Fixed Interest Rate
                Interest Accrual Method                                                 Simple interest
                Coupon Description                                                    5.56%
                Coupon Frequency                                                        1
                Coupon Date (Y)\r\n[N] 1                                             6月30日
                Bond Term (Year)\r\n[Unit] Yearly                                    20.0
                Maturities (Text)                                                     15+5
                Interest Reference                                                     ACT/ACT
                Coupon Date Description           Pay interest on June 30 every year, and postpo...
                Bond Term (Year)\r\n[Unit] Yearly.1                                     20.0
                Issue Amount\r\n[Unit] (100M)                                           380.0
                Remaing Maturity                                                         9.41
                
                BENCHMARK
                债券代码	债券简称▲	估值日期▲	流通场所	待偿期	日间估价全价	日间应计利息	估价净价	估价收益率
                1105001	11工行01	2022-01-27	银行间	9.4219	114.4813	3.2141	111.2672	4.0910
        """
        coupon_rate = p2f(ticker['Coupon Description'])    # 0.0556

        # generate schedule

        issue_date = d2q(ticker['Dated Date'])   # ql.Date(30, 6, 2011)
        maturity_date = d2q(ticker['Maturity Date'])#  ql.Date(30, 6, 2031)
        tenor = ql.Period(ql.Annual)
        calendar = ql.China()
        convention = ql.Following
        terminationDateConvention = ql.Following
        rule = ql.DateGeneration.Forward
        month_end = False
        schedule = ql.Schedule(issue_date, maturity_date, tenor,
                               calendar, convention,
                               terminationDateConvention, rule,
                               month_end)
        settlementDays = 1
        dc = ql.ActualActual()
        fixed_leg = ql.FixedRateLeg(schedule, dc, [100], [coupon_rate])
        bond = ql.Bond(settlementDays, ql.TARGET(), issue_date, fixed_leg)

        spot_dates = [ql.Date(27, 1, 2022),
                      ql.Date(27, 4, 2022),
                      ql.Date(27, 7, 2022),
                      ql.Date(27, 10, 2022),
                      ql.Date(27, 1, 2023),
                      ql.Date(27, 1, 2025),
                      ql.Date(27, 1, 2027),
                      ql.Date(27, 1, 2029),
                      ql.Date(27, 1, 2032),
                      ql.Date(27, 1, 2037),
                      ql.Date(27, 1, 2042),
                      ql.Date(27, 1, 2052),
                      ]
        spot_rates = [ 2.1048 / 100,
                        2.3085 / 100,
                        2.3634 / 100,
                        2.4317 / 100,
                        2.4652 / 100,
                        2.6922 / 100,
                        3.0388 / 100,
                        3.3562 / 100,
                        3.4502 / 100,
                        3.6769 / 100,
                        3.8052 / 100,
                        3.8791 / 100]
        spread = 0.0 # 0.6/ 100
        spot_rates = [x + spread for x in spot_rates]
        # # 上海清算所商业银行债收益率曲线(AAA) 1-27
        # spot_dates = [ql.Date(27, 1, 2022),
        #               ql.Date(27, 2, 2022),
        #               ql.Date(27, 4, 2022),
        #               ql.Date(27, 7, 2022),
        #               ql.Date(27, 10, 2022),
        #               ql.Date(27, 1, 2023),
        #               ql.Date(27, 1, 2024),
        #               ql.Date(27, 1, 2025),
        #               ql.Date(27, 1, 2026),
        #               ql.Date(27, 1, 2027),
        #               ql.Date(27, 1, 2028),
        #               ql.Date(27, 1, 2029),
        #               ql.Date(27, 1, 2030),
        #               ql.Date(27, 1, 2031),
        #               ql.Date(27, 1, 2032),
        #               ]
        # spot_rates = [
        #     # 上海清算所商业银行债收益率曲线(AAA) 1-27
        #     1.9 / 100,
        #     2.37 / 100,
        #     2.38 / 100,
        #     2.41 / 100,
        #     2.44 / 100,
        #     2.45 / 100,
        #     2.5692 / 100,
        #     2.6906 / 100,
        #     2.8293 / 100,
        #     3.0076 / 100,
        #     3.1493 / 100,
        #     3.2994 / 100,
        #     3.3699 / 100,
        #     3.3981 / 100,
        #     3.4531 / 100,
        #     # 上海清算所商业银行债收益率曲线(AA+) 1-27
        #     # 1.95 / 100,
        #     # 2.4198 / 100,
        #     # 2.4292 / 100,
        #     # 2.4599 / 100,
        #     # 2.4892 / 100,
        #     # 2.5 / 100,
        #     # 2.6465 / 100,
        #     # 2.7481 / 100,
        #     # 2.9432 / 100,
        #     # 3.148 / 100,
        #     # 3.2909 / 100,
        #     # 3.4466 / 100,
        #     # 3.5317 / 100,
        #     # 3.5748 / 100,
        #     # 3.6285 / 100,
        # ]
        # day_count = ql.ActualActual()
        # interpolation = ql.Linear()
        compounding = ql.Compounded
        compounding_frequency = ql.Annual
        # spot_curve = ql.ZeroCurve(spot_dates, spot_rates, day_count, calendar,
        #                           interpolation, compounding, compounding_frequency)   # 116.63027293435499
        spot_curves = []
        spot_curves.append(ql.ZeroCurve(spot_dates, spot_rates, dc, calendar, ))
        spot_curves.append(ql.LogLinearZeroCurve(spot_dates, spot_rates, dc, calendar, ))
        spot_curves.append(ql.CubicZeroCurve(spot_dates, spot_rates, dc, calendar, ))
        spot_curves.append(ql.NaturalCubicZeroCurve(spot_dates, spot_rates, dc, calendar, ))
        spot_curves.append(ql.LogCubicZeroCurve(spot_dates, spot_rates, dc, calendar, ))
        spot_curves.append(ql.MonotonicCubicZeroCurve(spot_dates, spot_rates, dc, calendar, ))
        for spot_curve in spot_curves:
            spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)
            bond_engine = ql.DiscountingBondEngine(spot_curve_handle)
            bond.setPricingEngine(bond_engine)
            # bond.cleanPrice();print(bond.cleanPrice())
            calculated_clean_price.append(bond.cleanPrice())
            # bond.NPV(); print(bond.NPV())
            # bond.accruedAmount(); print(bond.accruedAmount())
            # bond.dirtyPrice();print(bond.dirtyPrice())
    zero_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 0 ]
    log_linear_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 1]
    cubic_zero_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 2]
    natural_cubic_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 3]
    log_cubic_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 4]
    monotonic_cubic_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 5]

    commercial_bank_chinabond['zero_curve_clean_price'] = pd.Series(zero_curve_clean_price)
    commercial_bank_chinabond['log_linear_clean_price'] = pd.Series(log_linear_clean_price)
    commercial_bank_chinabond['cubic_zero_curve_clean_price'] = pd.Series(cubic_zero_curve_clean_price)
    commercial_bank_chinabond['natural_cubic_curve_clean_price'] = pd.Series(natural_cubic_curve_clean_price)
    commercial_bank_chinabond['log_cubic_curve_clean_price'] = pd.Series(log_cubic_curve_clean_price)
    commercial_bank_chinabond['monotonic_cubic_curve_clean_price'] = pd.Series(monotonic_cubic_curve_clean_price)
    commercial_bank_chinabond.loc[:, ['Symbol','estimated_clean_price_SHCH','zero_curve_clean_price','log_linear_clean_price', \
                                            'cubic_zero_curve_clean_price','natural_cubic_curve_clean_price',\
                                            'log_cubic_curve_clean_price','monotonic_cubic_curve_clean_price']].to_csv('../resource/commercial_bank_valuation.csv')

    # commercial_bank_chinabond.to_csv('../resource/commercial_bank_valuation.csv')