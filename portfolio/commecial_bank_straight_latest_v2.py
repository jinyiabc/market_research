import math

import os

import pandas as pd
from datetime import datetime, date
import QuantLib as ql


def date_manipulate(x):
    x = datetime.strptime(x, '%m月%d日')
    return x


def p2f(x):
    return float(x.strip('%')) / 100


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
    ql.Settings.instance().evaluationDate = settlement_date
    """
    Assumption: Yield Curve do not change during holding period.
    """
    commercial_bank_chinabond = pd.read_csv(f'../resource/commecial_bank_straight_latest.CSV',
                                            parse_dates=['COUPON_DATE'],
                                            date_parser=date_manipulate,
                                            )
    length = len(commercial_bank_chinabond)
    calculated_clean_price = []
    holding_1year_return = []
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
        coupon_rate = p2f(ticker['Coupon Description'])  # 0.0556

        # generate schedule

        issue_date = d2q(ticker['Dated Date'])  # ql.Date(30, 6, 2011)
        maturity_date = d2q(ticker['Maturity Date'])  # ql.Date(30, 6, 2031)
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
        # 上海清算所商业银行债收益率曲线(AAA) latest
        spot_dates = [ql.Date(27, 1, 2022),
                      ql.Date(27, 2, 2022),
                      ql.Date(27, 4, 2022),
                      ql.Date(27, 7, 2022),
                      ql.Date(27, 10, 2022),
                      ql.Date(27, 1, 2023),
                      ql.Date(27, 1, 2024),
                      ql.Date(27, 1, 2025),
                      ql.Date(27, 1, 2026),
                      ql.Date(27, 1, 2027),
                      ql.Date(27, 1, 2028),
                      ql.Date(27, 1, 2029),
                      ql.Date(27, 1, 2030),
                      ql.Date(27, 1, 2031),
                      ql.Date(27, 1, 2032),
                      ]
        spot_rates = [
            # 上海清算所商业银行债收益率曲线(AAA) 1-27
            1.856 / 100,
            2.1 / 100,
            2.28 / 100,
            2.33 / 100,
            2.3938 / 100,
            2.43 / 100,
            2.6169 / 100,
            2.7137 / 100,
            2.8233 / 100,
            3.0527 / 100,
            3.2245 / 100,
            3.335 / 100,
            3.4266 / 100,
            3.4674 / 100,
            3.5211 / 100,
        ]
        spread = 0.0  # 0.6/ 100
        spot_rates = [x + spread for x in spot_rates]
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
            # bond.bondYield(100, ql.Actual360(), ql.Compounded, ql.Annual)
            # holding_1year_return.append(
            #     bond.bondYield(100, ql.Actual360(), ql.Compounded, ql.Annual, settlement_date + ql.Period(1, ql.Years)))

            # bond.cleanPrice();print(bond.cleanPrice())
            calculated_clean_price.append(bond.cleanPrice())
            # bond.NPV(); print(bond.NPV())
            # bond.accruedAmount(); print(bond.accruedAmount())
            # bond.dirtyPrice();print(bond.dirtyPrice())
    # holding_1year_return = [value for index, value in enumerate(holding_1year_return) if index % 6 == 0]
    zero_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 0]
    log_linear_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 1]
    cubic_zero_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 2]
    natural_cubic_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 3]
    log_cubic_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 4]
    monotonic_cubic_curve_clean_price = [value for index, value in enumerate(calculated_clean_price) if index % 6 == 5]

    commercial_bank_chinabond['holding_1year_return'] = pd.Series(holding_1year_return)
    commercial_bank_chinabond['zero_curve_clean_price'] = pd.Series(zero_curve_clean_price)
    commercial_bank_chinabond['log_linear_clean_price'] = pd.Series(log_linear_clean_price)
    commercial_bank_chinabond['cubic_zero_curve_clean_price'] = pd.Series(cubic_zero_curve_clean_price)
    commercial_bank_chinabond['natural_cubic_curve_clean_price'] = pd.Series(natural_cubic_curve_clean_price)
    commercial_bank_chinabond['log_cubic_curve_clean_price'] = pd.Series(log_cubic_curve_clean_price)
    commercial_bank_chinabond['monotonic_cubic_curve_clean_price'] = pd.Series(monotonic_cubic_curve_clean_price)
    tolerance = 1.0e-7
    commercial_bank_chinabond['tol_valuation_ratio1'] = (commercial_bank_chinabond['zero_curve_clean_price'] \
                                                         - commercial_bank_chinabond[
                                                             'estimated_clean_price_SHCH']).abs() \
                                                        / commercial_bank_chinabond['estimated_clean_price_SHCH']
    commercial_bank_chinabond['tol_valuation_ratio2'] = (commercial_bank_chinabond['log_linear_clean_price'] \
                                                         - commercial_bank_chinabond[
                                                             'estimated_clean_price_SHCH']).abs() \
                                                        / commercial_bank_chinabond['estimated_clean_price_SHCH']
    commercial_bank_chinabond['tol_valuation_ratio3'] = (commercial_bank_chinabond['cubic_zero_curve_clean_price'] \
                                                         - commercial_bank_chinabond[
                                                             'estimated_clean_price_SHCH']).abs() \
                                                        / commercial_bank_chinabond['estimated_clean_price_SHCH']
    commercial_bank_chinabond['tol_valuation_ratio4'] = (commercial_bank_chinabond['natural_cubic_curve_clean_price'] \
                                                         - commercial_bank_chinabond[
                                                             'estimated_clean_price_SHCH']).abs() \
                                                        / commercial_bank_chinabond['estimated_clean_price_SHCH']
    commercial_bank_chinabond['tol_valuation_ratio5'] = (commercial_bank_chinabond['log_cubic_curve_clean_price'] \
                                                         - commercial_bank_chinabond[
                                                             'estimated_clean_price_SHCH']).abs() \
                                                        / commercial_bank_chinabond['estimated_clean_price_SHCH']
    commercial_bank_chinabond['tol_valuation_ratio6'] = (commercial_bank_chinabond['monotonic_cubic_curve_clean_price'] \
                                                         - commercial_bank_chinabond[
                                                             'estimated_clean_price_SHCH']).abs() \
                                                        / commercial_bank_chinabond['estimated_clean_price_SHCH']

    df2 = commercial_bank_chinabond.loc[:,
          ['Symbol', 'Latest Bond Rating', 'estimated_clean_price_SHCH', 'zero_curve_clean_price',
           'log_linear_clean_price', \
           'cubic_zero_curve_clean_price', 'natural_cubic_curve_clean_price', \
           'log_cubic_curve_clean_price', 'monotonic_cubic_curve_clean_price', \
           'tol_valuation_ratio1', 'tol_valuation_ratio2', \
           'tol_valuation_ratio3', 'tol_valuation_ratio4', \
           'tol_valuation_ratio5', 'tol_valuation_ratio6', 'holding_1year_return' \
           ]].to_csv(f'../resource/commecial_bank_straight_latest_valuation-3.csv')

    # Result: Three valuation method calculate closely with value from SHCH: Shanghai Clearing House.
    # zero_curve_clean_price, cubic_zero_curve_clean_price,natural_cubic_curve_clean_price
